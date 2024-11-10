from .console_tools import richconsole
from .typer_tools import Option, Typer
from .uo_tools import schema, json, toml, yaml, mpck
from .us_tools import SETTINGS

print = richconsole.print


settings_: Typer = Typer(
    name='settings',
    add_help_option=False,
    pretty_exceptions_show_locals=False)

init_obj = {
    "action.dirs.datetime": {
        "default.opt.four-week-month": False,
        "default.opt.format": "%Y-%m-%d",
        "default.opt.range": "1yr"
    },
    "action.dirs.simple": {
        "default.opt.range": 1
    },
    "action.opt.silent": False,
    "default.info.timezone": None,
    "user.locale.city": None,
    "user.locale.continent": None,
    "user.locale.country": None,
    "user.locale.state": None,
    "user.locale.street-name": None,
    "user.locale.street-number": None
}

schema_obj = {
    "description": "",
    "type": "object",
    "properties": {
        "action.dirs.datetime": {
            "description": "",
            "type": "object",
            "properties": {
                "default.opt.four-week-month": {
                    "description": "Use a four week (28d) range instead of a complete month",
                    "type": ["boolean", "null"],
                    "default": False
                },
                "default.opt.format": {
                    "description": "Change the date format used for folders",
                    "type": ["string", "null"],
                    "default": "%Y-%m-%d"
                },
                "default.opt.range": {
                    "description": "",
                    "type": ["string", "null"],
                    "default": "1yr"
                }
            }
        },
        "action.dirs.simple": {
            "description": "",
            "type": "object",
            "properties": {
                "default.opt.range": {
                    "description": "",
                    "type": ["integer", "null"],
                    "default": 1
                }
            }
        },
        "action.opt.silent": {
            "description": "",
            "type": ["boolean", "null"],
            "default": False
        },
        "default.info.timezone": {
            "description": "Default timezone used for date related commands",
            "type": ["string", "null"]
        }
    }
}

def _schema_init(dirname: str = '.mtax', filename: str = 'schema'):
    _schema = schema(directory=dirname, filename=filename)
    _schema.change('$schema', 'http://json-schema.org/draft-07/schema#')
    _schema.change('$id', 'montyalex.python-cli.settings-v0.1.3')
    _schema.change('title', 'Settings')
    _schema.change('description', 'MontyAlex CLI Settings')
    _schema.change('type', 'object')
    _schema.change('properties', {"mtax": schema_obj})
    _schema.change('required', ["mtax"])

@settings_.command(name='init', add_help_option=False)
def init_(
    dirname: str = Option('.mtax', '--directory-name', '-dir'),
    filename: str = Option('settings', '--file-name', '-name'),
    *,
    overwrite: bool = Option(False, '--overwrite', '-o'),
    use_all: bool = Option(False, '--all', '-a'),
    use_synced: bool = Option(False, '--sync', '-s'),
    use_json: bool = Option(False, '--json', '-j'),
    use_toml: bool = Option(False, '--toml', '-t'),
    use_yaml: bool = Option(False, '--yaml', '-y'),
    use_mpck: bool = Option(False, '--mpck', '-m')):
    uo: json | toml | yaml | mpck | None = None
    if use_json:
        uo = json(directory=dirname, filename=filename)
    if use_toml:
        uo = toml(directory=dirname, filename=filename)
    if use_yaml:
        uo = yaml(directory=dirname, filename=filename)
    if use_mpck:
        uo = mpck(directory=dirname, filename=filename)
    if uo is None:
        uo = json(directory=dirname, filename=filename)

    if not use_all or use_synced:
        if overwrite:
            if isinstance(uo, json):
                uo.change('$schema', './schema.json')
                _schema_init(dirname)
            uo.change('mtax', init_obj, append=False)
        else:
            if isinstance(uo, json):
                uo.change('$schema', './schema.json')
                _schema_init(dirname)
            if isinstance(uo, toml):
                uo.change('mtax', {
                    "action.dirs.datetime": {
                        "default.opt.four-week-month": False,
                        "default.opt.format": "%Y-%m-%d",
                        "default.opt.range": "1yr"
                    },
                    "action.dirs.simple": {
                        "default.opt.range": 1
                    },
                    "action.opt.silent": False,
                    "default.info.timezone": "",
                    "user.locale.city": "",
                    "user.locale.continent": "",
                    "user.locale.country": "",
                    "user.locale.state": "",
                    "user.locale.street-name": "",
                    "user.locale.street-number": ""
                })
            else:
                uo.change('mtax', init_obj)
    else:
        juo = json(directory=dirname, filename=filename)
        tuo = toml(directory=dirname, filename=filename)
        yuo = yaml(directory=dirname, filename=filename)
        muo = mpck(directory=dirname, filename=filename)
        if overwrite:
            juo.change('$schema', './schema.json')
            _schema_init(dirname)
            juo.change('mtax', init_obj)
            tuo.change('mtax', {
                "action.dirs.datetime": {
                    "default.opt.four-week-month": False,
                    "default.opt.range": "1yr"
                },
                "action.dirs.simple": {
                    "default.opt.range": 1
                },
                "action.opt.silent": False,
                "default.info.timezone": "",
                "user.locale.city": "",
                "user.locale.continent": "",
                "user.locale.country": "",
                "user.locale.state": "",
                "user.locale.street-name": "",
                "user.locale.street-number": ""
            }, append=False)
            yuo.change('mtax', init_obj, append=False)
            muo.change('mtax', init_obj, append=False)
        else:
            juo.change('$schema', './schema.json')
            _schema_init(dirname)
            juo.change('mtax', init_obj)
            tuo.change('mtax', {
                "action.dirs.datetime": {
                    "default.opt.four-week-month": False,
                    "default.opt.range": "1yr"
                },
                "action.dirs.simple": {
                    "default.opt.range": 1
                },
                "action.opt.silent": False,
                "default.info.timezone": "",
                "user.locale.city": "",
                "user.locale.continent": "",
                "user.locale.country": "",
                "user.locale.state": "",
                "user.locale.street-name": "",
                "user.locale.street-number": ""
            })
            yuo.change('mtax', init_obj)
            muo.change('mtax', init_obj)

@settings_.command(name='list', add_help_option=False)
def list_(
    repr_listing: bool = Option(False, '--repr', '-r'),
):
    if repr_listing:
        print(f'{SETTINGS!r}')
    else:
        SETTINGS.show_all_values()

@settings_.command(name='delete', add_help_option=False)
def delete_(
    dirname: str = Option('.mtax', '--directory-name', '-dir'),
    filename: str = Option('settings', '--file-name', '-name'),
    key: str = Option(None, '--key', '-k'),
    *,
    use_json: bool = Option(False, '--json', '-j'),
    use_toml: bool = Option(False, '--toml', '-t'),
    use_yaml: bool = Option(False, '--yaml', '-y'),
    use_mpck: bool = Option(False, '--mpck', '-m')):
    uo: json | toml | yaml | mpck | None = None
    if use_json:
        uo = json(directory=dirname, filename=filename)
    if use_toml:
        uo = toml(directory=dirname, filename=filename)
    if use_yaml:
        uo = yaml(directory=dirname, filename=filename)
    if use_mpck:
        uo = mpck(directory=dirname, filename=filename)
    if uo is None:
        uo = json(directory=dirname, filename=filename)

    if key:
        uo.change(key, None, overwrite=True)
    uo.remove()

def inspect_initialize(uo, dirname, filename, use_json, use_toml, use_yaml, use_mpck):
    if not uo.exists:
        print('Creating new settings file...')
        init_(
            dirname=dirname,
            filename=filename,
            overwrite=False,
            use_json=use_json,
            use_toml=use_toml,
            use_yaml=use_yaml,
            use_mpck=use_mpck)

@settings_.command(name='inspect', add_help_option=False)
def inspect_(
    dirname: str = Option('.mtax', '--directory-name', '-dir'),
    filename: str = Option('settings', '--file-name', '-name'),
    use_json: bool = Option(False, '--json', '-j'),
    use_toml: bool = Option(False, '--toml', '-t'),
    use_yaml: bool = Option(False, '--yaml', '-y'),
    use_mpck: bool = Option(False, '--mpck', '-m'),
    full_inspection: bool = Option(False, '--full', '-fi'),
    mem_alloc_inspection: bool = Option(False, '--memory', '-mi'),
    repr_inspection: bool = Option(False, '--repr', '-ri'),
    exists_inspection: bool = Option(False, '--exists', '-ei'),
    key_inspection: str = Option(None, '--key', '-ki'),
):
    uo: json | toml | yaml | mpck | None = None
    if use_json:
        juo: json = json(directory=dirname, filename=filename)
        uo = juo
    if use_toml:
        tuo: toml = toml(directory=dirname, filename=filename)
        uo = tuo
    if use_yaml:
        yuo: yaml = yaml(directory=dirname, filename=filename)
        uo = yuo
    if use_mpck:
        muo: mpck = mpck(directory=dirname, filename=filename)
        uo = muo
    if uo is None:
        uo = json(directory=dirname, filename=filename)

    inspection: bool = False
    inspect_initialize(uo, dirname, filename, use_json, use_toml, use_yaml, use_mpck)
    if full_inspection:
        inspection = True
        uo.inspect(full=True)
        print("[green]Verified Settings:[/]")
        print(f'{SETTINGS!r}')
        SETTINGS.show_all_values()
        # if repr_listing:
        #     print(f'{SETTINGS!r}')
        # else:
        #     print(f'{SETTINGS!r}')
        #     SETTINGS.show_all_values()
    if mem_alloc_inspection:
        inspection = True
        uo.inspect(mem_alloc=True)
    if repr_inspection:
        inspection = True
        uo.inspect(representation=True)
    if key_inspection:
        inspection = True
        uo.inspect(key=key_inspection)
    if exists_inspection:
        inspection = True
        if uo.exists:
            print(f'Found! [green]{uo.modelpath}[/]')
        else:
            print(f'Not Found! [red]{uo.modelpath}[/]')
    if not inspection:
        uo.inspect()
