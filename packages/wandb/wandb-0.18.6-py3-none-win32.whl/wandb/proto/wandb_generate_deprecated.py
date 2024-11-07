#!/usr/bin/env python


def generate_deprecated_class_definition() -> None:
    """Generate a class definition listing the deprecated features.
    This is to allow static checks to ensure that proper field names are used.
    """
    from wandb.proto.wandb_telemetry_pb2 import Deprecated  # type: ignore[import]

    deprecated_features = Deprecated.DESCRIPTOR.fields_by_name.keys()

    code: str = (
        "# Generated by wandb/proto/wandb_internal_codegen.py.  DO NOT EDIT!\n\n\n"
        "import sys\n\n\n"
        "if sys.version_info >= (3, 8):\n"
        "    from typing import Literal\n"
        "else:\n"
        "    from typing_extensions import Literal\n\n\n"
        "DEPRECATED_FEATURES = Literal[\n"
        + ",\n".join(f'    "{feature}"' for feature in deprecated_features)
        + ",\n"
        + "]\n\n\n"
        "class Deprecated:\n"
        + "".join(
            [
                f'    {feature}: DEPRECATED_FEATURES = "{feature}"\n'
                for feature in deprecated_features
            ]
        )
    )
    with open("wandb_deprecated.py", "w") as f:
        f.write(code)

generate_deprecated_class_definition()
