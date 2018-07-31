import base64


def prepare_upload(f):
    return {
        'file': base64.b64encode(f.read()).decode('ascii')
    }
