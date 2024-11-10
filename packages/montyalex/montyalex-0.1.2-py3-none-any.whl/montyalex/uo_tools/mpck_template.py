from montyalex.uo_tools._useroptions import UserOptions


class MpckOptions(UserOptions):
    def __init__(self, *, directory: str = '.mtax', filename: str = 'settings') -> None:
        super().__init__(
            json=False, toml=False, yaml=False, mpck=True, directory=directory, filename=filename)
