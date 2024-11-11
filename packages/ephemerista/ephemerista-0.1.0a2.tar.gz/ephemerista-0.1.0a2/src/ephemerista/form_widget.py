import pathlib
from collections.abc import Callable
from enum import Enum
from typing import Any

import anywidget._descriptor
import anywidget.experimental
import psygnal
import pydantic
from pydantic import ConfigDict, PydanticInvalidForJsonSchema
from pydantic.alias_generators import to_camel
from pydantic.fields import ComputedFieldInfo, FieldInfo
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue, JsonSchemaWarningKind, _deduplicate_schemas
from pydantic_core import PydanticOmit, core_schema


class FormWidgetGenerateJsonSchema(GenerateJsonSchema):
    ignored_warning_kinds: set[JsonSchemaWarningKind] = {"non-serializable-default"}  # noqa: RUF012

    def nullable_schema(self, schema: core_schema.NullableSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that allows null values.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        null_schema = {"type": "null", "title": "Empty"}
        inner_json_schema = self.generate_inner(schema["schema"])

        if inner_json_schema == null_schema:
            return null_schema
        else:
            # Thanks to the equality check against `null_schema` above, I think 'oneOf' would also be valid here;
            # I'll use 'anyOf' for now, but it could be changed it if it would work better with some external tooling
            inner_json_schema["title"] = "Value"

            return self.get_flattened_anyof([inner_json_schema, null_schema])

    def tagged_union_schema(self, schema: core_schema.TaggedUnionSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that allows values matching any of the given schemas, where
        the schemas are tagged with a discriminator field that indicates which schema should be used to validate
        the value.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        generated: dict[str, JsonSchemaValue] = {}
        for k, v in schema["choices"].items():
            if isinstance(k, Enum):
                k = k.value  # noqa: PLW2901
            try:
                # Use str(k) since keys must be strings for json; while not technically correct,
                # it's the closest that can be represented in valid JSON
                generated[str(k)] = self.generate_inner(v).copy()
            except PydanticOmit:
                continue
            except PydanticInvalidForJsonSchema as exc:
                self.emit_warning("skipped-choice", exc.message)

        one_of_choices = _deduplicate_schemas(generated.values())
        if len(one_of_choices) == 1:
            # Don't show oneOf if there's only one option
            json_schema: JsonSchemaValue = one_of_choices[0]
        else:
            json_schema: JsonSchemaValue = {"oneOf": one_of_choices}

        # This reflects the v1 behavior; TODO: we should make it possible to exclude OpenAPI stuff from the JSON schema
        openapi_discriminator = self._extract_discriminator(schema, one_of_choices)
        if openapi_discriminator is not None:
            json_schema["discriminator"] = {
                "propertyName": openapi_discriminator,
                "mapping": {k: v.get("$ref", v) for k, v in generated.items()},
            }

        return json_schema

    def tuple_schema(self, schema: core_schema.TupleSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a tuple schema e.g. `Tuple[int,
        str, bool]` or `Tuple[int, ...]`.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        json_schema: JsonSchemaValue = {"type": "array"}
        if "variadic_item_index" in schema:
            variadic_item_index = schema["variadic_item_index"]
            if variadic_item_index > 0:
                json_schema["minItems"] = variadic_item_index
                json_schema["prefixItems"] = [
                    self.generate_inner(item) for item in schema["items_schema"][:variadic_item_index]
                ]
            if variadic_item_index + 1 == len(schema["items_schema"]):
                # if the variadic item is the last item, then represent it faithfully
                json_schema["items"] = self.generate_inner(schema["items_schema"][variadic_item_index])
            else:
                # otherwise, 'items' represents the schema for the variadic
                # item plus the suffix, so just allow anything for simplicity
                # for now
                json_schema["items"] = True
        else:
            prefix_items = [self.generate_inner(item) for item in schema["items_schema"]]
            if prefix_items:
                json_schema["prefixItems"] = prefix_items
            json_schema["minItems"] = len(prefix_items)
            json_schema["maxItems"] = len(prefix_items)

        # Checking if all items are the same
        first_item = json_schema["prefixItems"][0]
        all_same = True
        for item in json_schema["prefixItems"]:
            if first_item != item:
                all_same = False

        if all_same:
            # RJSF does not support prefixItems so we swap this into items
            # The main use for this is the Vec3 type
            item_type = json_schema["prefixItems"][0]
            json_schema.pop("prefixItems")
            json_schema["items"] = item_type

        self.update_with_validations(json_schema, schema, self.ValidationsMapping.array)
        return json_schema


def annotate_vec3s_with_unique_ids(schema: dict[str, Any]):
    """Annotate vec3 types in JSON schema with unique IDs and return the IDs

    This function will mutate the input to add the uninque IDs on the JSON
    schema using the $id attribute.

    RJSF doesn't have an easy way to customize fields fields when they are
    deeply nested in a way that is also compatible with pydantic. I tried many
    solutions, but I never found anything that works in all situations.

    This approach doesn't scale well if we add more special types, but works
    well enough given that we only have one type to treat specially, vec3.
    """

    def parse_defs(schema: dict[str, Any]) -> list[dict[str, Any]]:
        items = []

        if "$defs" in schema:
            for define in schema["$defs"].values():
                items.extend(parse_type(define))

        return items

    def parse_object(schema: dict[str, Any]) -> list[dict[str, Any]]:
        items = []

        for object_property in schema["properties"].values():
            items.extend(parse_type(object_property))

        return items

    def parse_array(schema: dict[str, Any]) -> list[dict[str, Any]]:
        vec3_expected_items_count = 3
        if (
            "minItems" in schema
            and "maxItems" in schema
            and "items" in schema
            and schema["minItems"] == vec3_expected_items_count
            and schema["maxItems"] == vec3_expected_items_count
            and schema["items"] == {"type": "number"}
        ):
            return [schema]

        return []

    def parse_any_of(schema: dict[str, Any]) -> list[dict[str, Any]]:
        return_value = []
        for item in schema["anyOf"]:
            return_value.extend(parse_type(item))

        return return_value

    def parse_one_of(schema: dict[str, Any]) -> list[dict[str, Any]]:
        return_value = []
        for item in schema["oneOf"]:
            return_value.extend(parse_type(item))

        return return_value

    def parse_all_of(schema: dict[str, Any]) -> list[dict[str, Any]]:
        return_value = []
        for item in schema["allOf"]:
            return_value.extend(parse_type(item))

        return return_value

    def parse_type(schema: dict[str, Any]) -> list[dict[str, Any]]:
        if "type" in schema:
            if schema["type"] == "object":
                return parse_object(schema)
            elif schema["type"] == "array":
                return parse_array(schema)
            else:
                # It's a primitive type, so we don't care
                return []
        elif "anyOf" in schema:
            return parse_any_of(schema)
        elif "oneOf" in schema:
            return parse_one_of(schema)
        elif "allOf" in schema:
            return parse_all_of(schema)
        elif "$ref" in schema:
            # We handle refs via parse_defs
            return []
        else:
            message = "Unable to parse type"
            raise RuntimeError(message)

    found = parse_type(schema)
    found.extend(parse_defs(schema))

    item_ids = []

    for index, item in enumerate(found):
        item_id = f"/schemas/vec3-{index}"
        item["$id"] = item_id
        item_ids.append(item_id)

    schema["$vec3UniqueIds"] = item_ids


def underscore_case_to_words(underscore_case_string: str) -> str:
    parts_list = underscore_case_string.split("_")

    parts_list = [x.lower() for x in parts_list]

    return " ".join(parts_list).capitalize()


def camel_case_to_words(camel_case_string: str) -> str:
    import re

    parts_list: list[str] = re.split("(?<=[a-z])(?=[A-Z])", camel_case_string)

    parts_list = [x.lower() for x in parts_list]

    return " ".join(parts_list).capitalize()


def field_title_generator(field_name: str, _field_info: FieldInfo | ComputedFieldInfo) -> str:
    return underscore_case_to_words(field_name)


def model_title_generator(model: type) -> str:
    return camel_case_to_words(model.__name__)


_mime_bundle_descriptor_get: Callable[[object, object, type], anywidget._descriptor.ReprMimeBundle] | None = None


def _mime_bundle_descriptor_get_override(self, instance: object, owner: type) -> anywidget._descriptor.ReprMimeBundle:
    """Install hooks after ReprMimeBundle lazy loadingS

    anywidget lazyloads the ReprMimeBundle object. This is great. But we
    still need a way to install our message interceptors while leveraging
    the lazy loading. This hook does this.
    """

    if not _mime_bundle_descriptor_get:
        msg = "Could not find descriptor"
        raise RuntimeError(msg)

    bundle = _mime_bundle_descriptor_get(self, instance, owner)

    obj = bundle._obj()
    if obj:
        # Install our message interceptor so we can handle custom messages
        obj._parent_msg_callback = bundle._comm._msg_callback
        bundle._comm.on_msg(obj._FormWidgetHandler__ipywidget_message_interceptor)

    return bundle


class FormWidgetHandler(pydantic.BaseModel):
    model_config = ConfigDict(
        field_title_generator=field_title_generator,
        model_title_generator=model_title_generator,
        # Generic configs not related to form widgets
        populate_by_name=True,
        alias_generator=to_camel,
    )

    def __init__(self, **_data):
        global _mime_bundle_descriptor_get  # noqa: PLW0603
        if not _mime_bundle_descriptor_get:
            _mime_bundle_descriptor_get = anywidget.experimental.MimeBundleDescriptor.__get__  # type: ignore
            anywidget.experimental.MimeBundleDescriptor.__get__ = _mime_bundle_descriptor_get_override  # type: ignore

    def __ipywidget_message_interceptor(self, message):
        """Intercepts custom messages from front-end"""
        try:
            data = message["content"]["data"]

            if data["method"] == "custom" and data["content"]["operation"] == "get_schema":
                json_schema = self.model_json_schema(
                    by_alias=False,
                    schema_generator=FormWidgetGenerateJsonSchema,
                )

                annotate_vec3s_with_unique_ids(json_schema)

                self._ipywidget_send_custom(
                    {
                        "operation": "get_schema",
                        "response": json_schema,
                    },
                )
            elif data["method"] == "custom" and data["content"]["operation"] == "get_initial_data":
                self._ipywidget_send_custom(
                    {"operation": "get_initial_data", "response": self.model_dump(mode="json")},
                )

            else:
                self._parent_msg_callback(message)
        except KeyError:
            pass

    def _ipywidget_send_custom(self, message):
        """Sends custom messages to the front-end

        Custom messages are the only way that anywidget allows us to deliver
        messages to the front-end.
        """
        self._repr_mimebundle_._comm.send(  # type: ignore
            {
                "method": "custom",
                "content": message,
            }
        )


static_folder_path = pathlib.Path(__file__).parent / "static"
form_widget_esm_path = static_folder_path / "form_widget.js"
form_widget_css_path = static_folder_path / "form_widget.css"


def with_form_widget(k):
    k = anywidget.experimental.widget(esm=form_widget_esm_path, css=form_widget_css_path)(k)
    k = psygnal.evented()(k)

    return k
