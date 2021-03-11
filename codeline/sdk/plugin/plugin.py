"""Plugin base class

Author: Rory Byrne <rory@rory.bio>
"""
from abc import abstractmethod, ABC

from codeline.sdk.plugin.context import Context
from codeline.sdk.plugin.result import Result


class CodelinePlugin(ABC):
    title = None
    trigger = None

    @abstractmethod
    def main(self, context: Context) -> Result:
        raise NotImplementedError("Please implement a main function in your plugin")
