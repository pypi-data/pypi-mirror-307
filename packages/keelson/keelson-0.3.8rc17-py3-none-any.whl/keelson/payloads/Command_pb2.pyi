from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Command(_message.Message):
    __slots__ = ("timestamp", "value_set", "value_actual", "mode_set", "mode_actual", "config_id", "config_value", "other_json")
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RUNNIG: _ClassVar[Command.Mode]
        STANDBY: _ClassVar[Command.Mode]
        ERROR: _ClassVar[Command.Mode]
    RUNNIG: Command.Mode
    STANDBY: Command.Mode
    ERROR: Command.Mode
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_SET_FIELD_NUMBER: _ClassVar[int]
    VALUE_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    MODE_SET_FIELD_NUMBER: _ClassVar[int]
    MODE_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VALUE_FIELD_NUMBER: _ClassVar[int]
    OTHER_JSON_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value_set: float
    value_actual: float
    mode_set: Command.Mode
    mode_actual: Command.Mode
    config_id: str
    config_value: str
    other_json: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value_set: _Optional[float] = ..., value_actual: _Optional[float] = ..., mode_set: _Optional[_Union[Command.Mode, str]] = ..., mode_actual: _Optional[_Union[Command.Mode, str]] = ..., config_id: _Optional[str] = ..., config_value: _Optional[str] = ..., other_json: _Optional[str] = ...) -> None: ...

class CommandThruster(_message.Message):
    __slots__ = ("timestamp", "set", "actual", "mode")
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RUNNIG: _ClassVar[CommandThruster.Mode]
        STANDBY: _ClassVar[CommandThruster.Mode]
        ERROR: _ClassVar[CommandThruster.Mode]
    RUNNIG: CommandThruster.Mode
    STANDBY: CommandThruster.Mode
    ERROR: CommandThruster.Mode
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    set: float
    actual: float
    mode: CommandThruster.Mode
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., set: _Optional[float] = ..., actual: _Optional[float] = ..., mode: _Optional[_Union[CommandThruster.Mode, str]] = ...) -> None: ...

class CommandCameraXY(_message.Message):
    __slots__ = ("timestamp", "set_x_degrees", "set_y_degrees", "move_x_degrees", "move_y_degrees", "actual_x_degrees", "actual_y_degrees")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SET_X_DEGREES_FIELD_NUMBER: _ClassVar[int]
    SET_Y_DEGREES_FIELD_NUMBER: _ClassVar[int]
    MOVE_X_DEGREES_FIELD_NUMBER: _ClassVar[int]
    MOVE_Y_DEGREES_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_X_DEGREES_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_Y_DEGREES_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    set_x_degrees: float
    set_y_degrees: float
    move_x_degrees: float
    move_y_degrees: float
    actual_x_degrees: float
    actual_y_degrees: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., set_x_degrees: _Optional[float] = ..., set_y_degrees: _Optional[float] = ..., move_x_degrees: _Optional[float] = ..., move_y_degrees: _Optional[float] = ..., actual_x_degrees: _Optional[float] = ..., actual_y_degrees: _Optional[float] = ...) -> None: ...
