"""Writer

Author: Rory Byrne <rory@rory.bio>
"""
from pathlib import Path

from codeline.sdk.context.file import File


class Writer:
    """Simple file-writing class to be used by the plugin's Context"""

    def __init__(self, file: Path):
        self._file = file

    def write(self, file: File):
        """Writes the buffer to a file"""
        with open(self._file, 'w') as f:
            for line in file:
                f.write(str(line))
                f.write('\n')
