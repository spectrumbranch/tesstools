import os
from pathlib import PurePath
import shlex
import sys

from mortar.config import config
from mortar.path import win_from_wsl
import mortar.process as process
from mortar.ssh import SSH

_tess_env = {
    'command': os.environ['TESSERACT'],
    'data': os.environ['TESSERACT_DATA']
}

_tess_cmd = [
    _tess_env['command'],
    '-l', 'jpn',
    '--tessdata-dir', f"{(_tess_env['data'])}",
    '--psm', '3',
    '--oem', '1'
]


def tesseract_ssh(path_: str) -> str:
    tess_cmd = (f"{_tess_env['command']}"
                f" -l jpn --tessdata-dir {shlex.quote(_tess_env['data'])}")

    ssh = SSH(host=config.ssh.host, port=config.ssh.port)
    path = PurePath(path_)

    temp_win = "C:\\Users\\ChillRuns\\AppData\\Local\\Temp"
    temp_nix = '/mnt/c/Users/ChillRuns/AppData/Local/Temp'

    ssh.scp_to(path, f'{temp_nix}/{path.name}')
    ssh.run([tess_cmd + f' "{temp_win}\\{path.name}" "{temp_win}\\out"'])
    ssh.scp_from(f'{temp_nix}/out.txt', '.')

    out_name = 'out.txt'

    with open(out_name, 'r') as fi:
        result = fi.read()

    os.remove(out_name)

    return result


def tesseract_wsl(path_: str) -> str:
    path = win_from_wsl(path_)
    out_stem = 'out'
    out_name = f'{out_stem}.txt'

    process.run(_tess_cmd + [path, out_stem])

    with open(out_name, 'r') as fi:
        result = fi.read()

    os.remove(out_name)

    return result


def ocr(path: str) -> str:
    """ Generate OCR text from an image in the same way MORT does. """

    if config.ssh.use_ssh:
        result = tesseract_ssh(path)
    else:
        result = tesseract_wsl(path)

    return result


def main():
    if len(sys.argv) < 2:
        raise Exception('path to image file is required')

    print(ocr(sys.argv[1]))


if __name__ == '__main__':
    main()
