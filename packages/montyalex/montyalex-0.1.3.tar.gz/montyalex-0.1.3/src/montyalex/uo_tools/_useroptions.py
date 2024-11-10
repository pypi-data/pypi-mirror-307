from montyalex.console_tools import richconsole
from montyalex.fs_tools.paths import rmfile
from montyalex.typing_tools import Any, Dict
from montyalex.uo_tools._template import UserTemplate

print = richconsole.print


def unpack(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    items: Dict[str, Any] = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(unpack(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

class UserOptions(UserTemplate):
    def __init__(
        self,
        *,
        json: bool = False,
        toml: bool = False,
        yaml: bool = False,
        mpck: bool = False,
        directory: str = '.mtax',
        filename: str = 'settings') -> None:
        super().__init__(json, toml, yaml, mpck, directory, filename)

    @property
    def options(self) -> Dict[str, Any]:
        return getattr(self, self.modelname)(read=True)

    @property
    def unpacked(self) -> Dict[str, Any]:
        return unpack

    @property
    def items(self):
        return self.options.items

    def remove(self):
        rmfile(self.modelpath)

    def change(self, key: str, value: Any, append: bool = True, overwrite: bool = False):
        d = {f"{key}": value}
        self.model(d, write=True, append=append, overwrite=overwrite)

    def inspect(
        self,
        mem_alloc: bool = False,
        representation: bool = False,
        full: bool = False,
        key: str = None):
        if key:
            third = None
            match self.modelname:
                case 'json':
                    if ':' in key:
                        first, second = key.split(':', maxsplit=1)
                        if ':' in second:
                            third = key.split(':', maxsplit=1)[1]
                        if third:
                            print(self.mpck(read=True)[f"{first}"][f"{second}"][f"{third}"])
                        else:
                            print(self.json(read=True)[f"{first}"][f"{second}"])
                    else:
                        print(self.json(read=True)[f"{key}"])
                case 'toml':
                    if ':' in key:
                        first, second = key.split(':', maxsplit=1)
                        if ':' in second:
                            third = key.split(':', maxsplit=1)[1]
                        if third:
                            print(self.mpck(read=True)[f"{first}"][f"{second}"][f"{third}"])
                        else:
                            print(self.toml(read=True)[f"{first}"][f"{second}"])
                    else:
                        print(self.toml(read=True)[f"{key}"])
                case 'yaml':
                    if ':' in key:
                        first, second = key.split(':', maxsplit=1)
                        if ':' in second:
                            third = key.split(':', maxsplit=1)[1]
                        if third:
                            print(self.mpck(read=True)[f"{first}"][f"{second}"][f"{third}"])
                        else:
                            print(self.yaml(read=True)[f"{first}"][f"{second}"])
                    else:
                        print(self.yaml(read=True)[f"{key}"])
                case 'mpck':
                    if ':' in key:
                        first, second = key.split(':', maxsplit=1)
                        if ':' in second:
                            third = key.split(':', maxsplit=1)[1]
                        if third:
                            print(self.mpck(read=True)[f"{first}"][f"{second}"][f"{third}"])
                        else:
                            print(self.mpck(read=True)[f"{first}"][f"{second}"])
                    else:
                        print(self.mpck(read=True)[f"{key}"])
        else:
            if self.exists:
                print(f'Found! [green]{self.modelpath}[/]')
                if full:
                    print("\n[green]User Options:[/]")
                if mem_alloc or full:
                    print(f'[bold dim]{self.options.keys}[/]')
                if representation or full:
                    print(f'[dim]{self.options.keys()}[/]')
                if mem_alloc or full:
                    print(f'[bold dim]{self.options.values}[/]')
                if representation or full:
                    print(f'[dim]{self.options.values()}[/]')
                if full:
                    print(f'{self.options}')
                print("\n[green]Iterated Items:[/]")
                if mem_alloc or full:
                    print(f'[bold dim]{self.items}[/]')
                print(f'[dim]{self.options}[/]')
                if representation or full:
                    print(f'[dim italic]{self.items()}[/]')
                for _k, _val in self.items():
                    print(f'{_k}: {_val}')
                print("\n[green]Unpacked Items:[/]")
                if mem_alloc or full:
                    print(f'[bold dim]{self.unpacked!r}[/]')
                print(f'[dim]{self.unpacked(self.options)}[/]')
                if representation or full:
                    print(f'[dim italic]{self.unpacked(self.options).items()}[/]')
                for _k, _val in self.unpacked(self.options).items():
                    print(f'{_k}: {_val}')
                print('')
            else:
                print(f'Not Found! [red]{self.modelpath}[/]')


# ---------------------------------------------------------------------------
# | Example Usage
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    json_user_options = UserOptions(json=True)
    juo = json_user_options

# ---------------------------------------------------------------------------
# | Run either A|B if there is not an initialized file with elements
# ---------------------------------------------------------------------------
    # Run this if you would like to start from scratch or use overwrite
    # juo.remove()

    # (A)
    # d: Dict[str, Any] = {"": ""}  # Use this to add items
    # juo.model(d, write=True)  # Set overwrite=True if the file exists before running

    # (B)
    # juo.change(key='', value='')  # Or use this independently

    juo.inspect()
