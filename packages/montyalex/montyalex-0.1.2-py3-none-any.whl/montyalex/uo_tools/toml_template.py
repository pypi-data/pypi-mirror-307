from montyalex.uo_tools._useroptions import UserOptions


class TomlOptions(UserOptions):
    def __init__(self, *, directory: str = '.mtax', filename: str = 'settings') -> None:
        super().__init__(
            json=False, toml=True, yaml=False, mpck=False, directory=directory, filename=filename)
