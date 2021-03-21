"""Git Commit Plugin

Author: Rory Byrne <rory@rory.bio>
"""
import subprocess
import time
from argparse import ArgumentParser
from pathlib import Path

from codeline.sdk import CodelinePlugin
from codeline.sdk.context.context import Context
from codeline.sdk.context.file import File
from codeline.sdk.context.line import CommandLine
from codeline.sdk.exception import PluginException
from codeline.sdk.plugin.result import Result
from plugins.commit.unidiff import Hunk, PatchedFile, PatchSet


class Plugin(CodelinePlugin):
    """Git commit plugin for Codeline"""

    title = "Commit"
    trigger = "commit"

    GIT_APPLY = "git apply --cached --unidiff-zero -"
    GIT_COMMIT = "git commit -m"
    GIT_DIFF = "git diff --unified=0 {}"

    # pylint: disable=arguments-differ
    def main(self, context: Context, *, message: str = None, **kwargs) -> Result:
        """Commits the hunk below the command-line"""
        if not message:
            raise PluginException("Codeline didn't pass in a commit message")

        # Write file without command line
        lines = [line for line in context.file if not isinstance(line, CommandLine)]
        new_file = File(lines, context.file.path)
        context.write(new_file)

        # Patch
        start_line_no = context.command_index + 1  # Index starts at 0
        patched_file = self._create_patch(context.file.path, start_line_no)

        # Commit
        self._do_apply(patched_file)
        self._do_commit(message)

        # Response
        context.write_response("Done.")
        time.sleep(3)
        context.clear()

        return Result(True, "Plugin executed successfully.")

    def define_arguments(self, parser: ArgumentParser):
        """Defined argparse arguments for the command"""
        parser.add_argument('-m', dest='message', type=str, required=True)

    # Patch functionality #######################

    def _create_patch(self, file: Path, start_line_no: int) -> PatchedFile:
        """Creates a patch file for the hunk containing the given"""
        diff = self._do_diff(file)
        patch_set = PatchSet(diff)

        if len(patch_set) != 1:
            raise PluginException("Expected one patch in the patch_set")

        patched_file = patch_set[0]
        to_remove = []
        for hunk in patched_file:
            if not self._hunk_contains_line(hunk, start_line_no):
                to_remove.append(hunk)

        # Remove hunks that we are not interested in
        for hunk in to_remove:
            patched_file.remove(hunk)

        if len(patched_file) == 0:
            raise PluginException("Found no hunks to commit")

        if len(patched_file) != 1:
            raise PluginException("Found more than one hunk")

        return patched_file

    @staticmethod
    def _hunk_contains_line(hunk: Hunk, line_no: int):
        """Returns True if hunk contains the given line number"""
        start = hunk.target_start
        end = hunk.target_start + hunk.target_length
        return start <= line_no <= end

    # Git commands ##############################

    def _do_diff(self, file: Path) -> str:
        """Use git to generate a diff"""
        cmd = self.GIT_DIFF.format(file)
        result = subprocess.run(cmd.split(' '), capture_output=True, check=True)
        if result.returncode > 0:
            raise PluginException("git diff failed")

        diff = result.stdout.decode('utf-8')
        return diff

    def _do_apply(self, patch: PatchedFile):
        """Use git to stage the changes defined in a patch"""
        result = subprocess.run(self.GIT_APPLY.split(' '), input=str(patch), text=True, capture_output=True, check=True)
        if result.returncode > 0:
            print(result.stderr)
            raise PluginException("Failed to apply patch.")

    def _do_commit(self, message: str):
        """Run git commit with the given message"""
        cmd = self.GIT_COMMIT.split(' ')
        cmd.append(message)
        result = subprocess.run(cmd, capture_output=True, check=True)
        if result.returncode > 0:
            print(result.stderr)
            raise PluginException("Failed to commit changes")
