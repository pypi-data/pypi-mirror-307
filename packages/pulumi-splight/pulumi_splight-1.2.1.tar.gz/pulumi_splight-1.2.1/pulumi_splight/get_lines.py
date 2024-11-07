# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from . import _utilities
from . import outputs

__all__ = [
    'GetLinesResult',
    'AwaitableGetLinesResult',
    'get_lines',
    'get_lines_output',
]

@pulumi.output_type
class GetLinesResult:
    """
    A collection of values returned by getLines.
    """
    def __init__(__self__, id=None, tags=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def tags(self) -> Sequence['outputs.GetLinesTagResult']:
        return pulumi.get(self, "tags")


class AwaitableGetLinesResult(GetLinesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLinesResult(
            id=self.id,
            tags=self.tags)


def get_lines(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLinesResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_splight as splight

    lines = splight.get_lines()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('splight:index/getLines:getLines', __args__, opts=opts, typ=GetLinesResult).value

    return AwaitableGetLinesResult(
        id=pulumi.get(__ret__, 'id'),
        tags=pulumi.get(__ret__, 'tags'))
def get_lines_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLinesResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_splight as splight

    lines = splight.get_lines()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('splight:index/getLines:getLines', __args__, opts=opts, typ=GetLinesResult)
    return __ret__.apply(lambda __response__: GetLinesResult(
        id=pulumi.get(__response__, 'id'),
        tags=pulumi.get(__response__, 'tags')))
