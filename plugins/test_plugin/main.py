"""Test Plugin

Author: Rory Byrne <rory@rory.bio>
"""
import time
from argparse import ArgumentParser

from codeline.sdk import CodelinePlugin
from codeline.sdk.context.context import Context
from codeline.sdk.plugin.result import Result


class Plugin(CodelinePlugin):
    """Test plugin"""
    title = "Test Plugin"
    trigger = "test"

    def main(self, context: Context, **kwargs) -> Result:
        """Test"""
        context.write_response("In progress...")
        time.sleep(2)
        context.write_response("Done.")
        time.sleep(2)
        context.clear()

        return Result(True, "Plugin executed successfully.")

    def define_arguments(self, parser: ArgumentParser):
        subparsers = parser.add_subparsers(dest="subcommand")
        subparsers.add_parser("run")
