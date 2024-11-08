"""Token module hold implementation for token objects.

We implement a token class to hold all information about an access token.
"""

from dataclasses import dataclass
from typing import Optional, Union

from ..api import DEFAULT_DEPLOYMENT_URL


@dataclass
class Token:
    """Token object, holds information about the token."""

    name: str
    book_id: int
    token: str
    deployment_url: str = DEFAULT_DEPLOYMENT_URL

    @classmethod
    def from_unsafe(
        cls,
        name: str,
        book_id: Union[str, int],
        token: str,
        deployment_url: Optional[str] = None,
    ) -> "Token":
        """Create a token object from unsafe input. I.e. optional deployment_url."""
        if deployment_url is None:
            deployment_url = DEFAULT_DEPLOYMENT_URL

        if isinstance(book_id, str):
            book_id = int(book_id)

        return cls(name, book_id, token, deployment_url)

    def __repr__(self):
        """Return a string representation of the token."""
        return f"Token(name={self.name}, book_id={self.book_id}, deployment_url={self.deployment_url})"
