"""PluginMeta model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass, field

from codeline.sdk.context.context import Context
from codeline.sdk.plugin.plugin import CodelinePlugin
from codeline.sdk.plugin.result import Result


@dataclass
class PluginMeta:
    name: str
    implementation: CodelinePlugin
    title: str = field(init=False)
    trigger: str = field(init=False)

    def __post_init__(self):
        if None in [self.implementation.trigger, self.implementation.title]:
            raise RuntimeError(f"Invalid plugin: {self.name}")

        self.title = self.implementation.title
        self.trigger = self.implementation.trigger

    @property
    def entrypoint(self):
        return '.'.join([self.name, 'main'])

    def invoke(self, context: Context) -> Result:
        return self.implementation.main(context=context)
