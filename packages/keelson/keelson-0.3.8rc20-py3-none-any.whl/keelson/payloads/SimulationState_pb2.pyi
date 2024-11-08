from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SimulationState(_message.Message):
    __slots__ = ("simulation_time", "simulation_state", "simulation_name", "simulation_id", "simulation_time_str")
    SIMULATION_TIME_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_STATE_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_NAME_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_ID_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_TIME_STR_FIELD_NUMBER: _ClassVar[int]
    simulation_time: _timestamp_pb2.Timestamp
    simulation_state: str
    simulation_name: str
    simulation_id: str
    simulation_time_str: str
    def __init__(self, simulation_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., simulation_state: _Optional[str] = ..., simulation_name: _Optional[str] = ..., simulation_id: _Optional[str] = ..., simulation_time_str: _Optional[str] = ...) -> None: ...
