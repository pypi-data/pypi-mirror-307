from functools import partial

import jax
import jax.numpy as jnp
import numpy as np

from qax.utils import vmap_all_but_one
from .pack import pack_along_axis

BITS = 4
MAXQ = 2 ** BITS - 1

NF4 = jnp.asarray([-1.0, -0.6961928009986877, -0.5250730514526367, -0.39491748809814453, -0.28444138169288635, -0.18477343022823334, -0.09105003625154495, 0.0, 0.07958029955625534, 0.16093020141124725, 0.24611230194568634, 0.33791524171829224, 0.44070982933044434, 0.5626170039176941, 0.7229568362236023, 1.0])


def get_global_absmax(weight):
    return jnp.max(jnp.abs(weight))

def get_absmax(weight, contraction_axis=0):
    return {'scale': vmap_all_but_one(get_global_absmax, contraction_axis)(weight)}

def get_global_scale_and_zero(weight):
    xmin = jnp.min(weight)
    xmax = jnp.max(weight)

    xmax = jnp.where(xmax == xmin, xmin + 1, xmax)

    scale = xmax - xmin
    scale = (xmax - xmin) / 2
    zero = (xmin + xmax) / 2
    return {'scale': scale, 'zero': zero}


def get_scale_and_zero(weight, contraction_axis=0):
    return vmap_all_but_one(get_global_scale_and_zero, contraction_axis)(weight)

def _quantize(vec, zero, scale, code, block_size=-1):
    if zero is not None:
        vec -= zero

    if scale is not None:
        vec /= scale

    if code is not None:
        dists = jnp.abs(vec[..., None] - code)
        coded = jnp.argmin(dists, axis=-1)
    else:
        coded = jnp.round((vec + 1) * MAXQ / 2)

    q = jnp.clip(coded, 0, 2 ** BITS - 1)
    return q.astype(jnp.uint8)

def quantize_matrix(weight, zero=None, scale=None, code=None, contraction_axis=0):
    zero, scale = jax.tree_map(partial(jnp.expand_dims, axis=contraction_axis), (zero, scale))

    return _quantize(weight, zero, scale, code)

def _dequantize(value, zero, scale, code, dtype):
    if code is not None:
        value = code[value].astype(dtype)
    else:
        value = value.astype(dtype) * 2 / MAXQ - 1

    if scale is not None:
        value *= scale.astype(dtype)
    if zero is not None:
        value += zero.astype(dtype)
    return value

def dequantize_matrix(int_weight, zero=None, scale=None, code=None, contraction_axis=0, dtype=None):
    if dtype is None:
        dtype = next((v.dtype for v in (zero, scale, code) if v is not None), None)
        if dtype is None:
            raise ValueError('dtype must be specified if zero, scale, and code are all None')

    zero, scale = jax.tree_map(partial(jnp.expand_dims, axis=contraction_axis), (zero, scale))

    return _dequantize(int_weight, zero, scale, code, dtype)

def quantize_and_pack(W, use_absmax=False, contraction_axis=0, code=None):
    if use_absmax:
        params = get_absmax(W, contraction_axis=contraction_axis)
    else:
        params = get_scale_and_zero(W, contraction_axis=contraction_axis)

    Q = quantize_matrix(W, **params, code=code, contraction_axis=contraction_axis)

    packed = pack_along_axis(contraction_axis, Q)
    return packed, params
