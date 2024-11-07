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

__all__ = ['ActionArgs', 'Action']

@pulumi.input_type
class ActionArgs:
    def __init__(__self__, *,
                 asset: pulumi.Input['ActionAssetArgs'],
                 setpoints: pulumi.Input[Sequence[pulumi.Input['ActionSetpointArgs']]],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Action resource.
        :param pulumi.Input['ActionAssetArgs'] asset: target asset of the setpoint
        :param pulumi.Input[Sequence[pulumi.Input['ActionSetpointArgs']]] setpoints: action setpoints
        :param pulumi.Input[str] name: the name of the action to be created
        """
        pulumi.set(__self__, "asset", asset)
        pulumi.set(__self__, "setpoints", setpoints)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def asset(self) -> pulumi.Input['ActionAssetArgs']:
        """
        target asset of the setpoint
        """
        return pulumi.get(self, "asset")

    @asset.setter
    def asset(self, value: pulumi.Input['ActionAssetArgs']):
        pulumi.set(self, "asset", value)

    @property
    @pulumi.getter
    def setpoints(self) -> pulumi.Input[Sequence[pulumi.Input['ActionSetpointArgs']]]:
        """
        action setpoints
        """
        return pulumi.get(self, "setpoints")

    @setpoints.setter
    def setpoints(self, value: pulumi.Input[Sequence[pulumi.Input['ActionSetpointArgs']]]):
        pulumi.set(self, "setpoints", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        the name of the action to be created
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ActionState:
    def __init__(__self__, *,
                 asset: Optional[pulumi.Input['ActionAssetArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 setpoints: Optional[pulumi.Input[Sequence[pulumi.Input['ActionSetpointArgs']]]] = None):
        """
        Input properties used for looking up and filtering Action resources.
        :param pulumi.Input['ActionAssetArgs'] asset: target asset of the setpoint
        :param pulumi.Input[str] name: the name of the action to be created
        :param pulumi.Input[Sequence[pulumi.Input['ActionSetpointArgs']]] setpoints: action setpoints
        """
        if asset is not None:
            pulumi.set(__self__, "asset", asset)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if setpoints is not None:
            pulumi.set(__self__, "setpoints", setpoints)

    @property
    @pulumi.getter
    def asset(self) -> Optional[pulumi.Input['ActionAssetArgs']]:
        """
        target asset of the setpoint
        """
        return pulumi.get(self, "asset")

    @asset.setter
    def asset(self, value: Optional[pulumi.Input['ActionAssetArgs']]):
        pulumi.set(self, "asset", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        the name of the action to be created
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def setpoints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ActionSetpointArgs']]]]:
        """
        action setpoints
        """
        return pulumi.get(self, "setpoints")

    @setpoints.setter
    def setpoints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ActionSetpointArgs']]]]):
        pulumi.set(self, "setpoints", value)


class Action(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 asset: Optional[pulumi.Input[Union['ActionAssetArgs', 'ActionAssetArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 setpoints: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ActionSetpointArgs', 'ActionSetpointArgsDict']]]]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_splight as splight

        my_asset = splight.Asset("myAsset",
            description="My Asset Description",
            geometry=json.dumps({
                "type": "GeometryCollection",
                "geometries": [{
                    "type": "Point",
                    "coordinates": [
                        0,
                        0,
                    ],
                }],
            }))
        my_attribute = splight.AssetAttribute("myAttribute",
            type="Number",
            unit="meters",
            asset=my_asset.id)
        my_action = splight.Action("myAction",
            asset={
                "id": my_asset.id,
                "name": my_asset.name,
            },
            setpoints=[{
                "value": json.dumps(1),
                "attribute": {
                    "id": my_attribute.id,
                    "name": my_attribute.name,
                },
            }])
        ```

        ## Import

        ```sh
        $ pulumi import splight:index/action:Action [options] splight_action.<name> <action_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['ActionAssetArgs', 'ActionAssetArgsDict']] asset: target asset of the setpoint
        :param pulumi.Input[str] name: the name of the action to be created
        :param pulumi.Input[Sequence[pulumi.Input[Union['ActionSetpointArgs', 'ActionSetpointArgsDict']]]] setpoints: action setpoints
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ActionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_splight as splight

        my_asset = splight.Asset("myAsset",
            description="My Asset Description",
            geometry=json.dumps({
                "type": "GeometryCollection",
                "geometries": [{
                    "type": "Point",
                    "coordinates": [
                        0,
                        0,
                    ],
                }],
            }))
        my_attribute = splight.AssetAttribute("myAttribute",
            type="Number",
            unit="meters",
            asset=my_asset.id)
        my_action = splight.Action("myAction",
            asset={
                "id": my_asset.id,
                "name": my_asset.name,
            },
            setpoints=[{
                "value": json.dumps(1),
                "attribute": {
                    "id": my_attribute.id,
                    "name": my_attribute.name,
                },
            }])
        ```

        ## Import

        ```sh
        $ pulumi import splight:index/action:Action [options] splight_action.<name> <action_id>
        ```

        :param str resource_name: The name of the resource.
        :param ActionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ActionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 asset: Optional[pulumi.Input[Union['ActionAssetArgs', 'ActionAssetArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 setpoints: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ActionSetpointArgs', 'ActionSetpointArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ActionArgs.__new__(ActionArgs)

            if asset is None and not opts.urn:
                raise TypeError("Missing required property 'asset'")
            __props__.__dict__["asset"] = asset
            __props__.__dict__["name"] = name
            if setpoints is None and not opts.urn:
                raise TypeError("Missing required property 'setpoints'")
            __props__.__dict__["setpoints"] = setpoints
        super(Action, __self__).__init__(
            'splight:index/action:Action',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            asset: Optional[pulumi.Input[Union['ActionAssetArgs', 'ActionAssetArgsDict']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            setpoints: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ActionSetpointArgs', 'ActionSetpointArgsDict']]]]] = None) -> 'Action':
        """
        Get an existing Action resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['ActionAssetArgs', 'ActionAssetArgsDict']] asset: target asset of the setpoint
        :param pulumi.Input[str] name: the name of the action to be created
        :param pulumi.Input[Sequence[pulumi.Input[Union['ActionSetpointArgs', 'ActionSetpointArgsDict']]]] setpoints: action setpoints
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ActionState.__new__(_ActionState)

        __props__.__dict__["asset"] = asset
        __props__.__dict__["name"] = name
        __props__.__dict__["setpoints"] = setpoints
        return Action(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def asset(self) -> pulumi.Output['outputs.ActionAsset']:
        """
        target asset of the setpoint
        """
        return pulumi.get(self, "asset")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        the name of the action to be created
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def setpoints(self) -> pulumi.Output[Sequence['outputs.ActionSetpoint']]:
        """
        action setpoints
        """
        return pulumi.get(self, "setpoints")

