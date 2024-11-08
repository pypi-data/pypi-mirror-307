from google.protobuf import timestamp_pb2 as _timestamp_pb2
import LocationFix_pb2 as _LocationFix_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Target(_message.Message):
    __slots__ = ("timestamp", "mmsi", "data_source", "latitude_degrees", "longitude_degrees", "position", "position_source", "speed_over_ground_knots", "course_over_ground_knots", "heading_degrees", "rate_of_turn_degrees_per_minute", "CPA_metres", "TCPA_seconds", "BCR_metres", "BCT_seconds", "bearing_north_degrees", "bearing_relative_bow_degrees", "distance_metres", "navigation_status", "json_str")
    class NavigationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDER_WAY: _ClassVar[Target.NavigationStatus]
        AT_ANCHOR: _ClassVar[Target.NavigationStatus]
        NOT_UNDER_COMMAND: _ClassVar[Target.NavigationStatus]
        RESTRICTED_MANEUVERABILITY: _ClassVar[Target.NavigationStatus]
        CONSTRAINED_BY_DRAUGHT: _ClassVar[Target.NavigationStatus]
        MOORED: _ClassVar[Target.NavigationStatus]
        AGROUND: _ClassVar[Target.NavigationStatus]
        ENGAGED_IN_FISHING: _ClassVar[Target.NavigationStatus]
        UNDER_WAY_SAILING: _ClassVar[Target.NavigationStatus]
        FUTURE_HSC: _ClassVar[Target.NavigationStatus]
        FUTURE_WIG: _ClassVar[Target.NavigationStatus]
        TOWING_ASTERN: _ClassVar[Target.NavigationStatus]
        PUSHING_AHEAD: _ClassVar[Target.NavigationStatus]
        RESERVED_FUTURE_USE: _ClassVar[Target.NavigationStatus]
        AIS_SART: _ClassVar[Target.NavigationStatus]
        UNDEFINED: _ClassVar[Target.NavigationStatus]
    UNDER_WAY: Target.NavigationStatus
    AT_ANCHOR: Target.NavigationStatus
    NOT_UNDER_COMMAND: Target.NavigationStatus
    RESTRICTED_MANEUVERABILITY: Target.NavigationStatus
    CONSTRAINED_BY_DRAUGHT: Target.NavigationStatus
    MOORED: Target.NavigationStatus
    AGROUND: Target.NavigationStatus
    ENGAGED_IN_FISHING: Target.NavigationStatus
    UNDER_WAY_SAILING: Target.NavigationStatus
    FUTURE_HSC: Target.NavigationStatus
    FUTURE_WIG: Target.NavigationStatus
    TOWING_ASTERN: Target.NavigationStatus
    PUSHING_AHEAD: Target.NavigationStatus
    RESERVED_FUTURE_USE: Target.NavigationStatus
    AIS_SART: Target.NavigationStatus
    UNDEFINED: Target.NavigationStatus
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MMSI_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_DEGREES_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_DEGREES_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    POSITION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    SPEED_OVER_GROUND_KNOTS_FIELD_NUMBER: _ClassVar[int]
    COURSE_OVER_GROUND_KNOTS_FIELD_NUMBER: _ClassVar[int]
    HEADING_DEGREES_FIELD_NUMBER: _ClassVar[int]
    RATE_OF_TURN_DEGREES_PER_MINUTE_FIELD_NUMBER: _ClassVar[int]
    CPA_METRES_FIELD_NUMBER: _ClassVar[int]
    TCPA_SECONDS_FIELD_NUMBER: _ClassVar[int]
    BCR_METRES_FIELD_NUMBER: _ClassVar[int]
    BCT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    BEARING_NORTH_DEGREES_FIELD_NUMBER: _ClassVar[int]
    BEARING_RELATIVE_BOW_DEGREES_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_METRES_FIELD_NUMBER: _ClassVar[int]
    NAVIGATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    JSON_STR_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    mmsi: int
    data_source: DataSource
    latitude_degrees: float
    longitude_degrees: float
    position: _LocationFix_pb2.LocationFix
    position_source: str
    speed_over_ground_knots: float
    course_over_ground_knots: float
    heading_degrees: float
    rate_of_turn_degrees_per_minute: float
    CPA_metres: float
    TCPA_seconds: float
    BCR_metres: float
    BCT_seconds: float
    bearing_north_degrees: float
    bearing_relative_bow_degrees: float
    distance_metres: float
    navigation_status: Target.NavigationStatus
    json_str: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., mmsi: _Optional[int] = ..., data_source: _Optional[_Union[DataSource, _Mapping]] = ..., latitude_degrees: _Optional[float] = ..., longitude_degrees: _Optional[float] = ..., position: _Optional[_Union[_LocationFix_pb2.LocationFix, _Mapping]] = ..., position_source: _Optional[str] = ..., speed_over_ground_knots: _Optional[float] = ..., course_over_ground_knots: _Optional[float] = ..., heading_degrees: _Optional[float] = ..., rate_of_turn_degrees_per_minute: _Optional[float] = ..., CPA_metres: _Optional[float] = ..., TCPA_seconds: _Optional[float] = ..., BCR_metres: _Optional[float] = ..., BCT_seconds: _Optional[float] = ..., bearing_north_degrees: _Optional[float] = ..., bearing_relative_bow_degrees: _Optional[float] = ..., distance_metres: _Optional[float] = ..., navigation_status: _Optional[_Union[Target.NavigationStatus, str]] = ..., json_str: _Optional[str] = ...) -> None: ...

class TargetDescription(_message.Message):
    __slots__ = ("timestamp", "data_source", "mmsi", "imo", "name", "callsign", "vessel_type", "platform_type", "length_over_all_meters", "width_overl_all_meters", "draft_meters", "height_above_waterline_meters", "to_bow_meters", "to_stern_meters", "to_port_meters", "to_starboard_meters", "departed", "destination", "estimated_time_of_arrival", "acctual_time_of_arrival", "estimated_time_of_departure", "acctual_time_of_departure", "json_str")
    class TargetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[TargetDescription.TargetType]
        WIG: _ClassVar[TargetDescription.TargetType]
        FISHING: _ClassVar[TargetDescription.TargetType]
        TOWING: _ClassVar[TargetDescription.TargetType]
        TOWING_LONG: _ClassVar[TargetDescription.TargetType]
        DREDGING: _ClassVar[TargetDescription.TargetType]
        DIVING: _ClassVar[TargetDescription.TargetType]
        MILITARY: _ClassVar[TargetDescription.TargetType]
        SAILING: _ClassVar[TargetDescription.TargetType]
        PLEASURE: _ClassVar[TargetDescription.TargetType]
        HSC: _ClassVar[TargetDescription.TargetType]
        PILOT: _ClassVar[TargetDescription.TargetType]
        SAR: _ClassVar[TargetDescription.TargetType]
        TUG: _ClassVar[TargetDescription.TargetType]
        PORT: _ClassVar[TargetDescription.TargetType]
        ANTI_POLLUTION: _ClassVar[TargetDescription.TargetType]
        LAW_ENFORCEMENT: _ClassVar[TargetDescription.TargetType]
        MEDICAL: _ClassVar[TargetDescription.TargetType]
        PASSENGER: _ClassVar[TargetDescription.TargetType]
        CARGO: _ClassVar[TargetDescription.TargetType]
        TANKER: _ClassVar[TargetDescription.TargetType]
        OTHER: _ClassVar[TargetDescription.TargetType]
    UNKNOWN: TargetDescription.TargetType
    WIG: TargetDescription.TargetType
    FISHING: TargetDescription.TargetType
    TOWING: TargetDescription.TargetType
    TOWING_LONG: TargetDescription.TargetType
    DREDGING: TargetDescription.TargetType
    DIVING: TargetDescription.TargetType
    MILITARY: TargetDescription.TargetType
    SAILING: TargetDescription.TargetType
    PLEASURE: TargetDescription.TargetType
    HSC: TargetDescription.TargetType
    PILOT: TargetDescription.TargetType
    SAR: TargetDescription.TargetType
    TUG: TargetDescription.TargetType
    PORT: TargetDescription.TargetType
    ANTI_POLLUTION: TargetDescription.TargetType
    LAW_ENFORCEMENT: TargetDescription.TargetType
    MEDICAL: TargetDescription.TargetType
    PASSENGER: TargetDescription.TargetType
    CARGO: TargetDescription.TargetType
    TANKER: TargetDescription.TargetType
    OTHER: TargetDescription.TargetType
    class PlatformType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SHORE: _ClassVar[TargetDescription.PlatformType]
        SEA: _ClassVar[TargetDescription.PlatformType]
    SHORE: TargetDescription.PlatformType
    SEA: TargetDescription.PlatformType
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    MMSI_FIELD_NUMBER: _ClassVar[int]
    IMO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    VESSEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_TYPE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_OVER_ALL_METERS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_OVERL_ALL_METERS_FIELD_NUMBER: _ClassVar[int]
    DRAFT_METERS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_ABOVE_WATERLINE_METERS_FIELD_NUMBER: _ClassVar[int]
    TO_BOW_METERS_FIELD_NUMBER: _ClassVar[int]
    TO_STERN_METERS_FIELD_NUMBER: _ClassVar[int]
    TO_PORT_METERS_FIELD_NUMBER: _ClassVar[int]
    TO_STARBOARD_METERS_FIELD_NUMBER: _ClassVar[int]
    DEPARTED_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_TIME_OF_ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    ACCTUAL_TIME_OF_ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_TIME_OF_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    ACCTUAL_TIME_OF_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    JSON_STR_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    data_source: DataSource
    mmsi: int
    imo: int
    name: str
    callsign: str
    vessel_type: TargetDescription.TargetType
    platform_type: TargetDescription.PlatformType
    length_over_all_meters: float
    width_overl_all_meters: float
    draft_meters: float
    height_above_waterline_meters: float
    to_bow_meters: float
    to_stern_meters: float
    to_port_meters: float
    to_starboard_meters: float
    departed: str
    destination: str
    estimated_time_of_arrival: str
    acctual_time_of_arrival: str
    estimated_time_of_departure: str
    acctual_time_of_departure: str
    json_str: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data_source: _Optional[_Union[DataSource, _Mapping]] = ..., mmsi: _Optional[int] = ..., imo: _Optional[int] = ..., name: _Optional[str] = ..., callsign: _Optional[str] = ..., vessel_type: _Optional[_Union[TargetDescription.TargetType, str]] = ..., platform_type: _Optional[_Union[TargetDescription.PlatformType, str]] = ..., length_over_all_meters: _Optional[float] = ..., width_overl_all_meters: _Optional[float] = ..., draft_meters: _Optional[float] = ..., height_above_waterline_meters: _Optional[float] = ..., to_bow_meters: _Optional[float] = ..., to_stern_meters: _Optional[float] = ..., to_port_meters: _Optional[float] = ..., to_starboard_meters: _Optional[float] = ..., departed: _Optional[str] = ..., destination: _Optional[str] = ..., estimated_time_of_arrival: _Optional[str] = ..., acctual_time_of_arrival: _Optional[str] = ..., estimated_time_of_departure: _Optional[str] = ..., acctual_time_of_departure: _Optional[str] = ..., json_str: _Optional[str] = ...) -> None: ...

class DataSource(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AIS_RADIO: _ClassVar[DataSource.Source]
        AIS_PROVIDER: _ClassVar[DataSource.Source]
        RADAR_MARINE: _ClassVar[DataSource.Source]
        RADAR_ROAD: _ClassVar[DataSource.Source]
        LIDAR: _ClassVar[DataSource.Source]
        CAMERA_RBG: _ClassVar[DataSource.Source]
        CAMERA_MONO: _ClassVar[DataSource.Source]
        CAMERA_IR: _ClassVar[DataSource.Source]
    AIS_RADIO: DataSource.Source
    AIS_PROVIDER: DataSource.Source
    RADAR_MARINE: DataSource.Source
    RADAR_ROAD: DataSource.Source
    LIDAR: DataSource.Source
    CAMERA_RBG: DataSource.Source
    CAMERA_MONO: DataSource.Source
    CAMERA_IR: DataSource.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: _containers.RepeatedScalarFieldContainer[DataSource.Source]
    def __init__(self, source: _Optional[_Iterable[_Union[DataSource.Source, str]]] = ...) -> None: ...
