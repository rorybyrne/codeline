"""Plugin base class

Author: Rory Byrne <rory@rory.bio>
"""
from abc import abstractmethod, ABC

from codeline.sdk.context.context import Context
from codeline.sdk.plugin.result import Result


class CodelinePlugin(ABC):
    title = None
    trigger = None

    @abstractmethod
    def main(self, context: Context, **kwargs) -> Result:
        raise NotImplementedError()
