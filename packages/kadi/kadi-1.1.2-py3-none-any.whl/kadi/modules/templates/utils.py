# Copyright 2022 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from io import BytesIO

import jsonref
from flask import json
from flask_login import current_user

import kadi.lib.constants as const
from kadi.lib.resources.utils import get_filtered_resources
from kadi.lib.resources.utils import search_resources
from kadi.modules.records.extras import remove_extra_values
from kadi.modules.records.schemas import RecordImportSchema

from .models import Template
from .models import TemplateType
from .schemas import TemplateImportSchema


JSON_SCHEMA_TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
}


def search_templates(
    search_query=None,
    page=1,
    per_page=10,
    sort="_score",
    visibility=None,
    explicit_permissions=False,
    user_ids=None,
    template_type=None,
    user=None,
):
    """Search and filter for templates.

    Uses :func:`kadi.lib.resources.utils.get_filtered_resources` and
    :func:`kadi.lib.resources.utils.search_resources`.

    :param search_query: (optional) See
        :func:`kadi.lib.resources.utils.search_resources`.
    :param page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param per_page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param sort: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param visibility: (optional) See
        :func:`kadi.lib.resources.utils.get_filtered_resources`.
    :param explicit_permissions: (optional) See
        :func:`kadi.lib.resources.utils.get_filtered_resources`.
    :param user_ids: (optional) See
        :func:`kadi.lib.resources.utils.get_filtered_resources`.
    :param template_type: (optional) A type value to filter the templates with.
    :param user: (optional) The user to check for any permissions regarding the searched
        templates. Defaults to the current user.
    :return: The search results as returned by
        :func:`kadi.lib.resources.utils.search_resources`.
    """
    user = user if user is not None else current_user

    templates_query = get_filtered_resources(
        Template,
        visibility=visibility,
        explicit_permissions=explicit_permissions,
        user_ids=user_ids,
        user=user,
    )

    if template_type in TemplateType.__values__:
        templates_query = templates_query.filter(Template.type == template_type)

    template_ids = [t.id for t in templates_query.with_entities(Template.id)]

    return search_resources(
        Template,
        search_query=search_query,
        page=page,
        per_page=per_page,
        sort=sort,
        filter_ids=template_ids,
    )


def _parse_json_data(import_data, template_type):
    try:
        import_data = json.load(import_data)

        if not isinstance(import_data, dict):
            return None

        # Basic check if we are dealing with template data. We assume record data
        # otherwise.
        if "data" in import_data:
            import_template_type = import_data.get("type")
            import_data = TemplateImportSchema(
                template_type=import_template_type, partial=True
            ).load(import_data)
        else:
            import_template_type = TemplateType.RECORD
            import_data = RecordImportSchema(partial=True).load(import_data)

            # Remove the values of extras when dealing with record data.
            if "extras" in import_data:
                import_data["extras"] = remove_extra_values(import_data["extras"])

            import_data = {"data": import_data}

        # Allow using record data for extras templates and vice versa.
        if (
            template_type == TemplateType.RECORD
            and import_template_type == TemplateType.EXTRAS
        ):
            import_data["data"] = {"extras": import_data.get("data", [])}

        elif (
            template_type == TemplateType.EXTRAS
            and import_template_type == TemplateType.RECORD
        ):
            import_data["data"] = import_data.get("data", {}).get("extras", [])

        elif template_type != import_template_type:
            return None

        return import_data
    except:
        return None


def _json_schema_to_extras(properties, required_props=None):
    required_props = required_props if required_props is not None else []
    extras = []

    if isinstance(properties, dict):
        properties_iter = properties.items()
    else:
        properties_iter = enumerate(properties)

    for key, value in properties_iter:
        # Keys within lists will simply be ignored by the extra schema.
        extra = {"key": key}

        if (extras_description := value.get("description")) is not None:
            extra["description"] = str(extras_description)

        # We just use "string" as fallback type, as extras always need an explicit type.
        value_type = value.get("type", "string")

        if isinstance(value_type, list):
            value_type = value_type[0]

        if value_type in {"object", "array"}:
            extra["type"] = "dict" if value_type == "object" else "list"

            if value_type == "object":
                result = _json_schema_to_extras(
                    value.get("properties", {}), value.get("required", [])
                )
            else:
                if (items := value.get("items")) is not None:
                    result = _json_schema_to_extras([items])
                else:
                    result = _json_schema_to_extras(value.get("prefixItems", []))

            extra["value"] = result
        else:
            if value_type == "string":
                extra["type"] = "date" if value.get("format") == "date-time" else "str"
            else:
                extra["type"] = JSON_SCHEMA_TYPE_MAPPING.get(value_type, "str")

            if (default := value.get("default")) is not None:
                extra["value"] = default

            # This handling of the custom "unit" property only works for files exported
            # via Kadi.
            if (unit := value.get("unit")) is not None:
                extra["unit"] = unit.get("default")

            validation = {}

            if key in required_props:
                validation["required"] = True

            if (options := value.get("enum")) is not None:
                validation["options"] = options

            minimum = value.get("minimum")
            maximum = value.get("maximum")

            if minimum is not None or maximum is not None:
                validation["range"] = {"min": minimum, "max": maximum}

            if validation:
                extra["validation"] = validation

        extras.append(extra)

    return extras


def _parse_json_schema_data(import_data, template_type):
    try:
        import_data = jsonref.load(import_data)

        if not isinstance(import_data, dict):
            return None

        extras = _json_schema_to_extras(import_data.get("properties", {}))

        if template_type == TemplateType.RECORD:
            import_data = {"data": {"extras": extras}}
        elif template_type == TemplateType.EXTRAS:
            import_data = {"data": extras}

        return TemplateImportSchema(template_type=template_type, partial=True).load(
            import_data
        )
    except:
        return None


def parse_import_data(stream, import_type, template_type):
    """Parse imported template data of a given format.

    :param stream: The import data as a readable binary stream.
    :param import_type: The import type, one of ``"json"`` or ``"json-schema"``.
    :param template_type: The expected template type corresponding to the import data.
    :return: The imported template data as a dictionary. Note that none of the template
        properties are guaranteed to be present.
    """
    import_data = BytesIO(stream.read(const.IMPORT_MAX_SIZE))

    if import_type == const.IMPORT_TYPE_JSON:
        return _parse_json_data(import_data, template_type)

    if import_type == const.IMPORT_TYPE_JSON_SCHEMA:
        return _parse_json_schema_data(import_data, template_type)

    return None
