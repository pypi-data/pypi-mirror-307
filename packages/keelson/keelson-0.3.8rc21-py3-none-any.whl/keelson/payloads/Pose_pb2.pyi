import Quaternion_pb2 as _Quaternion_pb2
import Vector_pb2 as _Vector_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Pose(_message.Message):
    __slots__ = ("timestamp", "position", "orientation", "orientation_euler")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_EULER_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    position: _Vector_pb2.Vector3
    orientation: _Quaternion_pb2.Quaternion
    orientation_euler: EulerAngle
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., position: _Optional[_Union[_Vector_pb2.Vector3, _Mapping]] = ..., orientation: _Optional[_Union[_Quaternion_pb2.Quaternion, _Mapping]] = ..., orientation_euler: _Optional[_Union[EulerAngle, _Mapping]] = ...) -> None: ...

class EulerAngle(_message.Message):
    __slots__ = ("roll", "pitch", "yaw")
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    roll: float
    pitch: float
    yaw: float
    def __init__(self, roll: _Optional[float] = ..., pitch: _Optional[float] = ..., yaw: _Optional[float] = ...) -> None: ...
