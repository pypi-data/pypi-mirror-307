
from .base_class import SingleStepQuantity
from ...extensions import ForwardOutputExtension
from ..utils.calculation import *

import jittor as jt

class RankMe(SingleStepQuantity):
    def _compute(self, global_step):
        data = self._module.output
        data = data.view(data.shape[0], -1)
        svd_values = cal_eig_not_sym(data)  
        eps = 1e-7
        svd_values_norm1 = jt.norm(svd_values, p=1)
        rankme = jt.exp(-jt.sum(
            [(svd_values[i] / svd_values_norm1 + eps) * jt.log(svd_values[i] / svd_values_norm1 + eps) for i in range(min(data.shape))]
        ))
        return rankme

    def forward_extensions(self):
        extensions = [ForwardOutputExtension()]
        return extensions
