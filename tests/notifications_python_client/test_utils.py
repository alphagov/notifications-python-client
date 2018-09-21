import io
import pytest

from notifications_python_client import prepare_upload


def test_prepare_upload_raises_an_error_for_large_files():
    with pytest.raises(ValueError) as exc:
        prepare_upload(io.BytesIO(b'a' * 3 * 1024 * 1024))

    assert 'larger than 2MB' in str(exc.value)
