from typing import Dict, List, Set, Union

import jax.numpy as jnp
from pydantic import validator

from openff.system.exceptions import InvalidExpressionError
from openff.system.types import DefaultModel, FloatQuantity


class Potential(DefaultModel):
    """Base class for storing applied parameters"""

    # ... Dict[str, FloatQuantity] = dict()
    parameters: Dict = dict()

    @validator("parameters")
    def validate_parameters(cls, v):
        for key, val in v.items():
            v[key] = FloatQuantity.validate_type(val)
        return v


class PotentialHandler(DefaultModel):
    """Base class for storing parametrized force field data"""

    name: str
    expression: str
    independent_variables: Union[str, Set[str]]
    slot_map: Dict[str, str] = dict()
    potentials: Dict[str, Potential] = dict()

    # Pydantic silently casts some types (int, float, Decimal) to str
    # in models that expect str; this may be updates, see #1098
    @validator("expression", pre=True)
    def is_valid_expr(cls, val):
        if isinstance(val, str):
            return val
        else:
            raise InvalidExpressionError

    def store_matches(self):
        raise NotImplementedError

    def store_potentials(self):
        raise NotImplementedError

    def get_force_field_parameters(self):
        params: list = list()
        for potential in self.potentials.values():
            row = [val for val in potential.parameters.values()]  # val.magnitude
            params.append(row)

        return jnp.array(params)

    def get_system_parameters(self, p=None):
        if p is None:
            p = self.get_force_field_parameters()
        mapping = self.get_mapping()
        q: List = list()

        for key in self.slot_map.keys():
            q.append(p[mapping[self.slot_map[key]]])

        return jnp.array(q)

    def get_mapping(self) -> Dict:
        mapping: Dict = dict()
        for idx, key in enumerate(self.potentials.keys()):
            for p in self.slot_map.values():
                if key == p:
                    mapping.update({key: idx})

        return mapping

    def parametrize(self, p=None):
        if p is None:
            p = self.get_force_field_parameters()

        return self.get_system_parameters(p=p)

    def parametrize_partial(self):
        from functools import partial

        return partial(
            self.parametrize,
            mapping=self.get_mapping(),
        )

    def get_param_matrix(self):
        from functools import partial

        import jax

        p = self.get_force_field_parameters()

        parametrize_partial = partial(
            self.parametrize,
        )

        jac_parametrize = jax.jacfwd(parametrize_partial)
        jac_res = jac_parametrize(p)

        return jac_res.reshape(-1, p.flatten().shape[0])
