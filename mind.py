from pathlib import Path
import json
import shutil
from datetime import datetime

import drive


DEFAULT_MIND_PATH = 'mind.json'
DEFAULT_TEMP_PATH = 'mdmind/temp'


def read(mind_path=DEFAULT_MIND_PATH) -> set[Path]:
    with open(mind_path) as f:
        a = json.load(f)
    return {Path(i).absolute() for i in a}


def write(paths: set[Path], mind_path=DEFAULT_MIND_PATH):
    a = [str(p) for p in paths]
    with open(mind_path, "w+") as f:
        json.dump(a, f, indent=4)

def copy(paths: set[Path], dist_path):
    dist_path = Path(dist_path)
    collected_path = dist_path / 'collected'
    if dist_path.exists():
        shutil.rmtree(dist_path)
    collected_path.mkdir(parents=True)

    for p in paths:
        shutil.copytree(p, collected_path / p.name)

    file_path = dist_path / 'mdmind'
    shutil.make_archive(file_path, 'zip', collected_path)

    return file_path

def unpack(archive_path, dist_path):
    dist_path = Path(dist_path)
    extracted_path = dist_path / 'extracted'
    if dist_path.exists():
        shutil.rmtree(dist_path)
    extracted_path.mkdir(parents=True)

    shutil.unpack_archive(archive_path, extracted_path, 'zip')



def main():
    service = drive.build_service()

    unpack('temp/mdmind.zip', './adad')


if __name__ == '__main__':
    main()
