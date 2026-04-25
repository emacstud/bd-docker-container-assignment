import io
from functools import lru_cache
from pathlib import Path

import xmlschema

from models import ValidationErrorItem, ValidationResponse

BASE_DIR = Path(__file__).resolve().parent
XSD_FILE = BASE_DIR / "resources" / "saftpt1.04_01.xsd"


@lru_cache(maxsize=1)
def load_schema() -> xmlschema.XMLSchema11:
    """Load and cache the XSD schema.

    Returns:
        xmlschema.XMLSchema11: The loaded XML Schema 1.1 validator instance.
    """
    return xmlschema.XMLSchema11(str(XSD_FILE))


def validate_xml_content(xml_content: bytes | bytearray | str) -> ValidationResponse:
    """
    Validate XML content against the configured XSD schema.

    Args:
        xml_content: The XML content to validate.

    Returns:
        ValidationResponse: A dictionary-like response containing:
            - `valid`: Whether the XML is valid
            - `errors`: A list of validation error objects
            - `number_errors`: The number of validation errors found
    """
    try:
        schema = load_schema()

        if isinstance(xml_content, (bytes, bytearray)):
            source = io.BytesIO(xml_content)
        else:
            source = io.StringIO(str(xml_content))

        errors: list[ValidationErrorItem] = []
        for err in schema.iter_errors(source):
            path = getattr(err, "path", None)
            reason = getattr(err, "reason", None)

            errors.append(
                {
                    "path": str(path) if path is not None else None,
                    "reason": str(reason) if reason is not None else None,
                    "message": str(err),
                }
            )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "number_errors": len(errors)
        }
    
    except Exception as e:
        return {
            "valid": False,
            "errors": [
                {
                    "path": None,
                    "reason": "Validation process failed",
                    "message": str(e)
                }
            ],
            "number_errors": 1,
        }
