from codeline.service.command import CommandService
from codeline.service.file import FileService
from codeline.service.plugin import PluginService


def test_process_file_success():
    fs = FileService()
    ps = PluginService('/home/rory/projects/personal/codeline/dev/plugins')
    cs = CommandService(ps, fs)

    file = '/home/rory/projects/personal/codeline/dev/source.py'
    cs.process_file(file)
