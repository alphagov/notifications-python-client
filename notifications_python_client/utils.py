import base64

DOCUMENT_UPLOAD_SIZE_LIMIT = 2 * 1024 * 1024


def prepare_upload(f):
    contents = f.read()

    if len(contents) > DOCUMENT_UPLOAD_SIZE_LIMIT:
        raise ValueError('Document is larger than 2MB')

    return {
        'file': base64.b64encode(contents).decode('ascii')
    }
