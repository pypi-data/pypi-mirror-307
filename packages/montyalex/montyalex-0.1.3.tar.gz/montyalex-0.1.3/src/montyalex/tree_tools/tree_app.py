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
    fs_tree = FileSystemTree(id_)
    if fs_tree.exists:
        print(f'Tree {id_!r} already exists')
    else:
        fs_tree.write()
        print(f'Tree created at: {id_!r}, use setup to continue')

@tree_.command(name='setup')
def setup_(id_: str, template: str = None):
    fs_tree = FileSystemTree(id_)
    scanned_tree = FileSystemTree(id_).scan()
    if template:
        fs_tree.setup(template=template)
    fs_tree_name = scanned_tree["name"]
    # fs_treeId = scanned_tree[""]
    fs_tree_age = scanned_tree["age"]
    fs_tree_template = None
    if 'template' in scanned_tree.keys():
        fs_tree_template = scanned_tree["template"]
    print(f'Tree: {fs_tree_name!r}, {fs_tree_age!r}')
    # print(f'Identifier: {fs_treeId!r}')
    if fs_tree_template:
        print(f'Template: {fs_tree_template!r}')

@nodes_.command(name='first')
def first_(id_: str):
    fs_tree = FileSystemTree(id_).scan()
    fs_nodes = fs_tree["nodes"]
    first_node = fs_nodes[0]
    print(f'First item of {fs_tree["name"]!r} tree: {first_node}')

@nodes_.command(name='next')
def next_(id_: str):
    fs_tree = FileSystemTree(id_).scan()
    print(f'Next item of {fs_tree["name"]!r} tree: ')

@nodes_.command(name='prev')
def prev_(id_: str):
    fs_tree = FileSystemTree(id_).scan()
    print(f'Prev item of {fs_tree["name"]!r} tree: ')

@nodes_.command(name='last')
def last_(id_: str):
    fs_tree = FileSystemTree(id_).scan()
    fs_nodes = fs_tree["nodes"]
    last_node = fs_nodes[-1]
    print(f'Last item of {fs_tree["name"]!r} tree: {last_node}')

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
    fs_tree = FileSystemTree(id_)
    if fs_tree.exists is True:
        print(f'Tree {id_!r} deleted')
        fs_tree.delete()
    else:
        print(f'Tree {id_!r} already does not exist')
