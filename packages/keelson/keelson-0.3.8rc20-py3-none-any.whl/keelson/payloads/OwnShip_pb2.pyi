from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SimulationShip(_message.Message):
    __slots__ = ("ship_id", "latitude_deg", "longitude_deg", "altitude_meter", "heading_deg", "rate_of_turn_degmin", "roll_deg", "pitch_deg", "longitudal_speed_ms", "vertical_speed_ms", "vertical_bow_speed_ms", "vertical_stern_speed_ms", "course_over_ground_deg", "speed_over_ground_knots", "wind_apparent_speed_ms", "wind_apparent_angle_deg", "wind_true_speed_ms", "wind_true_angle_deg")
    SHIP_ID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_DEG_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_DEG_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_METER_FIELD_NUMBER: _ClassVar[int]
    HEADING_DEG_FIELD_NUMBER: _ClassVar[int]
    RATE_OF_TURN_DEGMIN_FIELD_NUMBER: _ClassVar[int]
    ROLL_DEG_FIELD_NUMBER: _ClassVar[int]
    PITCH_DEG_FIELD_NUMBER: _ClassVar[int]
    LONGITUDAL_SPEED_MS_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_SPEED_MS_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_BOW_SPEED_MS_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_STERN_SPEED_MS_FIELD_NUMBER: _ClassVar[int]
    COURSE_OVER_GROUND_DEG_FIELD_NUMBER: _ClassVar[int]
    SPEED_OVER_GROUND_KNOTS_FIELD_NUMBER: _ClassVar[int]
    WIND_APPARENT_SPEED_MS_FIELD_NUMBER: _ClassVar[int]
    WIND_APPARENT_ANGLE_DEG_FIELD_NUMBER: _ClassVar[int]
    WIND_TRUE_SPEED_MS_FIELD_NUMBER: _ClassVar[int]
    WIND_TRUE_ANGLE_DEG_FIELD_NUMBER: _ClassVar[int]
    ship_id: int
    latitude_deg: float
    longitude_deg: float
    altitude_meter: float
    heading_deg: float
    rate_of_turn_degmin: float
    roll_deg: float
    pitch_deg: float
    longitudal_speed_ms: float
    vertical_speed_ms: float
    vertical_bow_speed_ms: float
    vertical_stern_speed_ms: float
    course_over_ground_deg: float
    speed_over_ground_knots: float
    wind_apparent_speed_ms: float
    wind_apparent_angle_deg: float
    wind_true_speed_ms: float
    wind_true_angle_deg: float
    def __init__(self, ship_id: _Optional[int] = ..., latitude_deg: _Optional[float] = ..., longitude_deg: _Optional[float] = ..., altitude_meter: _Optional[float] = ..., heading_deg: _Optional[float] = ..., rate_of_turn_degmin: _Optional[float] = ..., roll_deg: _Optional[float] = ..., pitch_deg: _Optional[float] = ..., longitudal_speed_ms: _Optional[float] = ..., vertical_speed_ms: _Optional[float] = ..., vertical_bow_speed_ms: _Optional[float] = ..., vertical_stern_speed_ms: _Optional[float] = ..., course_over_ground_deg: _Optional[float] = ..., speed_over_ground_knots: _Optional[float] = ..., wind_apparent_speed_ms: _Optional[float] = ..., wind_apparent_angle_deg: _Optional[float] = ..., wind_true_speed_ms: _Optional[float] = ..., wind_true_angle_deg: _Optional[float] = ...) -> None: ...
