import os
import tempfile

from codeline.model.plugin import Plugin
from codeline.service.plugin import PluginService

SOURCE_CODE = """def main():
    # ~$ echo "hello"
    print("test")
"""


def test_load_plugin_success():
    pass
