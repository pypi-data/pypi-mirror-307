from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import TYPE_CHECKING, Callable, Iterable, Union

import numpy as np
import numpy.typing as npt
import pint
import spiceypy
import spiceypy.utils.callbacks
from anytree import Node, RenderTree
from attrs import define, field
from loguru import logger as log
from planetary_coverage.spice import (
    SpiceBody,
    SpiceInstrument,
    SpiceRef,
    SpiceSpacecraft,
)
from spiceypy.utils.callbacks import UDFUNB, UDFUNS

from spice_segmenter.types import TIMES_TYPES

from .decorators import declare, vectorize
from .spice_window import SpiceWindow
from .utils import et

if TYPE_CHECKING:
    from ops import Inverted

    from spice_segmenter.occultation import OccultationTypes


left_types = Union["Property", str, float, int, Enum]


def as_spice_ref(item: str | int | SpiceRef) -> SpiceRef:
    if isinstance(item, SpiceRef):
        return item
    else:
        return SpiceRef(item)


def as_pint_unit(item: str | pint.Unit) -> pint.Unit:
    if isinstance(item, pint.Unit):
        return item
    else:
        return pint.Unit(item)


class PropertyTypes(Enum):
    SCALAR = auto()
    BOOLEAN = auto()
    VECTOR = auto()
    DISCRETE = auto()


class MinMaxConditionTypes(Enum):
    LOCAL_MINIMUM = "local_minimum"
    LOCAL_MAXIMUM = "local_maximum"
    GLOBAL_MINIMUM = "global_minimum"
    GLOBAL_MAXIMUM = "global_maximum"


@define(repr=False, order=False, eq=False)
class Property(ABC):
    @abstractmethod
    def __call__(self, time: TIMES_TYPES) -> float | bool | Enum: ...

    def __str__(self) -> str:
        return self.__repr__()

    @property
    @abstractmethod
    def unit(self) -> pint.Unit | Iterable[pint.Unit]: ...

    @property
    def type(self) -> PropertyTypes:
        return PropertyTypes.SCALAR

    def as_unit(self, unit: pint.Unit | str) -> UnitAdaptor:
        return UnitAdaptor(self, unit)

    def has_unit(self) -> bool:
        return bool(str(self.unit))

    @property
    @abstractmethod
    def name(self) -> str: ...

    def compute_as_spice_function(self) -> UDFUNS:
        def as_function(time: TIMES_TYPES) -> float | bool | Enum:
            return self.__call__(time)

        # todo we are marking as_function as returing float, bool or enum, but wont work with SpiceUDFUNS. You need to use SpiceUDFUNB instead for booleans
        # while for enum wont work at all. Move these routines in the derived ScalarProperty and BooleanProperty classes please!
        return spiceypy.utils.callbacks.SpiceUDFUNS(as_function)

    def is_decreasing(self, time: TIMES_TYPES) -> bool:
        return spiceypy.uddc(self.compute_as_spice_function(), time, self.dt)  # type: ignore

    def is_decreasing_as_spice_function(self) -> UDFUNB:
        def as_function(function: Callable, time: TIMES_TYPES) -> bool:
            return self.is_decreasing(time)

        return spiceypy.utils.callbacks.SpiceUDFUNB(as_function)

    def __repr__(self) -> str:
        return f"{self.name}"

    def _handle_other_operand(self, other: left_types) -> Property:
        if isinstance(other, Property):
            return other
        else:
            return Constant.from_value(other)

    def __gt__(self, other: left_types) -> Constraint:
        return Constraint(self, self._handle_other_operand(other), ">")

    def __ge__(self, other: left_types) -> Constraint:
        log.warning(
            "Using >= operator on properties is not supported by SPICE. Using > instead."
        )
        return Constraint(self, self._handle_other_operand(other), ">")

    def __le__(self, other: left_types) -> Constraint:
        log.warning(
            "Using <= operator on properties is not supported by SPICE. Using < instead."
        )
        return Constraint(self, self._handle_other_operand(other), "<")

    def __lt__(self, other: left_types) -> Constraint:
        return Constraint(self, self._handle_other_operand(other), "<")

    def __and__(self, other: left_types) -> Constraint:
        return Constraint(self, self._handle_other_operand(other), "&")

    def __eq__(self, other: left_types) -> Constraint:  # type: ignore
        other = self._handle_other_operand(other)
        if not isinstance(other, Property):
            return NotImplemented

        return Constraint(self, other, "=")

    def __or__(self, other: left_types) -> Constraint:
        return Constraint(self, self._handle_other_operand(other), "|")

    def config(self, config: dict) -> None:
        log.debug("adding prop unit for {}", self.unit)
        config["property_unit"] = str(self.unit)
        config["property"] = self.name


@define(repr=False, order=False, eq=False)
class BooleanProperty(Property):
    @abstractmethod
    def __call__(self, time: TIMES_TYPES) -> bool:
        pass

    @property
    def type(self) -> PropertyTypes:
        return PropertyTypes.BOOLEAN

    @property
    def unit(self) -> pint.Unit:
        return pint.Unit("")

    def has_unit(self) -> bool:
        return False

    def compute_as_spice_function(self, invert: bool = False) -> UDFUNB:
        if invert:

            def as_function(udfun, time: TIMES_TYPES) -> bool:
                return ~self.__call__(time)

        else:

            def as_function(udfun, time: TIMES_TYPES) -> bool:
                return self.__call__(time)

        return spiceypy.utils.callbacks.SpiceUDFUNB(as_function)


@define(repr=False, order=False, eq=False)
class Constant(Property):
    @staticmethod
    def from_value(value):
        if isinstance(value, bool):
            return BoolConstant(value)

        elif isinstance(value, (int, float, str, Enum, pint.Quantity)):
            return ScalarConstant(value)

        else:
            raise NotImplementedError


@define(repr=False, order=False, eq=False)
class ScalarConstant(Constant):
    _value: pint.Quantity = field(converter=lambda x: pint.Quantity(x))  # type: ignore

    def __repr__(self) -> str:
        val = f"{self.value}"

        if str(self.unit) != "dimensionless":
            val += f" {self.unit}"

        return val

    @property
    def name(self) -> str:
        return "constant"

    @property
    def value(self) -> float | OccultationTypes:
        return self._value.magnitude  # type: ignore

    @property
    def unit(self) -> pint.Unit:
        return self._value.u

    @unit.setter
    def unit(self, unit: pint.Unit) -> pint.Unit:
        self._value.u = unit

    @vectorize
    def __call__(self, time: TIMES_TYPES) -> float | OccultationTypes:
        return self._value.magnitude  # type: ignore

    def config(self, config: dict) -> None:
        config.update({"reference_value": self.value})
        config["reference_value_unit"] = str(self.unit)


@define(repr=False, order=False, eq=False)
class BoolConstant(Constant):
    _value: pint.Quantity = field(converter=bool)  # type: ignore

    def __repr__(self) -> str:
        return f"{self.value}"

    @property
    def name(self) -> str:
        return "bool_constant"

    @property
    def value(self) -> float | OccultationTypes:
        return self._value

    @property
    def unit(self) -> pint.Unit:
        return pint.Unit("")

    @vectorize
    def __call__(self, time: TIMES_TYPES) -> float | OccultationTypes:
        return self._value  # type: ignore

    def config(self, config: dict) -> None:
        config.update({"reference_value": self.value})


@define(repr=False, order=False, eq=False)
class UnitAdaptor(Property):
    parent: Property
    _unit: pint.Unit = field(converter=as_pint_unit)

    @property
    def name(self) -> str:
        return self.parent.name

    @property
    def unit(self) -> pint.Unit:
        return self._unit

    @vectorize
    def __call__(self, time: TIMES_TYPES) -> float:
        return (  # type: ignore
            pint.Quantity(self.parent(time), self.parent.unit).to(self.unit).magnitude
        )

    def config(self, config: dict) -> None:
        return self.parent.config(config)


@define(repr=False, order=False, eq=False)
class TargetedProperty(Property, ABC):
    observer: SpiceInstrument | SpiceSpacecraft = field(converter=as_spice_ref)
    target: SpiceBody = field(converter=as_spice_ref)
    light_time_correction: str = field(default="NONE", kw_only=True)

    def config(self, config: dict) -> None:
        log.debug(
            "targeted property config here with instnace of {}", self.__class__.__name__
        )
        Property.config(self, config)
        config.update(
            {
                "target": self.target.name,
                "target_frame": self.target.frame.name,
                "observer": self.observer.name,
                "abcorr": self.light_time_correction,
            }
        )


@declare(name="phase_angle", unit=pint.Unit("rad"))
class PhaseAngle(TargetedProperty):
    third_body: SpiceRef = field(
        factory=lambda: as_spice_ref("SUN"), converter=as_spice_ref
    )

    def __repr__(self) -> str:
        return f"Phase Angle of {self.target} with respect to {self.third_body} as seen from {self.observer}"

    @vectorize
    def __call__(self, time: TIMES_TYPES) -> float:
        return spiceypy.phaseq(  # type: ignore
            et(time),
            self.target.name,
            self.third_body.name,
            self.observer.name,
            self.light_time_correction,
        )

    def config(self, config: dict) -> None:
        TargetedProperty.config(self, config)
        config["third_body"] = self.third_body.name
        config["property"] = self.name


@declare(name="distance", unit=pint.Unit("km"))
class Distance(TargetedProperty):
    def __repr__(self) -> str:
        return f"Distance of {self.target} from {self.observer}"

    @vectorize
    def __call__(self, time: TIMES_TYPES) -> float:
        return spiceypy.vnorm(  # type: ignore
            spiceypy.spkpos(
                self.target.name,
                et(time),
                self.observer.frame.name,
                self.light_time_correction,
                self.observer.name,
            )[0]
        )

    def config(self, config: dict) -> None:
        TargetedProperty.config(self, config)
        config["property"] = self.name


@declare(name="angular_size", unit=pint.Unit("rad"))
class AngularSize(TargetedProperty):
    def __repr__(self) -> str:
        return f"Angular size of {self.target}, seen from {self.observer}"

    @vectorize
    def __call__(self, time: TIMES_TYPES) -> float:
        d = Distance.__call__(self, time)
        return 2 * np.arctan(self.target.radius / d)  # type: ignore

    def config(self, config: dict) -> None:
        TargetedProperty.config(self, config)
        config["property"] = self.name


class ConstraintTypes(Enum):
    COMPARE_TO_CONSTANT = auto()
    COMPARE_TO_OTHER_CONSTRAINT = auto()
    MINMAX = auto()


@define(repr=False, order=False, eq=False)
class ConstraintBase(Property):
    @property
    @abstractmethod
    def left(self) -> Property | ConstraintBase: ...

    @property
    @abstractmethod
    def right(self) -> Property | ConstraintBase: ...

    @property
    @abstractmethod
    def operator(self) -> str: ...

    @property
    @abstractmethod
    def ctype(self) -> ConstraintTypes: ...

    @abstractmethod
    def __call__(self, time: TIMES_TYPES) -> bool: ...

    def config(self, config: dict) -> None:
        if self.ctype == ConstraintTypes.COMPARE_TO_OTHER_CONSTRAINT:
            log.error(
                "Cannot serialize a constraint that compares to another constraint"
            )
            raise TypeError

        self.left.config(config)
        self.right.config(config)
        config["operator"] = self.operator

    def solve(self, window: SpiceWindow, **kwargs) -> SpiceWindow:  # type: ignore
        from .constraint_solver import MasterSolver

        solver = MasterSolver(constraint=self, **kwargs)
        return solver.solve(window)

    def __invert__(self) -> Inverted:
        from spice_segmenter.ops import Inverted

        return Inverted(self)

    def tree(self) -> Node:
        """
        Returns an anynode tree with the constraints
        """
        if isinstance(self.left, ConstraintBase) and isinstance(
            self.right, ConstraintBase
        ):
            if self.operator == "|":
                name = "OR"

            elif self.operator == "&":
                name = "AND"

            else:
                raise NotImplementedError

            node = Node(name, children=[self.left.tree(), self.right.tree()])

        else:
            node = Node(self)

        return node

    def render_tree(self) -> None:
        """
        Print anytree tree
        """
        for pre, _fill, node in RenderTree(self.tree()):
            print(f"{pre}{node.name}")


@define(repr=False, order=False, eq=False)
class Constraint(ConstraintBase):
    left: Property | ConstraintBase
    right: Property | ConstraintBase
    operator: str = field(default=None)

    def __attrs_post_init__(self) -> None:
        log.debug("Checking constraint {} for compatibility", self)
        log.debug("Left type is {}", type(self.left))
        log.debug("Right type is {}", type(self.right))

        if not isinstance(self.right, Property):
            log.debug(
                "Left side of constraint {} is not a constraint or property. Assuming is a constant.",
                self,
            )
            self.right = Constant.from_value(self.right)

        if not self.left.has_unit() and not self.right.has_unit():
            log.debug("Both sides of constraint {} have no units, skipping check", self)

        elif (
            self.ctype is not ConstraintTypes.COMPARE_TO_OTHER_CONSTRAINT
            and not self.right.has_unit()
        ):
            log.warning(
                "Constraint {} compares {} to {}",
                self,
                self.left.unit,
                self.right.unit,
            )
            return

        if hasattr(self.right, "value") and isinstance(
            self.right.value, MinMaxConditionTypes
        ):
            log.debug("Right side of constraint {} is a minmax condition", self)
            return

        if isinstance(self.left.unit, Iterable):
            log.warning(
                "Constraint {} has a left side with multiple units: {}. This is not supported",
                self,
                self.left.unit,
            )
            raise NotImplementedError

        if not self.left.unit.is_compatible_with(self.right.unit):
            raise ValueError(
                f"Cannot Create a constraints between two properties with incompatible units: {self.left.unit} != {self.right.unit}"
            )

    def __repr__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"

    @property
    def type(self) -> PropertyTypes:
        return PropertyTypes.BOOLEAN

    @property
    def ctype(self) -> ConstraintTypes:
        if isinstance(self.right, Constant) or isinstance(self.left, Constant):
            return ConstraintTypes.COMPARE_TO_CONSTANT
        elif isinstance(self.left, ConstraintBase) and isinstance(
            self.left, ConstraintBase
        ):
            return ConstraintTypes.COMPARE_TO_OTHER_CONSTRAINT

        else:
            log.error("Cannot determine constraint type")
            raise NotImplementedError

    @property
    def types(self) -> tuple[type[Property], type[Property]]:
        return type(self.left), type(self.right)

    @property
    def name(self) -> str:
        return f"{self}"

    @property
    def unit(self) -> pint.Unit:
        return pint.Unit("")  # a constraint has no unit, as it returns bools

    def __call__(self, time: TIMES_TYPES) -> npt.NDArray[np.bool_]:
        right: Property | None = None

        if self.left.unit != self.right.unit:
            log.warning(
                "Comparing {} with {}. This is not recommended. Will attempt automatic conversion.",
                self.left.unit,
                self.right.unit,
            )

            right = UnitAdaptor(self.right, self.left.unit)

        else:
            right = self.right

        if (
            right is None
        ):  # this is added just to make flake8 aware we are actually using it in the eval below
            raise ValueError("Could not convert right side of constraint")

        if self.operator == "=":
            operator = "=="
        else:
            operator = self.operator

        # todo: is thera a better way to do this?
        q = "self.left(time)" + operator + "right(time)"

        return np.array(eval(q), dtype=bool)
