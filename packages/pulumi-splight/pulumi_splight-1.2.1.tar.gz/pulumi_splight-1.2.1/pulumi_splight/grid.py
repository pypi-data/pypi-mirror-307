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
from ._inputs import *

__all__ = ['GridArgs', 'Grid']

@pulumi.input_type
class GridArgs:
    def __init__(__self__, *,
                 custom_timezone: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 geometry: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['GridTagArgs']]]] = None):
        """
        The set of arguments for constructing a Grid resource.
        :param pulumi.Input[str] custom_timezone: timezone that overrides location-based timezone of the resource
        :param pulumi.Input[str] description: description of the resource
        :param pulumi.Input[str] geometry: geo position and shape of the resource
        :param pulumi.Input[str] name: name of the resource
        :param pulumi.Input[Sequence[pulumi.Input['GridTagArgs']]] tags: tags of the resource
        """
        if custom_timezone is not None:
            pulumi.set(__self__, "custom_timezone", custom_timezone)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if geometry is not None:
            pulumi.set(__self__, "geometry", geometry)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="customTimezone")
    def custom_timezone(self) -> Optional[pulumi.Input[str]]:
        """
        timezone that overrides location-based timezone of the resource
        """
        return pulumi.get(self, "custom_timezone")

    @custom_timezone.setter
    def custom_timezone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_timezone", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        description of the resource
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def geometry(self) -> Optional[pulumi.Input[str]]:
        """
        geo position and shape of the resource
        """
        return pulumi.get(self, "geometry")

    @geometry.setter
    def geometry(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "geometry", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        name of the resource
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GridTagArgs']]]]:
        """
        tags of the resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GridTagArgs']]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _GridState:
    def __init__(__self__, *,
                 custom_timezone: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 geometry: Optional[pulumi.Input[str]] = None,
                 kinds: Optional[pulumi.Input[Sequence[pulumi.Input['GridKindArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['GridTagArgs']]]] = None):
        """
        Input properties used for looking up and filtering Grid resources.
        :param pulumi.Input[str] custom_timezone: timezone that overrides location-based timezone of the resource
        :param pulumi.Input[str] description: description of the resource
        :param pulumi.Input[str] geometry: geo position and shape of the resource
        :param pulumi.Input[Sequence[pulumi.Input['GridKindArgs']]] kinds: kind of the resource
        :param pulumi.Input[str] name: name of the resource
        :param pulumi.Input[Sequence[pulumi.Input['GridTagArgs']]] tags: tags of the resource
        """
        if custom_timezone is not None:
            pulumi.set(__self__, "custom_timezone", custom_timezone)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if geometry is not None:
            pulumi.set(__self__, "geometry", geometry)
        if kinds is not None:
            pulumi.set(__self__, "kinds", kinds)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="customTimezone")
    def custom_timezone(self) -> Optional[pulumi.Input[str]]:
        """
        timezone that overrides location-based timezone of the resource
        """
        return pulumi.get(self, "custom_timezone")

    @custom_timezone.setter
    def custom_timezone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_timezone", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        description of the resource
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def geometry(self) -> Optional[pulumi.Input[str]]:
        """
        geo position and shape of the resource
        """
        return pulumi.get(self, "geometry")

    @geometry.setter
    def geometry(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "geometry", value)

    @property
    @pulumi.getter
    def kinds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GridKindArgs']]]]:
        """
        kind of the resource
        """
        return pulumi.get(self, "kinds")

    @kinds.setter
    def kinds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GridKindArgs']]]]):
        pulumi.set(self, "kinds", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        name of the resource
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GridTagArgs']]]]:
        """
        tags of the resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GridTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Grid(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_timezone: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 geometry: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GridTagArgs', 'GridTagArgsDict']]]]] = None,
                 __props__=None):
        """
        ## Example Usage

        ## Import

        ```sh
        $ pulumi import splight:index/grid:Grid [options] splight_grid.<name> <grid_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] custom_timezone: timezone that overrides location-based timezone of the resource
        :param pulumi.Input[str] description: description of the resource
        :param pulumi.Input[str] geometry: geo position and shape of the resource
        :param pulumi.Input[str] name: name of the resource
        :param pulumi.Input[Sequence[pulumi.Input[Union['GridTagArgs', 'GridTagArgsDict']]]] tags: tags of the resource
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[GridArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ## Import

        ```sh
        $ pulumi import splight:index/grid:Grid [options] splight_grid.<name> <grid_id>
        ```

        :param str resource_name: The name of the resource.
        :param GridArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GridArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_timezone: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 geometry: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GridTagArgs', 'GridTagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GridArgs.__new__(GridArgs)

            __props__.__dict__["custom_timezone"] = custom_timezone
            __props__.__dict__["description"] = description
            __props__.__dict__["geometry"] = geometry
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["kinds"] = None
        super(Grid, __self__).__init__(
            'splight:index/grid:Grid',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            custom_timezone: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            geometry: Optional[pulumi.Input[str]] = None,
            kinds: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GridKindArgs', 'GridKindArgsDict']]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GridTagArgs', 'GridTagArgsDict']]]]] = None) -> 'Grid':
        """
        Get an existing Grid resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] custom_timezone: timezone that overrides location-based timezone of the resource
        :param pulumi.Input[str] description: description of the resource
        :param pulumi.Input[str] geometry: geo position and shape of the resource
        :param pulumi.Input[Sequence[pulumi.Input[Union['GridKindArgs', 'GridKindArgsDict']]]] kinds: kind of the resource
        :param pulumi.Input[str] name: name of the resource
        :param pulumi.Input[Sequence[pulumi.Input[Union['GridTagArgs', 'GridTagArgsDict']]]] tags: tags of the resource
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GridState.__new__(_GridState)

        __props__.__dict__["custom_timezone"] = custom_timezone
        __props__.__dict__["description"] = description
        __props__.__dict__["geometry"] = geometry
        __props__.__dict__["kinds"] = kinds
        __props__.__dict__["name"] = name
        __props__.__dict__["tags"] = tags
        return Grid(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="customTimezone")
    def custom_timezone(self) -> pulumi.Output[Optional[str]]:
        """
        timezone that overrides location-based timezone of the resource
        """
        return pulumi.get(self, "custom_timezone")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        description of the resource
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def geometry(self) -> pulumi.Output[Optional[str]]:
        """
        geo position and shape of the resource
        """
        return pulumi.get(self, "geometry")

    @property
    @pulumi.getter
    def kinds(self) -> pulumi.Output[Sequence['outputs.GridKind']]:
        """
        kind of the resource
        """
        return pulumi.get(self, "kinds")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.GridTag']]]:
        """
        tags of the resource
        """
        return pulumi.get(self, "tags")

