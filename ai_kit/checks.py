from django.core.checks import Tags  # pylint: disable=redefined-builtin
from django.core.checks import Warning, register

from ai_kit.conf import settings
from ai_kit.utils.enums import LLM_PROVIDERS
from ai_kit.utils.helpers import get_nested_key_value


class Messages:
    SETTING_DEPRECATED = "You have a deprecated setting {deprecated_setting} configured in your project settings."
    REQUIRED_SETTING_MISSING = "You have a required setting {required_setting} missing in your project settings."
    NESTED_REQUIRED_VALUE_MISSING = "You have a required value missing for {missing_nested_key} in the {key} index item of {parent_key}"
    INVALID_VALUE = "You have an invalid value for {invalid_value}."
    INVALID_OPTION_VALUE = (
        "You have an invalid option value for {invalid_option_value}."
    )
    NESTED_INVALID_VALUE = "You have an invalid value for {invalid_value} in the {index} index item of {parent_key}"


class Hints:
    SETTING_DEPRECATED = None
    REQUIRED_SETTING_MISSING = None
    NESTED_REQUIRED_VALUE_MISSING = None
    INVALID_VALUE = "It needs to be a {expected_type}."
    INVALID_OPTION_VALUE = "It needs to be one of {expected_options}."


class Codes:
    SETTING_DEPRECATED = "ai_kit.W001"
    REQUIRED_SETTING_MISSING = "ai_kit.W002"
    NESTED_REQUIRED_VALUE_MISSING = "ai_kit.W003"
    INVALID_VALUE = "ai_kit.W004"
    INVALID_OPTION_VALUE = "ai_kit.W005"
    NESTED_INVALID_VALUE = "ai_kit.W006"


@register(Tags.compatibility)
def ai_kit_deprecation_check(app_configs, **kwargs):  # pylint: disable=unused-argument
    warnings = []

    deprecated_settings = []

    for deprecated_setting in deprecated_settings:
        try:
            getattr(settings, deprecated_setting)
            warnings.append(
                Warning(
                    msg=Messages.SETTING_DEPRECATED.format(
                        deprecated_setting=deprecated_setting
                    ),
                    hint=Hints.SETTING_DEPRECATED,
                    id=Codes.SETTING_DEPRECATED,
                )
            )
        except AttributeError:
            pass

    return warnings


@register(Tags.compatibility)
def ai_kit_value_check(app_configs, **kwargs):  # pylint: disable=unused-argument
    warnings = []

    required_keys = {
        "AI_KIT_MODEL_REGISTRY": {
            "checks": {
                "type": list,
                "nested_type": dict,
            },
            "children": {
                "display_name": {
                    "checks": {
                        "type": str,
                    },
                },
                "version_name": {
                    "checks": {
                        "type": str,
                    },
                },
                "provider_name": {
                    "checks": {
                        "type": str,
                        "options": ", ".join([choice[0] for choice in LLM_PROVIDERS]),
                    },
                },
                "is_enabled": {
                    "checks": {
                        "optional": True,
                        "type": bool,
                    },
                },
                "is_multimodal": {
                    "checks": {
                        "optional": True,
                        "type": bool,
                    },
                },
                "is_function_calling_supported": {
                    "checks": {
                        "optional": True,
                        "type": bool,
                    },
                },
                "description": {
                    "checks": {
                        "optional": True,
                        "type": str,
                    },
                },
                "settings": {
                    "children": {
                        "api_version": {
                            "checks": {
                                "type": str,
                                "conditional": {
                                    "attribute": "self",
                                    "child_key": "provider_name",
                                    "value": "openai",
                                },
                            },
                        },
                        "endpoint": {
                            "checks": {
                                "type": str,
                                "conditional": {
                                    "attribute": "self",
                                    "child_key": "provider_name",
                                    "value": "openai",
                                },
                            },
                        },
                        "api_key": {
                            "checks": {
                                "type": str,
                                "conditional": {
                                    "attribute": "self",
                                    "child_key": "provider_name",
                                    "value": "openai",
                                },
                            },
                        },
                        "region": {
                            "checks": {
                                "type": str,
                                "conditional": {
                                    "attribute": "self",
                                    "child_key": "provider_name",
                                    "value": "bedrock",
                                },
                            },
                        },
                        "access_key_id": {
                            "checks": {
                                "type": str,
                                "conditional": {
                                    "attribute": "self",
                                    "child_key": "provider_name",
                                    "value": "bedrock",
                                },
                            },
                        },
                        "secret_access_key": {
                            "checks": {
                                "type": str,
                                "conditional": {
                                    "attribute": "self",
                                    "child_key": "provider_name",
                                    "value": "bedrock",
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    for key, data in required_keys.items():
        value = getattr(settings, key, None)
        checks = data["checks"]
        children = data.get("children")
        warnings = enforce_checks(
            key=key,
            value=value,
            checks=checks,
            warnings=warnings,
            children=children,
        )

    return warnings


def enforce_checks(
    key: str,
    value: any,
    checks: str,
    warnings: list,
    children: dict = None,
    self: any = None,
    parents: list = [],
    index: int = None,
):
    """
    Enforce checks on a value based on the checks and children data.
    """
    if not checks:
        checks = {}

    optional = checks.get("optional")
    conditional_check = checks.get("conditional")
    type_check = checks.get("type")
    nested_type_check = checks.get("nested_type")
    options = checks.get("options")

    if optional and not value:
        return warnings

    if conditional_check:
        if conditional_check["attribute"] == "self":
            attribute_value = self
        else:
            attribute_value = getattr(settings, conditional_check["attribute"], None)

        child_key = conditional_check.get("child_key")
        conditional_value = conditional_check.get("value")
        if child_key:
            child_value = get_nested_key_value(attribute_value, child_key)
            if child_value != conditional_value:
                return warnings
        else:
            if attribute_value != conditional_value:
                return warnings

    if not value:
        parent_key = ""
        if len(parents) > 1:
            parent_key = parents[0] + f" at {parents[1]}"
            if len(parents) > 2:
                parent_key += "".join([f"[{i}]" for i in parents[2:]])

        msg = (
            Messages.REQUIRED_SETTING_MISSING.format(required_setting=key)
            if not parents
            else Messages.NESTED_REQUIRED_VALUE_MISSING.format(
                missing_nested_key=key, key=parents[-1], parent_key=parent_key
            )
        )

        warnings.append(
            Warning(
                msg=msg,
                hint=Hints.REQUIRED_SETTING_MISSING,
                id=(
                    Codes.REQUIRED_SETTING_MISSING
                    if not parents
                    else Codes.NESTED_REQUIRED_VALUE_MISSING
                ),
            )
        )

    if value and type_check and not type(value) == type_check:
        parent_key = ""
        if parents:
            if len(parents) > 1:
                parent_key = parents[0] + f" at {parents[1]}"
                if len(parents) > 2:
                    parent_key += "".join([f"[{i}]" for i in parents[2:]])

        msg = Messages.INVALID_VALUE.format(invalid_value=key)
        if parents and len(parents) > 1:
            msg = Messages.NESTED_INVALID_VALUE.format(
                invalid_value=key, index=index + 1, parent_key=parent_key
            )

        warnings.append(
            Warning(
                msg=msg,
                hint=Hints.INVALID_VALUE.format(expected_type=type_check.__name__),
                id=Codes.INVALID_VALUE if not parents else Codes.NESTED_INVALID_VALUE,
            )
        )

    if nested_type_check and isinstance(value, list):
        if not all(type(item) == nested_type_check for item in value):
            parent_key = ""
            if parents:
                if len(parents) > 1:
                    parent_key = parents[0] + f" at {parents[1]}"
                    if len(parents) > 2:
                        parent_key += "".join([f"[{i}]" for i in parents[2:]])

            msg = Messages.INVALID_VALUE.format(invalid_value=key)
            if parents and len(parents) > 1:
                msg = Messages.NESTED_INVALID_VALUE.format(
                    invalid_value=key, index=index + 1, parent_key=parent_key
                )

            warnings.append(
                Warning(
                    msg=msg,
                    hint=Hints.INVALID_VALUE.format(
                        expected_type=f"{type_check.__name__}[{nested_type_check.__name__}]"
                    ),
                    id=(
                        Codes.INVALID_VALUE
                        if not parents
                        else Codes.NESTED_INVALID_VALUE
                    ),
                )
            )
            return warnings

    if options and value:
        if isinstance(value, str) and value not in options:
            warnings.append(
                Warning(
                    msg=Messages.INVALID_OPTION_VALUE.format(invalid_option_value=key),
                    hint=Hints.INVALID_OPTION_VALUE.format(expected_options=options),
                    id=Codes.INVALID_OPTION_VALUE,
                )
            )
        elif isinstance(value, list) and not all(v in options for v in value):
            warnings.append(
                Warning(
                    msg=Messages.INVALID_OPTION_VALUE.format(invalid_option_value=key),
                    hint=Hints.INVALID_OPTION_VALUE.format(expected_options=options),
                    id=Codes.INVALID_OPTION_VALUE,
                )
            )

    if children:
        if isinstance(value, list):
            for index, item in enumerate(value):
                self = item
                if isinstance(item, dict):
                    warnings = child_checks(
                        value=item,
                        warnings=warnings,
                        children=children,
                        self=self,
                        parents=parents + [key],
                        index=index,
                    )
        elif isinstance(value, dict):
            warnings = child_checks(
                value=value,
                warnings=warnings,
                children=children,
                self=self,
                parents=parents + [key],
                index=index,
            )

    return warnings


def child_checks(
    value: dict,
    warnings: list,
    children: dict = None,
    self: any = None,
    parents: list = [],
    index: int = None,
):
    for child_key, child_data in children.items():
        child_value = value.get(child_key)
        child_checks = child_data.get("checks")
        child_children = child_data.get("children")

        warnings = enforce_checks(
            key=child_key,
            value=child_value,
            checks=child_checks,
            warnings=warnings,
            children=child_children,
            self=self,
            parents=parents,
            index=index,
        )

    return warnings
