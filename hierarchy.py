from pathlib import Path
import json


class Archive:
    """
    Archive представляет директорию, организованную из папок, хранящих различные 
    заметки, а также файлы прилагающиеся к ним.
    """

    def __init__(self, path: str | Path, description: str=''):
        self.path = Path(path).absolute()
        self.description = description

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(str(self.path))

    def __repr__(self):
        return str(self.path)


class MindFile:
    """
    MindFile представляет общую информацию об имеющихся архивах в виде JSON 
    файла, он служит для их отслеживания и организации.
    """

    def __init__(self, path: str | Path = 'mind.json'):
        self.path = Path(path).absolute()

    def read(self) -> set[Archive]:
        with open(self.path) as f:
            dicts = json.load(f)

        archives = set()
        for d in dicts:
            archives.add(
                Archive(Path(d['path']), d['description'])
            )
        return archives

    def write(self, archives):
        dicts = []
        for a in archives:
            dicts.append(
                {'path': str(a.path), 'description': a.description}
            )

        with open(self.path, 'w+') as f:
            json.dump(dicts, f, indent=4)



if __name__ == '__main__':
    a = Archive('tmp')
    print(list(a.path.glob('**/*')))
