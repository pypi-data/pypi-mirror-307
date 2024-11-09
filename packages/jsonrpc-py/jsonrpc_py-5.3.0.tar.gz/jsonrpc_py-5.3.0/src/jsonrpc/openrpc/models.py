from __future__ import annotations

from dataclasses import field
from enum import StrEnum
from typing import TYPE_CHECKING, final

from .abstract import ModelMeta
from .undefined import Undefined, UndefinedType

if TYPE_CHECKING:
    from typing import Any, Final

__all__: tuple[str, ...] = (
    "Components",
    "Contact",
    "ContentDescriptor",
    "Error",
    "Example",
    "ExamplePairing",
    "ExternalDocumentation",
    "Info",
    "License",
    "Link",
    "Method",
    "OpenRPC",
    "ParamStructure",
    "Server",
    "ServerVariable",
    "Tag",
    "VERSION",
)

VERSION: Final = "1.3.2"


class Contact(metaclass=ModelMeta):
    """
    Contact information for the API.

    :param str name: The identifying name of the contact person/organization.
    :param str url: The URL pointing to the contact information.
    :param str email: The email address of the contact person/organization.
    """

    name: str | None = None
    url: str | None = None
    email: str | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Contact schema <https://spec.open-rpc.org/#contact-object>`_.
        """
        obj: dict[str, Any] = {}

        if (name := self.name) is not None:
            obj |= {"name": name}
        if (url := self.url) is not None:
            obj |= {"url": url}
        if (email := self.email) is not None:
            obj |= {"email": email}

        return obj


class License(metaclass=ModelMeta):
    """
    License information for the API.

    :param str name: The license name used for the API.
    :param str url: A URL to the license used for the API.
    """

    name: str
    url: str | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `License schema <https://spec.open-rpc.org/#license-object>`_.
        """
        obj: dict[str, Any] = {"name": self.name}

        if (url := self.url) is not None:
            obj |= {"url": url}

        return obj


class Info(metaclass=ModelMeta):
    """
    The object provides metadata about the API.

    :param str title: The title of the application.
    :param str version: The version of the OpenRPC document.
    :param str description: A verbose description of the application.
    :param str terms_of_service: A URL to the Terms of Service for the API.
    :param Contact contact: The contact information for the API.
    :param License license: The license information for the API.
    """

    title: str
    version: str
    description: str | None = None
    terms_of_service: str | None = None
    contact: Contact | None = None
    license: License | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Info schema <https://spec.open-rpc.org/#info-object>`_.
        """
        obj: dict[str, Any] = {"title": self.title, "version": self.version}

        if (description := self.description) is not None:
            obj |= {"description": description}
        if (terms_of_service := self.terms_of_service) is not None:
            obj |= {"termsOfService": terms_of_service}
        if (contact := self.contact) is not None:
            obj |= {"contact": contact.json}
        if (licenze := self.license) is not None:
            obj |= {"license": licenze.json}

        return obj


class ServerVariable(metaclass=ModelMeta):
    """
    An object representing a Server Variable for server URL template substitution.

    :param str default: The default value to use for substitution.
    :param list[str] enum: An enumeration of string values to be used if the substitution options are from a limited set.
    :param str description: An optional description for the server variable.
    """

    default: str
    enum: list[str] | None = None
    description: str | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Server Variable schema <https://spec.open-rpc.org/#server-variable-object>`_.
        """
        obj: dict[str, Any] = {"default": self.default}

        if (enum := self.enum) is not None:
            obj |= {"enum": enum}
        if (description := self.description) is not None:
            obj |= {"description": description}

        return obj


class Server(metaclass=ModelMeta):
    """
    An object representing a Server.

    :param str name: A name to be used as the cannonical name for the server.
    :param str url: A URL to the target host.
    :param str summary: A short summary of what the server is.
    :param str description: An optional string describing the host designated by the URL.
    :param dict[str, ServerVariable] variables: A :py:class:`dict` between a variable name and its value.
    """

    name: str
    url: str
    summary: str | None = None
    description: str | None = None
    variables: dict[str, ServerVariable] | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Server schema <https://spec.open-rpc.org/#server-object>`_.
        """
        obj: dict[str, Any] = {"name": self.name, "url": self.url}

        if (summary := self.summary) is not None:
            obj |= {"summary": summary}
        if (description := self.description) is not None:
            obj |= {"description": description}
        if (variables := self.variables) is not None:
            obj |= {"variables": {key: value.json for key, value in variables.items()}}

        return obj


class ExternalDocumentation(metaclass=ModelMeta):
    """
    Allows referencing an external resource for extended documentation.

    :param str url: The URL for the target documentation.
    :param str description: A verbose explanation of the target documentation.
    """

    url: str
    description: str | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `External Documentation schema <https://spec.open-rpc.org/#external-documentation-object>`_.
        """
        obj: dict[str, Any] = {"url": self.url}

        if (description := self.description) is not None:
            obj |= {"description": description}

        return obj


class Tag(metaclass=ModelMeta):
    """
    Adds metadata to a single tag that is used by the :class:`~jsonrpc.openrpc.Method` object.

    :param str name: The name of the tag.
    :param str summary: A short summary of the tag.
    :param str description: A verbose explanation for the tag.
    :param ExternalDocumentation external_docs: Additional external documentation for this tag.
    """

    name: str
    summary: str | None = None
    description: str | None = None
    external_docs: ExternalDocumentation | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Tag schema <https://spec.open-rpc.org/#tag-object>`_.
        """
        obj: dict[str, Any] = {"name": self.name}

        if (summary := self.summary) is not None:
            obj |= {"summary": summary}
        if (description := self.description) is not None:
            obj |= {"description": description}
        if (external_docs := self.external_docs) is not None:
            obj |= {"externalDocs": external_docs.json}

        return obj


class ContentDescriptor(metaclass=ModelMeta):
    """
    Content Descriptors are objects that do just as they suggest \u2013 describe content.
    They are reusable ways of describing either parameters or result.

    :param str name: Name of the content that is being described.
    :param str summary: A short summary of the content that is being described.
    :param str description: A verbose explanation of the content descriptor behavior.
    :param bool required: Determines if the content is a required field.
    :param dict[str, typing.Any] schema: Schema that describes the content.
    :param bool deprecated: Specifies that the content is deprecated and should be transitioned out of usage.
    """

    name: str
    summary: str | None = None
    description: str | None = None
    required: bool | None = None
    schema: dict[str, Any] = field(default_factory=dict)
    deprecated: bool | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Content Descriptor schema <https://spec.open-rpc.org/#content-descriptor-object>`_.
        """
        obj: dict[str, Any] = {"name": self.name, "schema": self.schema}

        if (summary := self.summary) is not None:
            obj |= {"summary": summary}
        if (description := self.description) is not None:
            obj |= {"description": description}
        if (required := self.required) is not None:
            obj |= {"required": required}
        if (deprecated := self.deprecated) is not None:
            obj |= {"deprecated": deprecated}

        return obj


class Error(metaclass=ModelMeta):
    """
    Defines an application level error.

    :param int code: An :py:class:`int` object that indicates the error type that occurred.
    :param str message: A :py:class:`str` object providing a short description of the error.
    :param typing.Any data: A primitive or structured value that contains additional information about the error.
    """

    code: int
    message: str
    data: Any = Undefined

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Error schema <https://spec.open-rpc.org/#error-object>`_.
        """
        obj: dict[str, Any] = {"code": self.code, "message": self.message}

        if not isinstance(data := self.data, UndefinedType):
            obj |= {"data": data}

        return obj


class Link(metaclass=ModelMeta):
    """
    The Link object represents a possible design-time link for a result.

    :param str name: Cannonical name of the link.
    :param str summary: Short description for the link.
    :param str description: A description of the link.
    :param str method: The name of an existing OpenRPC method.
    :param dict[str, typing.Any] params: A :py:class:`dict` object representing parameters to pass to a method as specified with method.
    :param Server server: A :class:`~jsonrpc.openrpc.Server` object to be used by the target method.
    """

    name: str
    summary: str | None = None
    description: str | None = None
    method: str | None = None
    params: dict[str, Any] | None = None
    server: Server | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Link schema <https://spec.open-rpc.org/#link-object>`_.
        """
        obj: dict[str, Any] = {"name": self.name}

        if (summary := self.summary) is not None:
            obj |= {"summary": summary}
        if (description := self.description) is not None:
            obj |= {"description": description}
        if (method := self.method) is not None:
            obj |= {"method": method}
        if (params := self.params) is not None:
            obj |= {"params": params}
        if (server := self.server) is not None:
            obj |= {"server": server.json}

        return obj


@final
class ParamStructure(StrEnum):
    """
    Param Structure is the expected format of the parameters.
    """

    #: Parameters must contains named arguments as a by-name object.
    BY_NAME = "by-name"
    #: Parameters must contains positional arguments as a by-position array.
    BY_POSITION = "by-position"
    #: Parameters can be either named arguments or positional arguments.
    EITHER = "either"


class Example(metaclass=ModelMeta):
    """
    The object that defines an example that is intended to match the schema of a given :class:`~jsonrpc.openrpc.ContentDescriptor`.
    The ``value`` field and ``external_value`` field are mutually exclusive.

    :param str name: Cannonical name of the example.
    :param str summary: Short description for the example.
    :param str description: A verbose explanation of the example.
    :param typing.Any value: Embedded literal example.
    :param str external_value: A URL that points to the literal example.
    :raises TypeError: If ``value`` and ``external_value`` fields are specified both.
    """

    name: str | None = None
    summary: str | None = None
    description: str | None = None
    value: Any = Undefined
    external_value: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.value, UndefinedType) and self.external_value is not None:
            raise TypeError("The 'value' field and 'external_value' field are mutually exclusive")

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Example schema <https://spec.open-rpc.org/#example-object>`_.
        """
        obj: dict[str, Any] = {}

        if (name := self.name) is not None:
            obj |= {"name": name}
        if (summary := self.summary) is not None:
            obj |= {"summary": summary}
        if (description := self.description) is not None:
            obj |= {"description": description}
        if not isinstance(value := self.value, UndefinedType):
            obj |= {"value": value}
        elif (external_value := self.external_value) is not None:
            obj |= {"externalValue": external_value}

        return obj


class ExamplePairing(metaclass=ModelMeta):
    """
    The Example Pairing object consists of a set of example params and result.

    :param str name: Name for the example pairing.
    :param str summary: Short description for the example pairing.
    :param str description: A verbose explanation of the example pairing.
    :param list[Example] params: Example parameters.
    :param Example result: Example result.
    """

    name: str
    summary: str | None = None
    description: str | None = None
    params: list[Example] = field(default_factory=list)
    result: Example | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Example Pairing schema <https://spec.open-rpc.org/#example-pairing-object>`_.
        """
        obj: dict[str, Any] = {"name": self.name, "params": [value.json for value in self.params]}

        if (summary := self.summary) is not None:
            obj |= {"summary": summary}
        if (description := self.description) is not None:
            obj |= {"description": description}
        if (result := self.result) is not None:
            obj |= {"result": result.json}

        return obj


class Method(metaclass=ModelMeta):
    """
    Describes the interface for the given method name.

    :param str name: The cannonical name for the method.
    :param list[Tag] tags: A list of tags for API documentation control.
    :param str summary: A short summary of what the method does.
    :param str description: A verbose explanation of the method behavior.
    :param ExternalDocumentation external_docs: Additional external documentation for this method.
    :param list[ContentDescriptor] params: A list of parameters that are applicable for this method.
    :param ContentDescriptor result: The description of the result returned by the method.
    :param bool deprecated: Declares this method to be deprecated.
    :param list[Server] servers: An alternative ``servers`` array to service this method.
    :param list[Error] errors: A list of custom application defined errors that may be returned.
    :param list[Link] links: A list of possible links from this method call.
    :param ParamStructure param_structure: The expected format of the parameters.
    :param list[ExamplePairing] examples: Array of :class:`~jsonrpc.openrpc.ExamplePairing` objects
        where each example includes a valid params-to-result :class:`~jsonrpc.openrpc.ContentDescriptor` pairing.
    """

    name: str
    tags: list[Tag] | None = None
    summary: str | None = None
    description: str | None = None
    external_docs: ExternalDocumentation | None = None
    params: list[ContentDescriptor] = field(default_factory=list)
    result: ContentDescriptor | None = None
    deprecated: bool | None = None
    servers: list[Server] | None = None
    errors: list[Error] | None = None
    links: list[Link] | None = None
    param_structure: ParamStructure | None = None
    examples: list[ExamplePairing] | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Method schema <https://spec.open-rpc.org/#method-object>`_.
        """
        obj: dict[str, Any] = {"name": self.name, "params": [value.json for value in self.params]}

        if (tags := self.tags) is not None:
            obj |= {"tags": [value.json for value in tags]}
        if (summary := self.summary) is not None:
            obj |= {"summary": summary}
        if (description := self.description) is not None:
            obj |= {"description": description}
        if (external_docs := self.external_docs) is not None:
            obj |= {"externalDocs": external_docs.json}
        if (result := self.result) is not None:
            obj |= {"result": result.json}
        if (deprecated := self.deprecated) is not None:
            obj |= {"deprecated": deprecated}
        if (servers := self.servers) is not None:
            obj |= {"servers": [value.json for value in servers]}
        if (errors := self.errors) is not None:
            obj |= {"errors": [value.json for value in errors]}
        if (links := self.links) is not None:
            obj |= {"links": [value.json for value in links]}
        if (param_structure := self.param_structure) is not None:
            obj |= {"paramStructure": param_structure}
        if (examples := self.examples) is not None:
            obj |= {"examples": [value.json for value in examples]}

        return obj


class Components(metaclass=ModelMeta):
    """
    Holds a set of reusable objects for different aspects of the OpenRPC.

    :param dict[str, ContentDescriptor] content_descriptors: An object to hold reusable :class:`~jsonrpc.openrpc.ContentDescriptor` objects.
    :param dict[str, typing.Any] schemas: An object to hold reusable schema objects.
    :param dict[str, Example] examples: An object to hold reusable :class:`~jsonrpc.openrpc.Example` objects.
    :param dict[str, Link] links: An object to hold reusable :class:`~jsonrpc.openrpc.Link` objects.
    :param dict[str, Error] errors: An object to hold reusable :class:`~jsonrpc.openrpc.Error` objects.
    :param dict[str, ExamplePairing] example_pairing_objects: An object to hold reusable :class:`~jsonrpc.openrpc.ExamplePairing` objects.
    :param dict[str, Tag] tags: An object to hold reusable :class:`~jsonrpc.openrpc.Tag` objects.
    """

    content_descriptors: dict[str, ContentDescriptor] | None = None
    schemas: dict[str, Any] | None = None
    examples: dict[str, Example] | None = None
    links: dict[str, Link] | None = None
    errors: dict[str, Error] | None = None
    example_pairing_objects: dict[str, ExamplePairing] | None = None
    tags: dict[str, Tag] | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `Components schema <https://spec.open-rpc.org/#components-object>`_.
        """
        obj: dict[str, Any] = {}

        if (content_descriptors := self.content_descriptors) is not None:
            obj |= {"contentDescriptors": {key: value.json for key, value in content_descriptors.items()}}
        if (schemas := self.schemas) is not None:
            obj |= {"schemas": schemas}
        if (examples := self.examples) is not None:
            obj |= {"examples": {key: value.json for key, value in examples.items()}}
        if (links := self.links) is not None:
            obj |= {"links": {key: value.json for key, value in links.items()}}
        if (errors := self.errors) is not None:
            obj |= {"errors": {key: value.json for key, value in errors.items()}}
        if (example_pairing_objects := self.example_pairing_objects) is not None:
            obj |= {"examplePairingObjects": {key: value.json for key, value in example_pairing_objects.items()}}
        if (tags := self.tags) is not None:
            obj |= {"tags": {key: value.json for key, value in tags.items()}}

        return obj


class OpenRPC(metaclass=ModelMeta):
    """
    This is the root object of the OpenRPC document.

    :param str openrpc: The version string of OpenRPC.
    :param Info info: Provides metadata about the API.
    :param list[Server] servers: An array of servers, which provide connectivity information to a target server.
    :param list[Method] methods: The available methods for the API.
    :param Components components: An element to hold various schemas for the specification.
    :param ExternalDocumentation external_docs: Additional external documentation.
    """

    openrpc: str = VERSION
    info: Info
    servers: list[Server] | None = None
    methods: list[Method] = field(default_factory=list)
    components: Components | None = None
    external_docs: ExternalDocumentation | None = None

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the `OpenRPC schema <https://spec.open-rpc.org/#openrpc-object>`_.
        """
        obj: dict[str, Any] = {
            "openrpc": self.openrpc,
            "info": self.info.json,
            "methods": [value.json for value in self.methods],
        }

        if (servers := self.servers) is not None:
            obj |= {"servers": [value.json for value in servers]}
        if (components := self.components) is not None:
            obj |= {"components": components.json}
        if (external_docs := self.external_docs) is not None:
            obj |= {"externalDocs": external_docs.json}

        return obj
