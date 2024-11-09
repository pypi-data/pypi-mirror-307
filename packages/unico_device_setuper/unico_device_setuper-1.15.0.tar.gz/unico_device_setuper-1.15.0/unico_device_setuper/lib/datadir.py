import contextlib
import pathlib
import tomllib

import platformdirs

import unico_device_setuper
from unico_device_setuper.lib import util


def is_release_version():
    pyproject_path = util.module_path(unico_device_setuper).parent / 'pyproject.toml'
    with contextlib.suppress(FileNotFoundError):
        pyproject = tomllib.loads(pyproject_path.read_text())
        if pyproject.get('tool', {}).get('poetry', {}).get('name') == unico_device_setuper.__name__:
            return False
    return True


def get():
    if is_release_version():
        return pathlib.Path(platformdirs.user_data_dir(appname=util.APP_NAME)).absolute()

    return util.module_path(unico_device_setuper).parent / 'data'


@contextlib.contextmanager
def get_temporary():
    with util.temporary_dir(get()) as dir:
        yield dir
