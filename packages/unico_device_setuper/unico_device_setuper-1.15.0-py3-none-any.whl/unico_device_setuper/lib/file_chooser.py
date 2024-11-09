import contextlib
import pathlib
import subprocess
import typing

import plyer.platforms.macosx.filechooser
import slugify

from unico_device_setuper.lib import datadir, util


class FocusedFileChooser(plyer.platforms.macosx.filechooser.MacFileChooser):
    @property
    def title(self):
        subprocess.run(
            [
                '/usr/bin/osascript',
                '-e',
                'tell app "Finder" to set frontmost of process "Python" to true',
            ],
            check=False,
        )


def choose_files(name: str, allowed_extensions: typing.Iterable[str], *, allow_multiple: bool):
    last_filechooser_location_path = (
        datadir.get() / 'last_filechooser_locations' / f'{slugify.slugify(name)}.txt'
    )

    last_filechooser_location = None
    with contextlib.suppress(OSError):
        last_filechooser_location = pathlib.Path(last_filechooser_location_path.read_text())

    paths = (
        FocusedFileChooser(
            mode='dir_and_files',
            multiple=allow_multiple,
            filters=list(allowed_extensions),
            use_extensions=True,
            path=str(last_filechooser_location)
            if last_filechooser_location and last_filechooser_location.exists()
            else None,
        ).run()
        or []
    )

    paths = list(map(pathlib.Path, paths))

    last_filechooser_location_path.parent.mkdir(parents=True, exist_ok=True)
    if paths:
        last_filechooser_location_path.write_text(str(paths[0].parent))

    def explorer(path: pathlib.Path) -> typing.Iterator[pathlib.Path]:
        with contextlib.suppress(OSError):
            yield from path.iterdir()

    return sorted(
        (
            path
            for path in util.explore(paths, explorer)
            if path.suffix.lower() in allowed_extensions
        ),
        key=lambda p: p.name,
    )
