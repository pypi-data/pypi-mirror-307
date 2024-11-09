from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StringOrFloatValue(_message.Message):
    __slots__ = ("string_value", "float_value")
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    string_value: str
    float_value: float
    def __init__(self, string_value: _Optional[str] = ..., float_value: _Optional[float] = ...) -> None: ...

class KeyValuePair(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: StringOrFloatValue
    def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[StringOrFloatValue, _Mapping]] = ...) -> None: ...

class KeyValuePairSet(_message.Message):
    __slots__ = ("key_values",)
    KEY_VALUES_FIELD_NUMBER: _ClassVar[int]
    key_values: _containers.RepeatedCompositeFieldContainer[KeyValuePair]
    def __init__(self, key_values: _Optional[_Iterable[_Union[KeyValuePair, _Mapping]]] = ...) -> None: ...

class Vector(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, value: _Optional[_Iterable[float]] = ...) -> None: ...

class VectorSet(_message.Message):
    __slots__ = ("vectors", "model")
    VECTORS_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    vectors: _containers.RepeatedCompositeFieldContainer[Vector]
    model: str
    def __init__(self, vectors: _Optional[_Iterable[_Union[Vector, _Mapping]]] = ..., model: _Optional[str] = ...) -> None: ...

class VectorizeRequestSet(_message.Message):
    __slots__ = ("key_value_pairs", "setting")
    KEY_VALUE_PAIRS_FIELD_NUMBER: _ClassVar[int]
    SETTING_FIELD_NUMBER: _ClassVar[int]
    key_value_pairs: KeyValuePairSet
    setting: Setting
    def __init__(self, key_value_pairs: _Optional[_Union[KeyValuePairSet, _Mapping]] = ..., setting: _Optional[_Union[Setting, _Mapping]] = ...) -> None: ...

class VectorizeRequest(_message.Message):
    __slots__ = ("key_value_pairs", "setting")
    KEY_VALUE_PAIRS_FIELD_NUMBER: _ClassVar[int]
    SETTING_FIELD_NUMBER: _ClassVar[int]
    key_value_pairs: KeyValuePair
    setting: Setting
    def __init__(self, key_value_pairs: _Optional[_Union[KeyValuePair, _Mapping]] = ..., setting: _Optional[_Union[Setting, _Mapping]] = ...) -> None: ...

class Setting(_message.Message):
    __slots__ = ("key_coefficient", "string_val_coefficient", "float_val_coefficient")
    KEY_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    STRING_VAL_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VAL_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    key_coefficient: float
    string_val_coefficient: float
    float_val_coefficient: float
    def __init__(self, key_coefficient: _Optional[float] = ..., string_val_coefficient: _Optional[float] = ..., float_val_coefficient: _Optional[float] = ...) -> None: ...
