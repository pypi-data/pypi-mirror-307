import contextlib
import dataclasses

import httpx

from unico_device_setuper.lib import adb, cnsl, datadir, dl, pkg, rl, util

APK_DOWNLOAD_URL = rl.Url(
    'https://github.com/appium/io.appium.settings/releases/download/v5.12.16/settings_apk-debug.apk'
)


@dataclasses.dataclass
class InstalledAppiumSettings:
    version: str
    check_sum: str


@dataclasses.dataclass
class AppiumSettings:
    adb_ctx: adb.Adb

    PACKAGE_NAME = 'io.appium.settings'

    @classmethod
    @contextlib.asynccontextmanager
    async def make(cls, adb_ctx: adb.Adb, http_client: httpx.AsyncClient):
        apk_path = datadir.get() / 'appium_settings.apk'
        if not util.is_file(apk_path):
            await dl.download_url(APK_DOWNLOAD_URL, apk_path, http_client, label=apk_path.name)

        if cls.PACKAGE_NAME not in await pkg.get_apk_path_map(adb_ctx):
            with cnsl.step('Installation de Appium settings'):
                await adb_ctx.install(apk_path)

        await adb_ctx.shell(f'appops set {cls.PACKAGE_NAME} android:mock_location allow')
        await adb_ctx.shell(f'pm grant {cls.PACKAGE_NAME} android.permission.ACCESS_FINE_LOCATION')

        try:
            yield AppiumSettings(adb_ctx=adb_ctx)
        finally:
            with contextlib.suppress(util.SubprocessError):
                await adb_ctx.shell(f'am stopservice {cls.PACKAGE_NAME}/.LocationService')
            with contextlib.suppress(util.SubprocessError):
                await adb_ctx.shell(f'appops set {cls.PACKAGE_NAME} android:mock_location deny')
