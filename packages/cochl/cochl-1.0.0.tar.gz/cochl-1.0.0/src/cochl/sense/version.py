import warnings

from . import __version__
from .http_request import HttpRequest, RequestException


def check_latest_lib_version(host: str):
    url = f'{host}/client-libraries/versions'
    params = {'current_version': __version__}

    try:
        response = HttpRequest.get(url, params=params)
        if response.status_code == 200:
            supported_versions = response.json().get('supported_versions')

            if __version__ not in supported_versions:
                warnings.warn(
                    f'Warning! The library version is outdated. '
                    f'Please upgrade the library: supported versions {", ".join(supported_versions)}',
                    stacklevel=3
                )
        else:
            pass
    except RequestException as _e:
        pass
