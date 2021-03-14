from os.path import dirname, join
import tempfile

from codeline.service.command import CommandService
from codeline.service.file import FileService
from codeline.service.plugin import PluginService

SOURCE = """def myfunc():
    # <| test dostuff
    print("howdy")
    return
"""


def test_process_file_success():
    fs = FileService()
    root_dir = dirname(dirname(dirname(__file__)))
    plugins_dir = join(root_dir, 'plugins')
    ps = PluginService(plugins_dir)
    cs = CommandService(ps, fs)

    with tempfile.TemporaryDirectory() as td:
        source_file = join(td, 'source.py')
        with open(source_file, 'a') as f:
            f.write(SOURCE)

        cs.process_file(source_file)
        with open(source_file, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 3
