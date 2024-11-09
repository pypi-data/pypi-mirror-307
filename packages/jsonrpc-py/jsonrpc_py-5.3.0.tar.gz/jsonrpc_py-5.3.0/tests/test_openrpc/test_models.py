from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

import jsonrpc.openrpc as openrpc


class TestContact(TestCase):
    def setUp(self) -> None:
        self.contact: openrpc.Contact = openrpc.Contact()

    def test_name(self) -> None:
        self.assertNotIn("name", self.contact.json)

        self.contact.name = Mock()
        self.assertEqual(self.contact.json["name"], self.contact.name)

    def test_url(self) -> None:
        self.assertNotIn("url", self.contact.json)

        self.contact.url = Mock()
        self.assertEqual(self.contact.json["url"], self.contact.url)

    def test_email(self) -> None:
        self.assertNotIn("email", self.contact.json)

        self.contact.email = Mock()
        self.assertEqual(self.contact.json["email"], self.contact.email)


class TestLicense(TestCase):
    def setUp(self) -> None:
        self.license: openrpc.License = openrpc.License(name=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.license.json["name"], self.license.name)

    def test_url(self) -> None:
        self.assertNotIn("url", self.license.json)

        self.license.url = Mock()
        self.assertEqual(self.license.json["url"], self.license.url)


class TestInfo(TestCase):
    def setUp(self) -> None:
        self.info: openrpc.Info = openrpc.Info(title=Mock(), version=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.info.json["title"], self.info.title)
        self.assertEqual(self.info.json["version"], self.info.version)

    def test_description(self) -> None:
        self.assertNotIn("description", self.info.json)

        self.info.description = Mock()
        self.assertEqual(self.info.json["description"], self.info.description)

    def test_terms_of_service(self) -> None:
        self.assertNotIn("termsOfService", self.info.json)

        self.info.terms_of_service = Mock()
        self.assertEqual(self.info.json["termsOfService"], self.info.terms_of_service)

    def test_contact(self) -> None:
        self.assertNotIn("contact", self.info.json)

        self.info.contact = openrpc.Contact(name=Mock())
        self.assertEqual(self.info.json["contact"], self.info.contact.json)

    def test_license(self) -> None:
        self.assertNotIn("license", self.info.json)

        self.info.license = openrpc.License(name=Mock())
        self.assertEqual(self.info.json["license"], self.info.license.json)


class TestServerVariable(TestCase):
    def setUp(self) -> None:
        self.server_variable: openrpc.ServerVariable = openrpc.ServerVariable(default=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.server_variable.json["default"], self.server_variable.default)

    def test_enum(self) -> None:
        self.assertNotIn("enum", self.server_variable.json)

        self.server_variable.enum = [Mock() for _ in range(3)]
        self.assertCountEqual(self.server_variable.json["enum"], self.server_variable.enum)

    def test_description(self) -> None:
        self.assertNotIn("description", self.server_variable.json)

        self.server_variable.description = Mock()
        self.assertEqual(self.server_variable.json["description"], self.server_variable.description)


class TestServer(TestCase):
    def setUp(self) -> None:
        self.server: openrpc.Server = openrpc.Server(name=Mock(), url=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.server.json["name"], self.server.name)
        self.assertEqual(self.server.json["url"], self.server.url)

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.server.json)

        self.server.summary = Mock()
        self.assertEqual(self.server.json["summary"], self.server.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.server.json)

        self.server.description = Mock()
        self.assertEqual(self.server.json["description"], self.server.description)

    def test_variables(self) -> None:
        self.assertNotIn("variables", self.server.json)

        self.server.variables = {Mock(): openrpc.ServerVariable(default=Mock())}
        self.assertDictEqual(self.server.json["variables"], {key: value.json for key, value in self.server.variables.items()})


class TestExternalDocumentation(TestCase):
    def setUp(self) -> None:
        self.external_docs: openrpc.ExternalDocumentation = openrpc.ExternalDocumentation(url=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.external_docs.json["url"], self.external_docs.url)

    def test_description(self) -> None:
        self.assertNotIn("description", self.external_docs.json)

        self.external_docs.description = Mock()
        self.assertEqual(self.external_docs.json["description"], self.external_docs.description)


class TestTag(TestCase):
    def setUp(self) -> None:
        self.tag: openrpc.Tag = openrpc.Tag(name=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.tag.json["name"], self.tag.name)

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.tag.json)

        self.tag.summary = Mock()
        self.assertEqual(self.tag.json["summary"], self.tag.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.tag.json)

        self.tag.description = Mock()
        self.assertEqual(self.tag.json["description"], self.tag.description)

    def test_external_docs(self) -> None:
        self.assertNotIn("externalDocs", self.tag.json)

        self.tag.external_docs = openrpc.ExternalDocumentation(url=Mock())
        self.assertDictEqual(self.tag.json["externalDocs"], self.tag.external_docs.json)


class TestContentDescriptor(TestCase):
    def setUp(self) -> None:
        self.content_descriptor: openrpc.ContentDescriptor = openrpc.ContentDescriptor(name=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.content_descriptor.json["name"], self.content_descriptor.name)
        self.assertDictEqual(self.content_descriptor.json["schema"], {})

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.content_descriptor.json)

        self.content_descriptor.summary = Mock()
        self.assertEqual(self.content_descriptor.json["summary"], self.content_descriptor.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.content_descriptor.json)

        self.content_descriptor.description = Mock()
        self.assertEqual(self.content_descriptor.json["description"], self.content_descriptor.description)

    def test_required(self) -> None:
        self.assertNotIn("required", self.content_descriptor.json)

        for required in (True, False):
            with self.subTest(required=required):
                self.content_descriptor.required = required
                self.assertIs(self.content_descriptor.json["required"], required)

    def test_deprecated(self) -> None:
        self.assertNotIn("deprecated", self.content_descriptor.json)

        for deprecated in (True, False):
            with self.subTest(deprecated=deprecated):
                self.content_descriptor.deprecated = deprecated
                self.assertIs(self.content_descriptor.json["deprecated"], deprecated)


class TestError(TestCase):
    def setUp(self) -> None:
        self.error: openrpc.Error = openrpc.Error(code=Mock(), message=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.error.json["code"], self.error.code)
        self.assertEqual(self.error.json["message"], self.error.message)

    def test_data(self) -> None:
        self.assertNotIn("data", self.error.json)

        self.error.data = Mock()
        self.assertEqual(self.error.json["data"], self.error.data)


class TestLink(TestCase):
    def setUp(self) -> None:
        self.link: openrpc.Link = openrpc.Link(name=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.link.json["name"], self.link.name)

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.link.json)

        self.link.summary = Mock()
        self.assertEqual(self.link.json["summary"], self.link.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.link.json)

        self.link.description = Mock()
        self.assertEqual(self.link.json["description"], self.link.description)

    def test_method(self) -> None:
        self.assertNotIn("method", self.link.json)

        self.link.method = Mock()
        self.assertEqual(self.link.json["method"], self.link.method)

    def test_params(self) -> None:
        self.assertNotIn("params", self.link.json)

        self.link.params = {Mock(): None}
        self.assertDictEqual(self.link.json["params"], self.link.params)

    def test_server(self) -> None:
        self.assertNotIn("server", self.link.json)

        self.link.server = openrpc.Server(name=Mock(), url=Mock())
        self.assertDictEqual(self.link.json["server"], self.link.server.json)


class TestExample(TestCase):
    def setUp(self) -> None:
        self.example: openrpc.Example = openrpc.Example()

    def test_mutually_exclusive_fields(self) -> None:
        with self.assertRaises(TypeError) as context:
            openrpc.Example(value=Mock(), external_value=Mock())

        self.assertEqual(str(context.exception), "The 'value' field and 'external_value' field are mutually exclusive")

    def test_name(self) -> None:
        self.assertNotIn("name", self.example.json)

        self.example.name = Mock()
        self.assertEqual(self.example.json["name"], self.example.name)

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.example.json)

        self.example.summary = Mock()
        self.assertEqual(self.example.json["summary"], self.example.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.example.json)

        self.example.description = Mock()
        self.assertEqual(self.example.json["description"], self.example.description)

    def test_value(self) -> None:
        self.assertNotIn("value", self.example.json)

        self.example.value = Mock()
        self.assertEqual(self.example.json["value"], self.example.value)

    def test_external_value(self) -> None:
        self.assertNotIn("externalValue", self.example.json)

        self.example.external_value = Mock()
        self.assertEqual(self.example.json["externalValue"], self.example.external_value)


class TestExamplePairing(TestCase):
    def setUp(self) -> None:
        self.example_pairing: openrpc.ExamplePairing = openrpc.ExamplePairing(name=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.example_pairing.json["name"], self.example_pairing.name)
        self.assertListEqual(self.example_pairing.json["params"], [])

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.example_pairing.json)

        self.example_pairing.summary = Mock()
        self.assertEqual(self.example_pairing.json["summary"], self.example_pairing.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.example_pairing.json)

        self.example_pairing.description = Mock()
        self.assertEqual(self.example_pairing.json["description"], self.example_pairing.description)

    def test_params(self) -> None:
        self.assertListEqual(self.example_pairing.json["params"], [])

        self.example_pairing.params.extend(openrpc.Example(name=Mock()) for _ in range(3))
        self.assertCountEqual(self.example_pairing.json["params"], [value.json for value in self.example_pairing.params])

    def test_result(self) -> None:
        self.assertNotIn("result", self.example_pairing.json)

        self.example_pairing.result = openrpc.Example(name=Mock())
        self.assertEqual(self.example_pairing.json["result"], self.example_pairing.result.json)


class TestMethod(TestCase):
    def setUp(self) -> None:
        self.method: openrpc.Method = openrpc.Method(name=Mock())

    def test_required_fields(self) -> None:
        self.assertEqual(self.method.json["name"], self.method.name)
        self.assertListEqual(self.method.json["params"], [])

    def test_tags(self) -> None:
        self.assertNotIn("tags", self.method.json)

        self.method.tags = [openrpc.Tag(name=Mock()) for _ in range(3)]
        self.assertCountEqual(self.method.json["tags"], [value.json for value in self.method.tags])

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.method.json)

        self.method.summary = Mock()
        self.assertEqual(self.method.json["summary"], self.method.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.method.json)

        self.method.description = Mock()
        self.assertEqual(self.method.json["description"], self.method.description)

    def test_external_docs(self) -> None:
        self.assertNotIn("externalDocs", self.method.json)

        self.method.external_docs = openrpc.ExternalDocumentation(url=Mock())
        self.assertDictEqual(self.method.json["externalDocs"], self.method.external_docs.json)

    def test_params(self) -> None:
        self.assertListEqual(self.method.json["params"], [])

        self.method.params.extend(openrpc.ContentDescriptor(name=Mock()) for _ in range(3))
        self.assertCountEqual(self.method.json["params"], [value.json for value in self.method.params])

    def test_result(self) -> None:
        self.assertNotIn("result", self.method.json)

        self.method.result = openrpc.ContentDescriptor(name=Mock())
        self.assertDictEqual(self.method.json["result"], self.method.result.json)

    def test_deprecated(self) -> None:
        self.assertNotIn("deprecated", self.method.json)

        for deprecated in (True, False):
            with self.subTest(deprecated=deprecated):
                self.method.deprecated = deprecated
                self.assertIs(self.method.json["deprecated"], deprecated)

    def test_servers(self) -> None:
        self.assertNotIn("servers", self.method.json)

        self.method.servers = [openrpc.Server(name=Mock(), url=Mock()) for _ in range(3)]
        self.assertCountEqual(self.method.json["servers"], [value.json for value in self.method.servers])

    def test_errors(self) -> None:
        self.assertNotIn("errors", self.method.json)

        self.method.errors = [openrpc.Error(code=Mock(), message=Mock()) for _ in range(3)]
        self.assertCountEqual(self.method.json["errors"], [value.json for value in self.method.errors])

    def test_links(self) -> None:
        self.assertNotIn("links", self.method.json)

        self.method.links = [openrpc.Link(name=Mock()) for _ in range(3)]
        self.assertCountEqual(self.method.json["links"], [value.json for value in self.method.links])

    def test_param_structure(self) -> None:
        self.assertNotIn("paramStructure", self.method.json)

        for param_structure in openrpc.ParamStructure:
            with self.subTest(param_structure=param_structure):
                self.method.param_structure = param_structure
                self.assertEqual(self.method.json["paramStructure"], param_structure)

    def test_examples(self) -> None:
        self.assertNotIn("examples", self.method.json)

        self.method.examples = [openrpc.ExamplePairing(name=Mock()) for _ in range(3)]
        self.assertCountEqual(self.method.json["examples"], [value.json for value in self.method.examples])


class TestComponents(TestCase):
    def setUp(self) -> None:
        self.components: openrpc.Components = openrpc.Components()

    def test_content_descriptors(self) -> None:
        self.assertNotIn("contentDescriptors", self.components.json)

        self.components.content_descriptors = {Mock(): openrpc.ContentDescriptor(name=Mock())}
        self.assertDictEqual(
            self.components.json["contentDescriptors"],
            {key: value.json for key, value in self.components.content_descriptors.items()},
        )

    def test_schemas(self) -> None:
        self.assertNotIn("schemas", self.components.json)

        self.components.schemas = {Mock(): {"type": "Mock"}}
        self.assertDictEqual(self.components.json["schemas"], self.components.schemas)

    def test_examples(self) -> None:
        self.assertNotIn("examples", self.components.json)

        self.components.examples = {Mock(): openrpc.Example(name=Mock())}
        self.assertDictEqual(
            self.components.json["examples"],
            {key: value.json for key, value in self.components.examples.items()},
        )

    def test_links(self) -> None:
        self.assertNotIn("links", self.components.json)

        self.components.links = {Mock(): openrpc.Link(name=Mock())}
        self.assertDictEqual(
            self.components.json["links"],
            {key: value.json for key, value in self.components.links.items()},
        )

    def test_errors(self) -> None:
        self.assertNotIn("errors", self.components.json)

        self.components.errors = {Mock(): openrpc.Error(code=Mock(), message=Mock())}
        self.assertDictEqual(
            self.components.json["errors"],
            {key: value.json for key, value in self.components.errors.items()},
        )

    def test_example_pairing_objects(self) -> None:
        self.assertNotIn("examplePairingObjects", self.components.json)

        self.components.example_pairing_objects = {Mock(): openrpc.ExamplePairing(name=Mock())}
        self.assertDictEqual(
            self.components.json["examplePairingObjects"],
            {key: value.json for key, value in self.components.example_pairing_objects.items()},
        )

    def test_tags(self) -> None:
        self.assertNotIn("tags", self.components.json)

        self.components.tags = {Mock(): openrpc.Tag(name=Mock())}
        self.assertDictEqual(
            self.components.json["tags"],
            {key: value.json for key, value in self.components.tags.items()},
        )


class TestOpenRPC(TestCase):
    def setUp(self) -> None:
        self.openrpc: openrpc.OpenRPC = openrpc.OpenRPC(info=openrpc.Info(title=Mock(), version=Mock()))

    def test_required_fields(self) -> None:
        self.assertEqual(self.openrpc.json["openrpc"], openrpc.VERSION)
        self.assertDictEqual(self.openrpc.json["info"], self.openrpc.info.json)
        self.assertListEqual(self.openrpc.json["methods"], [])

    def test_servers(self) -> None:
        self.assertNotIn("servers", self.openrpc.json)

        self.openrpc.servers = [openrpc.Server(name=Mock(), url=Mock()) for _ in range(3)]
        self.assertCountEqual(self.openrpc.json["servers"], [value.json for value in self.openrpc.servers])

    def test_methods(self) -> None:
        self.assertListEqual(self.openrpc.json["methods"], [])

        self.openrpc.methods.extend(openrpc.Method(name=Mock()) for _ in range(3))
        self.assertCountEqual(self.openrpc.json["methods"], [value.json for value in self.openrpc.methods])

    def test_components(self) -> None:
        self.assertNotIn("components", self.openrpc.json)

        self.openrpc.components = openrpc.Components()
        self.assertDictEqual(self.openrpc.json["components"], self.openrpc.components.json)

    def test_external_docs(self) -> None:
        self.assertNotIn("externalDocs", self.openrpc.json)

        self.openrpc.external_docs = openrpc.ExternalDocumentation(url=Mock())
        self.assertDictEqual(self.openrpc.json["externalDocs"], self.openrpc.external_docs.json)
