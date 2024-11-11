import jax.numpy as jnp

from qax import ImplicitArray
from . import quant_utils
from .pack import unpack_along_axis


class Packed4BitMatrix(ImplicitArray):
    def __init__(self, int_weight, zero=None, scale=None, code=None, *, orig_shape, dtype, contraction_axis=0):
        super().__init__(shape=orig_shape, dtype=dtype)
        self.int_weight = int_weight
        self.zero = zero
        self.scale = scale
        self.code = code
        self.contraction_axis = contraction_axis

    def materialize(self):
        unpacked = unpack_along_axis(self.contraction_axis, self.int_weight)
        dequantized = quant_utils.dequantize_matrix(
            unpacked,
            zero=self.zero,
            scale=self.scale,
            code=self.code,
            contraction_axis=self.contraction_axis,
            dtype=self.dtype
        )
        return dequantized

    def flatten(self):
        return [
            ('int_weight', self.int_weight),
            ('zero', self.zero),
            ('scale', self.scale),
            ('code', self.code)
        ], (self.contraction_axis,)

    def unflatten(self, aux_data, children):
        self.int_weight, self.zero, self.scale, self.code = children
        self.contraction_axis, = aux_data

    @classmethod
    def from_full_precision(cls, W, use_absmax=False, contraction_axis=0, code=None):
        packed, params = quant_utils.quantize_and_pack(W, use_absmax=use_absmax, contraction_axis=contraction_axis, code=code)
        return cls(
            int_weight=packed,
            **params,
            contraction_axis=contraction_axis,
            orig_shape=W.shape,
            dtype=W.dtype,
            code=code
        )
