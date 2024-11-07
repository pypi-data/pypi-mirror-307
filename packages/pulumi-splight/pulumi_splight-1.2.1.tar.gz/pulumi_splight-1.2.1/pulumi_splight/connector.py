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

__all__ = ['ConnectorArgs', 'Connector']

@pulumi.input_type
class ConnectorArgs:
    def __init__(__self__, *,
                 version: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 inputs: Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorInputArgs']]]] = None,
                 log_level: Optional[pulumi.Input[str]] = None,
                 machine_instance_size: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 node: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorTagArgs']]]] = None):
        """
        The set of arguments for constructing a Connector resource.
        :param pulumi.Input[str] version: [NAME-VERSION] the version of the hub connector
        :param pulumi.Input[str] description: optional description to add details of the resource
        :param pulumi.Input[Sequence[pulumi.Input['ConnectorInputArgs']]] inputs: static config parameters of the routine
        :param pulumi.Input[str] log_level: log level of the connector
        :param pulumi.Input[str] machine_instance_size: instance size
        :param pulumi.Input[str] name: the name of the connector to be created
        :param pulumi.Input[str] node: id of the compute node where the connector runs
        :param pulumi.Input[str] restart_policy: restart policy of the connector
        :param pulumi.Input[Sequence[pulumi.Input['ConnectorTagArgs']]] tags: tags of the resource
        """
        pulumi.set(__self__, "version", version)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if inputs is not None:
            pulumi.set(__self__, "inputs", inputs)
        if log_level is not None:
            pulumi.set(__self__, "log_level", log_level)
        if machine_instance_size is not None:
            pulumi.set(__self__, "machine_instance_size", machine_instance_size)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if node is not None:
            pulumi.set(__self__, "node", node)
        if restart_policy is not None:
            pulumi.set(__self__, "restart_policy", restart_policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[str]:
        """
        [NAME-VERSION] the version of the hub connector
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: pulumi.Input[str]):
        pulumi.set(self, "version", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        optional description to add details of the resource
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def inputs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorInputArgs']]]]:
        """
        static config parameters of the routine
        """
        return pulumi.get(self, "inputs")

    @inputs.setter
    def inputs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorInputArgs']]]]):
        pulumi.set(self, "inputs", value)

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional[pulumi.Input[str]]:
        """
        log level of the connector
        """
        return pulumi.get(self, "log_level")

    @log_level.setter
    def log_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_level", value)

    @property
    @pulumi.getter(name="machineInstanceSize")
    def machine_instance_size(self) -> Optional[pulumi.Input[str]]:
        """
        instance size
        """
        return pulumi.get(self, "machine_instance_size")

    @machine_instance_size.setter
    def machine_instance_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "machine_instance_size", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        the name of the connector to be created
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def node(self) -> Optional[pulumi.Input[str]]:
        """
        id of the compute node where the connector runs
        """
        return pulumi.get(self, "node")

    @node.setter
    def node(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "node", value)

    @property
    @pulumi.getter(name="restartPolicy")
    def restart_policy(self) -> Optional[pulumi.Input[str]]:
        """
        restart policy of the connector
        """
        return pulumi.get(self, "restart_policy")

    @restart_policy.setter
    def restart_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "restart_policy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorTagArgs']]]]:
        """
        tags of the resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorTagArgs']]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ConnectorState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 inputs: Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorInputArgs']]]] = None,
                 log_level: Optional[pulumi.Input[str]] = None,
                 machine_instance_size: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 node: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorTagArgs']]]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Connector resources.
        :param pulumi.Input[str] description: optional description to add details of the resource
        :param pulumi.Input[Sequence[pulumi.Input['ConnectorInputArgs']]] inputs: static config parameters of the routine
        :param pulumi.Input[str] log_level: log level of the connector
        :param pulumi.Input[str] machine_instance_size: instance size
        :param pulumi.Input[str] name: the name of the connector to be created
        :param pulumi.Input[str] node: id of the compute node where the connector runs
        :param pulumi.Input[str] restart_policy: restart policy of the connector
        :param pulumi.Input[Sequence[pulumi.Input['ConnectorTagArgs']]] tags: tags of the resource
        :param pulumi.Input[str] version: [NAME-VERSION] the version of the hub connector
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if inputs is not None:
            pulumi.set(__self__, "inputs", inputs)
        if log_level is not None:
            pulumi.set(__self__, "log_level", log_level)
        if machine_instance_size is not None:
            pulumi.set(__self__, "machine_instance_size", machine_instance_size)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if node is not None:
            pulumi.set(__self__, "node", node)
        if restart_policy is not None:
            pulumi.set(__self__, "restart_policy", restart_policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        optional description to add details of the resource
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def inputs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorInputArgs']]]]:
        """
        static config parameters of the routine
        """
        return pulumi.get(self, "inputs")

    @inputs.setter
    def inputs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorInputArgs']]]]):
        pulumi.set(self, "inputs", value)

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional[pulumi.Input[str]]:
        """
        log level of the connector
        """
        return pulumi.get(self, "log_level")

    @log_level.setter
    def log_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_level", value)

    @property
    @pulumi.getter(name="machineInstanceSize")
    def machine_instance_size(self) -> Optional[pulumi.Input[str]]:
        """
        instance size
        """
        return pulumi.get(self, "machine_instance_size")

    @machine_instance_size.setter
    def machine_instance_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "machine_instance_size", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        the name of the connector to be created
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def node(self) -> Optional[pulumi.Input[str]]:
        """
        id of the compute node where the connector runs
        """
        return pulumi.get(self, "node")

    @node.setter
    def node(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "node", value)

    @property
    @pulumi.getter(name="restartPolicy")
    def restart_policy(self) -> Optional[pulumi.Input[str]]:
        """
        restart policy of the connector
        """
        return pulumi.get(self, "restart_policy")

    @restart_policy.setter
    def restart_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "restart_policy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorTagArgs']]]]:
        """
        tags of the resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConnectorTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        [NAME-VERSION] the version of the hub connector
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


class Connector(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 inputs: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ConnectorInputArgs', 'ConnectorInputArgsDict']]]]] = None,
                 log_level: Optional[pulumi.Input[str]] = None,
                 machine_instance_size: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 node: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ConnectorTagArgs', 'ConnectorTagArgsDict']]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ## Import

        ```sh
        $ pulumi import splight:index/connector:Connector [options] splight_connector.<name> <connector_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: optional description to add details of the resource
        :param pulumi.Input[Sequence[pulumi.Input[Union['ConnectorInputArgs', 'ConnectorInputArgsDict']]]] inputs: static config parameters of the routine
        :param pulumi.Input[str] log_level: log level of the connector
        :param pulumi.Input[str] machine_instance_size: instance size
        :param pulumi.Input[str] name: the name of the connector to be created
        :param pulumi.Input[str] node: id of the compute node where the connector runs
        :param pulumi.Input[str] restart_policy: restart policy of the connector
        :param pulumi.Input[Sequence[pulumi.Input[Union['ConnectorTagArgs', 'ConnectorTagArgsDict']]]] tags: tags of the resource
        :param pulumi.Input[str] version: [NAME-VERSION] the version of the hub connector
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConnectorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ## Import

        ```sh
        $ pulumi import splight:index/connector:Connector [options] splight_connector.<name> <connector_id>
        ```

        :param str resource_name: The name of the resource.
        :param ConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 inputs: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ConnectorInputArgs', 'ConnectorInputArgsDict']]]]] = None,
                 log_level: Optional[pulumi.Input[str]] = None,
                 machine_instance_size: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 node: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ConnectorTagArgs', 'ConnectorTagArgsDict']]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectorArgs.__new__(ConnectorArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["inputs"] = inputs
            __props__.__dict__["log_level"] = log_level
            __props__.__dict__["machine_instance_size"] = machine_instance_size
            __props__.__dict__["name"] = name
            __props__.__dict__["node"] = node
            __props__.__dict__["restart_policy"] = restart_policy
            __props__.__dict__["tags"] = tags
            if version is None and not opts.urn:
                raise TypeError("Missing required property 'version'")
            __props__.__dict__["version"] = version
        super(Connector, __self__).__init__(
            'splight:index/connector:Connector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            inputs: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ConnectorInputArgs', 'ConnectorInputArgsDict']]]]] = None,
            log_level: Optional[pulumi.Input[str]] = None,
            machine_instance_size: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            node: Optional[pulumi.Input[str]] = None,
            restart_policy: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ConnectorTagArgs', 'ConnectorTagArgsDict']]]]] = None,
            version: Optional[pulumi.Input[str]] = None) -> 'Connector':
        """
        Get an existing Connector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: optional description to add details of the resource
        :param pulumi.Input[Sequence[pulumi.Input[Union['ConnectorInputArgs', 'ConnectorInputArgsDict']]]] inputs: static config parameters of the routine
        :param pulumi.Input[str] log_level: log level of the connector
        :param pulumi.Input[str] machine_instance_size: instance size
        :param pulumi.Input[str] name: the name of the connector to be created
        :param pulumi.Input[str] node: id of the compute node where the connector runs
        :param pulumi.Input[str] restart_policy: restart policy of the connector
        :param pulumi.Input[Sequence[pulumi.Input[Union['ConnectorTagArgs', 'ConnectorTagArgsDict']]]] tags: tags of the resource
        :param pulumi.Input[str] version: [NAME-VERSION] the version of the hub connector
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConnectorState.__new__(_ConnectorState)

        __props__.__dict__["description"] = description
        __props__.__dict__["inputs"] = inputs
        __props__.__dict__["log_level"] = log_level
        __props__.__dict__["machine_instance_size"] = machine_instance_size
        __props__.__dict__["name"] = name
        __props__.__dict__["node"] = node
        __props__.__dict__["restart_policy"] = restart_policy
        __props__.__dict__["tags"] = tags
        __props__.__dict__["version"] = version
        return Connector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        optional description to add details of the resource
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def inputs(self) -> pulumi.Output[Optional[Sequence['outputs.ConnectorInput']]]:
        """
        static config parameters of the routine
        """
        return pulumi.get(self, "inputs")

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> pulumi.Output[Optional[str]]:
        """
        log level of the connector
        """
        return pulumi.get(self, "log_level")

    @property
    @pulumi.getter(name="machineInstanceSize")
    def machine_instance_size(self) -> pulumi.Output[Optional[str]]:
        """
        instance size
        """
        return pulumi.get(self, "machine_instance_size")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        the name of the connector to be created
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def node(self) -> pulumi.Output[Optional[str]]:
        """
        id of the compute node where the connector runs
        """
        return pulumi.get(self, "node")

    @property
    @pulumi.getter(name="restartPolicy")
    def restart_policy(self) -> pulumi.Output[Optional[str]]:
        """
        restart policy of the connector
        """
        return pulumi.get(self, "restart_policy")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.ConnectorTag']]]:
        """
        tags of the resource
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        [NAME-VERSION] the version of the hub connector
        """
        return pulumi.get(self, "version")

