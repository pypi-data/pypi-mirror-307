from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SailControlState(_message.Message):
    __slots__ = ("sheeting_mode", "coupled_steering_mode", "variable_thrust_mode", "variable_thrust_set_pct", "variable_thrust_actual_pct")
    SHEETING_MODE_FIELD_NUMBER: _ClassVar[int]
    COUPLED_STEERING_MODE_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_THRUST_MODE_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_THRUST_SET_PCT_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_THRUST_ACTUAL_PCT_FIELD_NUMBER: _ClassVar[int]
    sheeting_mode: int
    coupled_steering_mode: int
    variable_thrust_mode: int
    variable_thrust_set_pct: float
    variable_thrust_actual_pct: float
    def __init__(self, sheeting_mode: _Optional[int] = ..., coupled_steering_mode: _Optional[int] = ..., variable_thrust_mode: _Optional[int] = ..., variable_thrust_set_pct: _Optional[float] = ..., variable_thrust_actual_pct: _Optional[float] = ...) -> None: ...
