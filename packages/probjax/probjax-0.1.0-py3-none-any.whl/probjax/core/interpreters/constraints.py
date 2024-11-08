# TODO propagate constraints
from typing import Any, Iterable, Sequence, Tuple

from jax import lax
from jax.core import JaxprEqn

from probjax.core.interpreters.trace import TraceProcessingRule
from probjax.distributions.constraints import (
    positive,
    real,
    unit_interval,
    unit_square,
)

_UNIVARIATE_CONSTRAINTS = {
    lax.tanh_p: (real, unit_square),
    lax.erf_p: (real, unit_interval),
    lax.exp_p: (real, positive),
    lax.log_p: (positive, real),
    lax.sin_p: (real, unit_square),
    lax.cos_p: (real, unit_square),
    lax.tan_p: (real, unit_square),
}


class ConstraintTraceProcessingRule(TraceProcessingRule):
    def __init__(self, init_constraints, traced_vars: Iterable | None = None) -> None:
        super().__init__(traced_vars)
        self.invar_constraints = init_constraints

    def __call__(
        self, eqn: JaxprEqn, known_inputs: Sequence[Any | None], _: Sequence[Any | None]
    ) -> Tuple[Sequence[Any | None], Sequence[Any | None]]:
        outvars, outvals = super().__call__(eqn, known_inputs, _)
        primitive = eqn.primitive
        in_constraints = [self.traced_samples[str(i)] for i in eqn.invars]
        for o, v in zip(outvars, outvals):
            if self.traced_vars is None or str(o) in self.traced_vars:
                self.traced_samples[str(o)] = v
        return outvars, outvals

    def _default_processing_rule(primitive, in_constraint, outvars):
        pass
