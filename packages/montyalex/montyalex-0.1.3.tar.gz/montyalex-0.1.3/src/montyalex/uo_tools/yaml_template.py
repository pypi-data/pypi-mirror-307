from montyalex.uo_tools._useroptions import UserOptions


class YamlOptions(UserOptions):
    def __init__(self, *, directory: str = '.mtax', filename: str = 'settings') -> None:
        super().__init__(
            json=False, toml=False, yaml=True, mpck=False, directory=directory, filename=filename)
