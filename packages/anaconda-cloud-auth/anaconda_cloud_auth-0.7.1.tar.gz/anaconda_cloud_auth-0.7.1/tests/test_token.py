import platform
from pathlib import Path

import pytest
from keyring.errors import PasswordDeleteError
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from anaconda_cloud_auth.actions import logout
from anaconda_cloud_auth.config import AnacondaCloudConfig
from anaconda_cloud_auth.token import TokenExpiredError
from anaconda_cloud_auth.token import TokenInfo
from anaconda_cloud_auth.token import TokenNotFoundError


def test_expired_token_error(outdated_token_info: TokenInfo) -> None:
    with pytest.raises(TokenExpiredError):
        _ = outdated_token_info.get_access_token()


def test_token_not_found() -> None:
    config = AnacondaCloudConfig()

    with pytest.raises(TokenNotFoundError):
        _ = TokenInfo.load(config.domain)

    with pytest.raises(TokenNotFoundError):
        _ = TokenInfo(domain=config.domain).get_access_token()


def test_logout_multiple_okay(mocker: MockerFixture) -> None:
    """We can logout multiple times and no exception is raised."""
    import keyring

    delete_spy = mocker.spy(keyring, "delete_password")

    config = AnacondaCloudConfig(domain="test")
    token_info = TokenInfo(api_key="key", domain=config.domain)
    token_info.save()

    for _ in range(2):
        logout(config)

    delete_spy.assert_called_once()


def test_preferred_token_storage(monkeypatch: MonkeyPatch) -> None:
    import keyring.backend

    backends = {k.name: k for k in keyring.backend.get_all_keyring()}

    assert "token AnacondaKeyring" in backends
    assert backends["token AnacondaKeyring"].priority == 11.0
    assert (
        backends["token AnacondaKeyring"].priority
        > backends["chainer ChainerBackend"].priority
    )

    monkeypatch.setenv("ANACONDA_CLOUD_PREFERRED_TOKEN_STORAGE", "system")
    backends = {k.name: k for k in keyring.backend.get_all_keyring()}

    assert "token AnacondaKeyring" in backends
    assert backends["token AnacondaKeyring"].priority == 0.2
    assert (
        backends["token AnacondaKeyring"].priority
        < backends["chainer ChainerBackend"].priority
    )


def test_anaconda_keyring_save_delete(tmp_path: Path) -> None:
    from anaconda_cloud_auth.token import AnacondaKeyring

    fn = tmp_path / "keyring"
    AnacondaKeyring.keyring_path = fn
    assert AnacondaKeyring.viable

    anaconda_keyring = AnacondaKeyring()

    assert anaconda_keyring.get_password("s", "u") is None

    with pytest.raises(PasswordDeleteError):
        anaconda_keyring.delete_password("s", "u")

    anaconda_keyring.set_password("s", "u", "p")
    assert anaconda_keyring.keyring_path.exists()
    assert anaconda_keyring.keyring_path.read_text() == '{"s": {"u": "p"}}'

    anaconda_keyring.set_password("s", "u2", "p")
    assert anaconda_keyring.keyring_path.read_text() == '{"s": {"u": "p", "u2": "p"}}'

    assert anaconda_keyring.viable

    assert anaconda_keyring.get_password("s", "u") == "p"
    assert anaconda_keyring.get_password("s", "u3") is None

    anaconda_keyring.delete_password("s", "u")
    assert anaconda_keyring.keyring_path.read_text() == '{"s": {"u2": "p"}}'

    anaconda_keyring.set_password("s2", "u", "p")
    assert (
        anaconda_keyring.keyring_path.read_text()
        == '{"s": {"u2": "p"}, "s2": {"u": "p"}}'
    )

    anaconda_keyring.delete_password("s", "u2")
    assert anaconda_keyring.keyring_path.read_text() == '{"s": {}, "s2": {"u": "p"}}'

    with pytest.raises(PasswordDeleteError):
        anaconda_keyring.delete_password("s", "u2")

    assert anaconda_keyring.get_password("s3", "u4") is None


def test_anaconda_keyring_empty(tmp_path: Path) -> None:
    fn = tmp_path / "keyring"
    fn.touch()
    assert fn.exists()

    from anaconda_cloud_auth.token import AnacondaKeyring

    AnacondaKeyring.keyring_path = fn

    anaconda_keyring = AnacondaKeyring()
    assert anaconda_keyring.get_password("s", "u") is None

    with pytest.raises(PasswordDeleteError):
        anaconda_keyring.delete_password("s", "u")


@pytest.mark.skipif(
    platform.system() == "Windows", reason="This has been hard to test in CI/CD"
)
def test_anaconda_keyring_not_writable() -> None:
    from anaconda_cloud_auth.token import AnacondaKeyring

    if platform.system() == "Windows":
        root = Path("c:\\windows")
    else:
        root = Path("/root")
    AnacondaKeyring.keyring_path = root / "keyring"

    assert not AnacondaKeyring.viable


def test_anaconda_keyring_domain_migration(mocker: MockerFixture) -> None:
    import keyring
    import anaconda_cloud_auth.token

    mocker.patch.dict(anaconda_cloud_auth.token.MIGRATIONS, {"modern": "legacy"})

    # First make a token in the keyring with the legacy domain
    legacy_token = TokenInfo(
        api_key="one key to rule them all", domain="legacy", version=None
    )
    assert legacy_token.version is None
    legacy_token.save()

    payload = keyring.get_password(anaconda_cloud_auth.token.KEYRING_NAME, "legacy")
    assert payload

    decoded = TokenInfo._decode(payload)
    assert "version" not in decoded

    payload = keyring.get_password(anaconda_cloud_auth.token.KEYRING_NAME, "modern")
    assert payload is None

    # Now when loaded the keyring username will switch from legacy to modern
    token = TokenInfo.load(domain="modern")
    assert token.api_key == "one key to rule them all"
    assert token.version == 1

    payload = keyring.get_password(anaconda_cloud_auth.token.KEYRING_NAME, "legacy")
    assert payload is None

    payload = keyring.get_password(anaconda_cloud_auth.token.KEYRING_NAME, "modern")
    assert payload

    decoded = TokenInfo._decode(payload)
    assert decoded["version"] == 1
