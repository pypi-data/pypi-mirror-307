from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *


@jsii.data_type(
    jsii_type="@gammarers/aws-resource-naming.ResourceNaming.DefaultNaming",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class DefaultNaming:
    def __init__(self, *, type: "NamingType") -> None:
        '''
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6fe688f7026700ff451ff908b5358d3e7292c007575b3de8dfbdfcbadcb332f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> "NamingType":
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("NamingType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DefaultNaming(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@gammarers/aws-resource-naming.ResourceNaming.NamingType")
class NamingType(enum.Enum):
    NO = "NO"
    DEFAULT = "DEFAULT"
    CUSTOM = "CUSTOM"


@jsii.data_type(
    jsii_type="@gammarers/aws-resource-naming.ResourceNaming.NoNaming",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class NoNaming:
    def __init__(self, *, type: NamingType) -> None:
        '''
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cd6ae03c739c87909e65c512e87d9dfda9d588964f28553f04daaae884fb51)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> NamingType:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(NamingType, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NoNaming(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DefaultNaming",
    "NamingType",
    "NoNaming",
]

publication.publish()

def _typecheckingstub__a6fe688f7026700ff451ff908b5358d3e7292c007575b3de8dfbdfcbadcb332f(
    *,
    type: NamingType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cd6ae03c739c87909e65c512e87d9dfda9d588964f28553f04daaae884fb51(
    *,
    type: NamingType,
) -> None:
    """Type checking stubs"""
    pass
