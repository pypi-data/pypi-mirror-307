import jax.numpy as jnp

from qax.utils import vmap_all_but_one

def _pack(w_int):
    assert len(w_int.shape) == 1
    pack_dtype = jnp.uint8
    ele_width = pack_dtype.dtype.itemsize * 8
    bits = 4
    vals_per_int = ele_width // bits

    result = jnp.zeros(w_int.shape[0] // vals_per_int, dtype=pack_dtype)

    for offset in range(vals_per_int):
        result = result | (w_int[offset::vals_per_int] << (bits * offset)).astype(pack_dtype)

    return result

def _unpack(packed):
    assert len(packed.shape) == 1
    bits = 4
    ele_width = packed.dtype.itemsize * 8
    vals_per_int = ele_width // bits
    result = jnp.zeros(packed.shape[0] * vals_per_int, dtype=jnp.uint8)

    mask = (1 << bits) - 1
    for offset in range(vals_per_int):
        result = result.at[offset::vals_per_int].set(
            jnp.uint8(packed >> (bits * offset) & mask)
        )
    return result

def pack_along_axis(axis, w):
    return vmap_all_but_one(_pack, axis, out_ndim=1)(w)

def unpack_along_axis(axis, w):
    return vmap_all_but_one(_unpack, axis, out_ndim=1)(w)
