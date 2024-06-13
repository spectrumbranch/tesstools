from os import makedirs, walk
from pathlib import Path

from mortar.config import config
from mortar.process import run


def _flatten(entry) -> list[Path]:
    dir = entry[0]
    files = entry[2]

    return [Path(dir, file) for file in files]


def _files() -> list[Path]:
    top = Path(config.data, 'jp')

    dirs = list(walk(top))

    with_files = list(filter(lambda x: len(x[2]) != 0, dirs))

    files = [_flatten(x) for x in with_files]

    flat_files = [x for xs in files for x in xs]

    return flat_files


def extract_frames() -> None:
    files = _files()

    mkv_files = list(filter(lambda x: x.suffix == '.mkv', files))

    for file in mkv_files[0:1]:
        parent = file.parent
        out_dir = Path(parent, 'png')
        out_template = Path(out_dir, f'{file.stem}-%02d.png')

        makedirs(out_dir, exist_ok=True)

        command = ['ffmpeg', '-i', file, '-r', '1', out_template]

        print(f'{file.name}...')

        run(command)


def main() -> None:
    extract_frames()
