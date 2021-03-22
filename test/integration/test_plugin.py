import tempfile
from pathlib import Path

from codeline.service.command import CommandService
from codeline.service.file import FileService
from codeline.service.plugin import PluginService

SOURCE = """def myfunc():
    # <| test howdy
    print("howdy")
    return
"""


def test_process_file_success():
    """Should succeed"""
    file_service = FileService()
    root_dir = Path(__file__).parent.parent.parent
    plugins_dir = root_dir / 'plugins'
    plugin_service = PluginService([plugins_dir])  # Pass in a list of paths
    command_service = CommandService(plugin_service, file_service)

    with tempfile.TemporaryDirectory() as temp_dir:
        source_file = Path(temp_dir) / 'source.py'
        with open(source_file, 'a') as f:
            f.write(SOURCE)

        command_service.process_file(source_file)
        with open(source_file, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 3
