import re
from collections import OrderedDict
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


class Url:
    @classmethod
    def from_str(cls, url):
        pt = urlparse(url)
        kwargs = dict(
            url=url,
            scheme=pt.scheme,
            netloc=pt.netloc,
            path=pt.path,
            query=dict(parse_qsl(pt.query, True)),
            query_raw=pt.query,
            fragment=pt.fragment
        )
        return cls(**kwargs)

    @staticmethod
    def is_abs_url(url):
        return bool(urlparse(url).scheme)

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, item):
        return self.kwargs[item]

    def format(self, **kwargs):
        kwargs = self.kwargs | kwargs
        return urlunparse((
            kwargs.get('scheme'),
            kwargs.get('netloc'),
            kwargs.get('path') or '',
            '',
            urlencode(kwargs.get('query') or {}),
            kwargs.get('fragment')
        ))

    def sort_query(self):
        query = self.kwargs.get('query')
        if query is not None:
            self.kwargs['query'] = OrderedDict((k, query[k]) for k in sorted(query))
        return self

    @property
    def value(self):
        return self.format()

    @property
    def home(self):
        return self.format(
            path=None,
            query=None,
            fragment=None
        )

    @property
    def is_sub_site(self):
        def is_number(x):
            return re.match("^[0-9]+$", x)

        paths = self.path.split('/')
        for path in paths:
            if is_number(path):
                return True
        if paths and is_number(paths[-1].split('.', 1)[0]):
            return True
        for value in self.query.values():
            if is_number(value):
                return True
        return False


def get_auth_url(url, username, password=None):
    a, b = url.split('//', 1)
    pw = ''
    if password:
        pw = f":{password}"
    return f"{a}//{username}{pw}@{b}"


def split_auth_url(url):
    pa = urlparse(url)
    return (
        urlunparse((pa.scheme, pa.hostname, pa.path, pa.params, pa.query, pa.fragment)),
        pa.username,
        pa.password
    )
