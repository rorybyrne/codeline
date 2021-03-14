"""PluginMeta model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass, field

from codeline.sdk.context.context import Context
from codeline.sdk.plugin.plugin import CodelinePlugin
from codeline.sdk.plugin.result import Result


@dataclass
class PluginMeta:
    """Model of a plugin which is about to be invoked

    Attrs:
        name            The name of the plugin
        implementation  The loaded instance of the plugin
        title           The display title of the plugin
        trigger         The trigger word for the plugin
    """
    name: str
    implementation: CodelinePlugin
    title: str = field(init=False)
    trigger: str = field(init=False)

    def __post_init__(self):
        """Set the title and trigger from the implementation class

        Note:
            This should probably be loaded from a meta.json file in the plugin dir
        """
        if None in [self.implementation.trigger, self.implementation.title]:
            raise RuntimeError(f"Invalid plugin: {self.name}")

        self.title = self.implementation.title
        self.trigger = self.implementation.trigger

    def invoke(self, context: Context) -> Result:
        """Invoke the plugin"""
        return self.implementation.main(context=context)
