from montyalex.uo_tools._useroptions import UserOptions


class JsonSchemaOptions(UserOptions):
    def __init__(self, *, directory: str = '.mtax', filename: str = 'schema') -> None:
        super().__init__(
            json=True, toml=False, yaml=False, mpck=False, directory=directory, filename=filename)
