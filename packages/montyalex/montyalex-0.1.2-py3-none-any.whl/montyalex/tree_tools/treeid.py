from montyalex.fs_tools import current_working_dir, joinpaths, pathexists, mkdirs, rmfile
from montyalex.object_tools import singleton, pdumps, ploads


@singleton(get_identifier=lambda name: name)
class FileSystemTree:
    def __init__(self, name: str):
        self.name: str = name
        self.age = 0
        self.template: str = None
        self.nodes = [0, 0, 0]
        self._path: str = joinpaths(
            current_working_dir,
            '.mtax',
            '.pkl',
            f'tree-{self.name}')
        self.exists: bool = pathexists(self._path)
    def __str__(self) -> str:
        return f"{self.__dict__}"
    def progress(self):
        self.age += 1
        self.write()
    def write(self) -> None:
        mkdirs(self._path.removesuffix(f'tree-{self.name}'), exist_ok=True)
        with open(self._path, 'wb') as tree_pkl:
            tree_pkl.write(pdumps(self.__dict__))
    def setup(self, *, template: str = None):
        if template:
            self.template = template
    def scan(self):
        if self.exists:
            with open(self._path, 'rb') as tree_pkl:
                return ploads(tree_pkl.read())
        return self.__dict__
    def delete(self):
        if self.exists:
            rmfile(self._path)


# ---------------------------------------------------------------------------
# | Example Usage
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    tree1 = FileSystemTree('name')
    print(tree1)
    print(tree1.scan())
