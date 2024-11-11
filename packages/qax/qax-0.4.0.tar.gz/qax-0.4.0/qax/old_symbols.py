"""
ImplicitArray subclasses representing arbitrarily shaped constant values.
This is basically for DIY constant-folding.
"""

from abc import abstractmethod
from dataclasses import dataclass
from functools import partial
from typing import Union

import jax
import jax.numpy as jnp
import numpy as np
from plum import Signature

from .implicit_array import ArrayValue, ImplicitArray, UninitializedAval
from .primitives import get_primitive_handler, primitive_handler, default_handler
from .type_utils import Complement
from .constants import ELEMENTWISE_BINOPS, ELEMENTWISE_UNOPS

def _get_shape_dtype(x, shape, dtype):
    if shape is None:
        shape = np.shape(x)
    else:
        shape = jax.core.canonicalize_shape(shape)

    if dtype is None:
        jax.lax.dtype(x)
    return shape, dtype

def _out_shape_dtype(primitive, x, y, **kwargs):
    out_aval = jax.eval_shape(
        partial(default_handler, primitive, **kwargs),
        jax.core.get_aval(x),
        jax.core.get_aval(y)
    )
    return jax.tree_map(
        lambda x: (x.shape, x.dtype),
        out_aval
    )

def symbolic_zero_like(x, shape=None, dtype=None):
    shape, dtype = _get_shape_dtype(x, shape, dtype)
    return Zeros(shape=shape, dtype=dtype)

def symbolic_full_like(x, fill_value, shape=None):
    shape, _ = _get_shape_dtype(x, shape, None)
    return Full(fill_value, shape=shape)

class SymConstant(ImplicitArray):
    @abstractmethod
    def get_value(self):
        pass

    def materialize(self):
        return jnp.full(self.shape, self.get_value(), dtype=self.dtype)

    def reshape(self, *shape):
        copy = jax.tree_map(lambda x: x, self)
        copy.shape = shape
        return copy

    def astype(self, dtype):
        copy = jax.tree_map(lambda x: x, self)
        copy.dtype = dtype
        return copy

class Zeros(SymConstant):
    default_dtype = jnp.float32
    def get_value(self):
        return jnp.zeros((), dtype=self.dtype)

class Ones(SymConstant):
    default_dtype = jnp.float32

    def get_value(self):
        return jnp.ones((), dtype=self.dtype)

@dataclass
class Full(SymConstant):
    value : jax.Array

    def __post_init__(self):
        try:
            _ = self.dtype
        except UninitializedAval:
            self.dtype = jax.lax.dtype(self.value)

        super().__post_init__()

    def get_value(self):
        return self.value

    def astype(self, dtype):
        copy = Full(jax.lax.convert_element_type(self.value, dtype), shape=self.shape)
        return copy

_NULL = -1
_IDENTITY = -2
_GENERAL = -3

def identity(primitive, sym, other):
    shape, dtype = _out_shape_dtype(primitive, sym, other)
    return other.astype(dtype).reshape(*shape)

def right_null(primitive, other, sym):
    return null(primitive, sym, other)

def register_identity(primitive, kind):
    @primitive_handler(primitive, precedence=_IDENTITY)
    def identity_handler(primitive, sym : kind, other : ArrayValue, **kwargs):
        return identity(primitive, sym, other)

    @primitive_handler(primitive, precedence=_IDENTITY)
    def right_identity_handler(primitive, other : Complement[ArrayValue, kind], sym : kind, **kwargs):
        return identity(primitive, sym, other)

def null(primitive, sym, other):
    shape, dtype = _out_shape_dtype(primitive, sym, other)
    return sym.astype(dtype).reshape(*shape)

def register_null(primitive, kind):
    @primitive_handler(primitive, precedence=_NULL)
    def null_handler(primitive, sym : kind, other : ArrayValue, **kwargs):
        return null(primitive, sym, other)

    @primitive_handler(primitive, precedence=_NULL)
    def right_null_handler(primitive, other : Complement[ArrayValue, kind], sym : kind, **kwargs):
        return null(primitive, sym, other)

register_identity('mul', Ones)
register_identity('add', Zeros)
register_null('mul', Zeros)

register_identity('xor', Zeros)
reigster_identity('or', Zeros)
register_null('and', Zeros)

@primitive_handler(ELEMENTWISE_UNOPS, precedence=_GENERAL)
def handle_unop(primitive, sym : SymConstant, **kwargs):
    new_val = default_handler(primitive, sym.get_value(), **kwargs)
    return symbolic_full_like(sym, new_val)

@primitive_handler(ELEMENTWISE_BINOPS, precedence=_GENERAL)
def handle_binop(primitive, lhs : SymConstant, rhs : SymConstant, **kwargs):
    out_shape, out_dtype = _out_shape_dtype(primitive, lhs, rhs, **kwargs)
    new_val = default_handler(primitive, lhs.get_value(), rhs.get_value(), **kwargs)
    return symbolic_full_like(lhs, new_val, shape=out_shape)

def unchanged_unop(primitive, sym : Union[Zeros,Ones], **kwargs):
    out_shape, out_dtype = _out_shape_dtype(primitive, sym, **kwargs)
    return type(sym)(shape=out_shape, dtype=out_dtype)

@primitive_handler([
    'reduce_and',
    'reduce_or',
    'reduce_prod',
    'reduce_max',
    'reduce_min',
    'reduce_sum',
    'reduce_xor'
])
def zero_reductions(primitive, sym : Zeros, *, axes):
    return unchanged_unop(primitive, sym, axes=axes)

@primitive_handler([
])
