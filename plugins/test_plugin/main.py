import time

from codeline.sdk import CodelinePlugin
from codeline.sdk.context.context import Context
from codeline.sdk.plugin.result import Result


class Plugin(CodelinePlugin):
    title = "Test Plugin"
    trigger = "test"

    def main(self, context: Context) -> Result:
        """Test"""
        print("Running TestPlugin")
        context.write_response("In progress...")
        context.write_response("Done.")
        context.clear()

        return Result(True, "Plugin executed successfully.")
