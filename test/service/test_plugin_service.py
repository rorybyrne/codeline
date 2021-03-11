import os
import tempfile

from codeline.model.plugin import Plugin
from codeline.service.plugin import PluginService

SOURCE_CODE = """def main():
    # ~$ echo "hello"
    print("test")
"""


def test_load_plugin_success():
    # with tempfile.TemporaryDirectory() as tempdir:
    #     init = os.path.join(tempdir, '__init__.py')
    #     main = os.path.join(tempdir, 'main.py')
    #     print(f'Creating {init}')
    #     open(init, 'a').close()
    #     with open(main, 'a') as main_file:
    #         main_file.write(SOURCE_CODE)

    plugin_dir = '/home/rory/projects/personal/codeline/dev/plugins'
    plugin_service = PluginService(plugin_dir)
    # plugin_instance = plugin_service.load_plugin(plugin)
    # print(plugin_instance)

