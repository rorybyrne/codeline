"""Plugin base class

Author: Rory Byrne <rory@rory.bio>
"""
from abc import abstractmethod, ABC
from argparse import ArgumentParser

from codeline.sdk.context.context import Context
from codeline.sdk.plugin.result import Result


class CodelinePlugin(ABC):
    """Base class for Codeline plugins

    Your plugin should provide a trigger string which Codeline watches for.
    """
    title = None
    trigger = None

    @abstractmethod
    def main(self, context: Context, **kwargs) -> Result:
        """Implement your plugin here"""
        raise NotImplementedError()

    def define_arguments(self, parser: ArgumentParser):
        """Define arguments for the command"""
        raise NotImplementedError()
