from fastapi import FastAPI, Request

from models import ValidationResponse
from validator import validate_xml_content

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """Check whether the API service is running.

    Returns:
        dict[str, str]: A status response indicating that the service is available.
    """
    return {"status": "ok"}


@app.post("/validate")
async def validate_xml(request: Request) -> ValidationResponse:
    """Validate XML content sent in the HTTP request body.

    Args:
        request: The incoming request containing XML data in the request body.

    Returns:
        ValidationResponse: A dictionary-like response containing:
            - `valid`: Whether the XML content passed validation
            - `errors`: A list of validation errors, if any
            - `number_errors`: The total number of validation errors found
    """
    body: bytes = await request.body()

    if not body:
        return {
            "valid": False,
            "errors": [
                {
                    "path": None,
                    "reason": "Empty request body",
                    "message": "No XML content was provided.",
                }
            ],
            "number_errors": 1,
        }

    return validate_xml_content(body)
