from mimetypes import MimeTypes

mimetypes = MimeTypes()

custom_types = {
    'text/javascript': '.js',
    'application/x-javascript': '.js'
}

for k, v in custom_types.items():
    mimetypes.add_type(k, v)


def ct_to_mt(content_type):
    return content_type.partition(';')[0].strip()
