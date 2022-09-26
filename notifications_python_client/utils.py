import base64

DOCUMENT_UPLOAD_SIZE_LIMIT = 2 * 1024 * 1024


def prepare_upload(f, is_csv=False, confirm_email_before_download=None, retention_period=None):
    contents = f.read()

    if len(contents) > DOCUMENT_UPLOAD_SIZE_LIMIT:
        raise ValueError('File is larger than 2MB')

    file_data = {
        'file': base64.b64encode(contents).decode('ascii'),
        'is_csv': is_csv,
        'confirm_email_before_download': confirm_email_before_download,
        'retention_period': retention_period
    }

    return file_data
