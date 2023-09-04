from pathlib import Path
from dataclasses import dataclass
import pathlib
import json

@dataclass
class Archive:
    """
    Archive представляет директорию, организованную из папок, хранящих различные заметки,
    а также файлы прилагающиеся к ним.
    """
    path: Path
    description: str

    def __repr__(self):
        return str(self.path)



class Mind:
    """
    Mind представляет общую информацию об имеющихся архивах в виде json файла, он служит
    для их отслеживания и организации.
    """
    def __init__(self, path='mind.json'):
        self.path = Path(path).absolute()
        with open(path) as f:
            d = json.load(f)

        self.archives = []
        for e in d:
            desc = d['descris']

            self.archives.append(
                Archive(Path(e['path']).absolute(), e['description'])
            )

    def remove(self, archive: str | Archive):
        ...

    def write(self):
        ...

    def __str__(self):
        return str(self.archives)


if __name__ == '__main__':
    print(Mind())