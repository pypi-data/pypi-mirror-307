"""Plugin module."""

import os

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin


class PoetryGitBranchPlugin(ApplicationPlugin):
    """Poetry Git Branch Plugin class."""

    def activate(self, application: Application):
        """Activate the plugin."""
        application.event_dispatcher.add_listener(COMMAND, self.set_git_branch_env_var)  # type: ignore[arg-type, union-attr]

    def set_git_branch_env_var(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ) -> None:
        """Set the POETRY_GIT_BRANCH environment variable."""
        if not isinstance(event.command, EnvCommand):
            return

        env_var = "POETRY_GIT_BRANCH"
        # event.io.write_line(f"Setting {env_var} environment variable...")
        os.environ[env_var] = os.popen("git symbolic-ref --short HEAD").read().strip()
