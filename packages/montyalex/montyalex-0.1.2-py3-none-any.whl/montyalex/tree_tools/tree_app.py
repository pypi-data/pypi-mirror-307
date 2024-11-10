from montyalex.console_tools import richconsole
from montyalex.typer_tools import Option, Typer
from .presets import LPR, GPR, MCR, Table
from .treeid import FileSystemTree

print = richconsole.print


tree_: Typer = Typer(
    name='tree',
    pretty_exceptions_show_locals=False)
nodes_: Typer = Typer(
    name='nodes',
    pretty_exceptions_show_locals=False)
tree_.add_typer(nodes_)

@tree_.command(name='create')
def create_(id_: str):
    fsTree = FileSystemTree(id_)
    if fsTree.exists:
        print(f'Tree {id_!r} already exists')
    else:
        fsTree.write()
        print(f'Tree created at: {id_!r}, use setup to continue')

@tree_.command(name='setup')
def setup_(id_: str, template: str = None):
    fsTree = FileSystemTree(id_)
    scannedTree = FileSystemTree(id_).scan()
    if template:
        fsTree.setup(template=template)
    fsTreeName = scannedTree["name"]
    # fsTreeId = scannedTree[""]
    fsTreeAge = scannedTree["age"]
    fsTreeTemplate = None
    if 'template' in scannedTree.keys():
        fsTreeTemplate = scannedTree["template"]
    print(f'Tree: {fsTreeName!r}, {fsTreeAge!r}')
    # print(f'Identifier: {fsTreeId!r}')
    if fsTreeTemplate:
        print(f'Template: {fsTreeTemplate!r}')

@nodes_.command(name='first')
def first_(id_: str):
    fsTree = FileSystemTree(id_).scan()
    fsNodes = fsTree["nodes"]
    firstNode = fsNodes[0]
    print(f'First item of {fsTree["name"]!r} tree: {firstNode}')

@nodes_.command(name='next')
def next_(id_: str):
    fsTree = FileSystemTree(id_).scan()
    print(f'Next item of {fsTree["name"]!r} tree: ')

@nodes_.command(name='prev')
def prev_(id_: str):
    fsTree = FileSystemTree(id_).scan()
    print(f'Prev item of {fsTree["name"]!r} tree: ')

@nodes_.command(name='last')
def last_(id_: str):
    fsTree = FileSystemTree(id_).scan()
    fsNodes = fsTree["nodes"]
    lastNode = fsNodes[-1]
    print(f'Last item of {fsTree["name"]!r} tree: {lastNode}')

@tree_.command(name='table')
def table_(
    least: bool = Option(False, '-LPR', '--least-range'),
    most_common: bool = Option(False, '-MCR', '--common-range'),
    greatest: bool = Option(False, '-GPR', '--greatest-range'),
    show_wz_range: bool = Option(False, '-Z', '--show-zero-range')):
    if least:
        tables: dict[str, Table] = {k: v.table(show_wz_range) for k, v in LPR.items()}
        for table in tables.values():
            table.title = 'L.P. ' + table.title
            print(table)
    if greatest:
        tables: dict[str, Table] = {k: v.table(show_wz_range) for k, v in GPR.items()}
        for table in tables.values():
            table.title = 'G.P. ' + table.title
            print(table)
    if most_common:
        tables: dict[str, Table] = {k: v.table(show_wz_range) for k, v in MCR.items()}
        for table in tables.values():
            table.title = 'M.C. ' + table.title
            print(table)
    if show_wz_range:
        print('The zeroith directory for the digit amount specified is included')
    else:
        print('The zeroith directory for the digit amount specified is reserved')

@tree_.command(name='delete')
def delete_(id_: str):
    fsTree = FileSystemTree(id_)
    if fsTree.exists == True:
        print(f'Tree {id_!r} deleted')
        fsTree.delete()
    else:
        print(f'Tree {id_!r} already does not exist')
