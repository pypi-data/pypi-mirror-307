"""Get available resources from the skaha server."""

from typing import Any, Dict

from pydantic import model_validator
from requests.models import Response
from typing_extensions import Self

from skaha.client import SkahaClient


class Context(SkahaClient):
    """Get available resources from the skaha server."""

    @model_validator(mode="after")
    def _set_server(self) -> Self:
        """Sets the server path after validation."""
        self.server = f"{self.server}/{self.version}/context"  # type: ignore
        return self

    def resources(self) -> Dict[str, Any]:
        """Get available resources from the skaha server.

        Returns:
            A dictionary of available resources.

        Examples:
            >>> from skaha.context import Context
            >>> context = Context()
            >>> context.resources()
            {'defaultCores': 2,
             'defaultCoresHeadless': 1,
             'availableCores': [1, 2, 4, 8, 16],
             'defaultRAM': 16,
             'defaultRAMHeadless': 4,
             'availableRAM': [1, 2, 4, 8, 16, 32, 64, 128, 192],
             'availableGPUs': [1,2,3,...],
            }
        """
        response: Response = self.session.get(url=self.server)  # type: ignore
        response.raise_for_status()
        return response.json()
