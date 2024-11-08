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
    jsii_type="@gammarers/aws-resource-naming.ResourceNaming.NamingOptions",
    jsii_struct_bases=[],
    name_mapping={"naming": "naming"},
)
class NamingOptions:
    def __init__(
        self,
        *,
        naming: typing.Union["NamingType", typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        '''
        :param naming: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a21456f1875723092b0702d4fd53b02fa06b53aff36a896a2909135d5c42f6)
            check_type(argname="argument naming", value=naming, expected_type=type_hints["naming"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "naming": naming,
        }

    @builtins.property
    def naming(
        self,
    ) -> typing.Union["NamingType", typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("naming")
        assert result is not None, "Required property 'naming' is missing"
        return typing.cast(typing.Union["NamingType", typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@gammarers/aws-resource-naming.ResourceNaming.NamingType")
class NamingType(enum.Enum):
    DEFAULT = "DEFAULT"
    NONE = "NONE"


__all__ = [
    "NamingOptions",
    "NamingType",
]

publication.publish()

def _typecheckingstub__74a21456f1875723092b0702d4fd53b02fa06b53aff36a896a2909135d5c42f6(
    *,
    naming: typing.Union[NamingType, typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass
