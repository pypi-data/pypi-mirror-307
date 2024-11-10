from collections import Counter
from montyalex.fs_tools import joinpaths, current_working_dir


def find_duplicates(nonunique_list: list[str], obj: object):
    counts = Counter(nonunique_list)
    duplicates = {item: count for item, count in counts.items() if count > 1}

    if duplicates:
        print(f"{obj} name duplicates found:")
        for item, count in duplicates.items():
            print(f"'{item}' is repeated {count} times")

    return duplicates

class NamedEmptyFile:
    def __init__(self, name: str) -> None:
        self.file_name: str = name

    def __str__(self) -> str:
        return 'File'

class NamedDirectory:
    def __init__(self, name: str) -> None:
        self.directory_name: str = name

    def __str__(self) -> str:
        return 'Directory'

class Tree:
    def __init__(
        self,
        name: str,
        directories: set[NamedDirectory],
        files: set[NamedEmptyFile]) -> None:
        self.name: str = name
        self.named_directories: set[NamedDirectory] = directories
        self.named_files: set[NamedEmptyFile] = files

class VoidTree:
    def __init__(self, name: str) -> None:
        self.name = name
        self.os_path = joinpaths(current_working_dir, self.name)
        self.directory_set: set[NamedDirectory] = set()
        self.file_set: set[NamedEmptyFile] = set()
        self.tree = Tree(self.name, self.directory_set, self.file_set)

    def _add_directory_set(self, directory_set: set[NamedDirectory]):
        self.directory_set = directory_set
        self.tree.named_directories = self.directory_set

    def _add_file_set(self, file_set: set[NamedEmptyFile]):
        self.file_set = file_set
        self.tree.named_files = self.file_set

    def add_directories(self, directories: list[NamedDirectory]):
        find_duplicates(directories, NamedDirectory(''))
        self._add_directory_set(set(directories))

    def add_files(self, files: list[NamedEmptyFile]):
        find_duplicates(files, NamedEmptyFile(''))
        self._add_file_set(set(files))

    def get_tree(self):
        return self.tree.name

    def get_directories(self) -> set:
        return self.directory_set

    def get_files(self) -> set:
        return self.file_set

    def display_tree(self):
        tree = self.get_tree()
        print(tree)

    def display_directories(self):
        directories = self.get_directories()
        if directories:
            print(f'{directories!r}')

    def display_files(self):
        files = self.get_files()
        if files:
            print(f'{files!r}')


dirs_ = [
    # "dir1",
    # "dir2",
    # "dir2",
    # "dir2",
    # "dir2",
    # "dir2",
    # "dir2",
    # "dir3",
]

files_ = [
    # "file1",
    # "file2",
    # "file2",
    # "file2",
    # "file2",
    # "file2",
    # "file2",
    # "file2",
    # "file4",
    # "file3",
    # "file3",
]

void = VoidTree('name')

void.add_directories(dirs_)
void.add_files(files_)

void.display_tree()
void.display_directories()
void.display_files()
