import base64
import io

import pytest

from notifications_python_client import prepare_upload


def test_prepare_upload_raises_an_error_for_large_files():
    with pytest.raises(ValueError) as exc:
        prepare_upload(io.BytesIO(b'a' * 3 * 1024 * 1024))

    assert 'larger than 2MB' in str(exc.value)


@pytest.mark.parametrize(
    'is_csv',
    (
        True,
        False,
    )
)
def test_prepare_upload_generates_expected_dict(is_csv):
    file_content = b'a' * 256
    file_dict = prepare_upload(io.BytesIO(file_content), is_csv=is_csv)

    assert file_dict['is_csv'] == is_csv
    assert file_dict['file'] == base64.b64encode(file_content).decode('ascii')
