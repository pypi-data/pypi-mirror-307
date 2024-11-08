import pytest
from snip.token.token import Token

MOCK_DATA_1 = """
[any_name]
deployment = dep_1
book_id = 1
token = token

[no_deployment]
book_id = 1
token = token
"""

OVERWRITE_DATA = """
[any_name]
deployment = dep_1
book_id = 1
token = overwritten_token
"""

INVALID_DATA = """
[missing_book_id]
deployment = dep_1
token = another_token
"""


@pytest.fixture(scope="session", params=[0, 1, 2])
def config_file(request, tmp_path_factory):
    # Create a temporary file
    config_file = tmp_path_factory.mktemp("data") / "config.ini"
    config_file.write_text(
        """
        [any_name]
        deployment = dep_1
        book_id = 1
        token = token

        [no_deployment]
        book_id = 1
        token = token
        """
    )

    tokens = [
        Token(
            "any_name",
            1,
            "token",
            "dep_1",
        ),
        Token(
            "no_deployment",
            1,
            "token",
        ),
    ]

    return config_file, tokens


@pytest.fixture(scope="session")
def another_config_file(tmp_path_factory):
    # Create a temporary file
    config_file = tmp_path_factory.mktemp("data") / "config.ini"
    config_file.write_text(
        """
[any_name]
deployment = dep_1
book_id = 1
token = overwritten_token
"""
    )
    return config_file, (
        Token(
            "any_name",
            1,
            "token",
            "dep_1",
        ),
    )


@pytest.fixture(scope="session")
def invalid_config_file(tmp_path_factory):
    # Create a temporary file
    config_file = tmp_path_factory.mktemp("data") / "config.ini"
    config_file.write_text(
        """
[missing_book_id]
deployment = dep_1
token = another_token
"""
    )

    return config_file, ()


from keyring.backend import KeyringBackend


class TempKeyring(KeyringBackend):
    """A temporary keyring backend that stores passwords in memory."""

    priority = 100.0  # type: ignore
    name = "Temp"  # type: ignore

    def __init__(self, error=False):
        self.error = error
        self._passwords = {}

    def set_password(self, service, username, password):
        """Set the password for the given service and username."""
        key = (service, username)
        self._passwords[key] = password

    def get_password(self, service, username):
        """Get the password for the given service and username."""
        if self.error:
            raise Exception("Test")
        key = (service, username)
        return self._passwords.get(key)

    def delete_password(self, service, username):
        """Delete the password for the given service and username."""
        key = (service, username)
        if key in self._passwords:
            del self._passwords[key]


@pytest.fixture()
def dummy_keyring():
    kr = TempKeyring()

    return kr


@pytest.fixture(scope="session")
def tokens():
    return (
        Token("test", 1, "token", "dep_1"),
        Token("test2", 2, "token2"),
    )
