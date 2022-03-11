import argparse
import json
import os
import textwrap
from argparse import Action, ArgumentError, RawTextHelpFormatter
from functools import lru_cache
from typing import Callable, Dict, Iterable, List, NamedTuple, Optional, Union


def lazy_load_command(import_path: str) -> Callable:
    """Create a lazy loader for command"""
    _, _, name = import_path.rpartition('.')

    def command(*args, **kwargs):
        func = import_string(import_path)
        return func(*args, **kwargs)

    command.__name__ = name

    return command


_UNSET = object()

class Arg:
    """Class to keep information about command line argument"""
    def __init__(
            self,
            flags=_UNSET,
            help=_UNSET,
            action=_UNSET,
            default=_UNSET,
            nargs=_UNSET,
            type=_UNSET,
            choices=_UNSET,
            required=_UNSET,
            metavar=_UNSET,
            dest=_UNSET,
            ):
        self.flags = flags
        self.kwargs = {}
        for k, v in locals().items():
            if v is _UNSET:
                continue
            if k in ("self", "flags"):
                continue

            self.kwargs[k] = v

    def add_to_parser(self, parser: argparse.ArgumentParser):
        """Add this argument to an ArgumentParser"""
        parser.add_argument(*self.flags, **self.kwargs)


class ActionCommand(NamedTuple):
    """Single CLI command"""

    name: str
    help: str
    func: Callable
    args: Iterable[Arg]
    description: Optional[str] = None
    epilog: Optional[str] = None


class GroupCommand(NamedTuple):
    """ClI command with subcommands"""

    name: str
    help: str
    subcommands: Iterable
    description: Optional[str] = None
    epilog: Optional[str] = None


CLICommand = Union[ActionCommand, GroupCommand]

ARG_YUQUE_API_TOKEN = Arg(
    ('-t', '--token',),
    help=(
        "Your yuque api key, this parameter must be provided if you never configure $AIRBUS_HOME/airbus.cfg."
        "We recommend your to configure api key in $AIRBUS_HOME/airbus.cfg."
        ),
    type=str,
    )

ARG_YUQUE_API_UID = Arg(
    ('--uid',),
    help=(
        "Your yuque api key, this parameter must be provided if you never configure $AIRBUS_HOME/airbus.cfg."
        "We recommend your to configure api key in $AIRBUS_HOME/airbus.cfg."
        ),
    type=str,
    )

ARG_YUQUE_SELF_USER = Arg(
    ('-u', '--user'),
    help=(
        "Username of your yuque account, and this must be a phone number. "
        "We recommend your to configure api key in $AIRBUS_HOME/airbus.cfg."
        ),
    type=str,
    )

ARG_YUQUE_SELF_PASSWORD = Arg(
    ('-p', '--password'),
    help=(
        "Password of your yuque account. "
        "We recommend your to configure api key in $AIRBUS_HOME/airbus.cfg."
        ),
    type=str,
    )

ARG_YUQUE_THUMBSUP_USER = Arg(
    ('--thumbsup-user',),
    help=(
        "Username of other yuque account to thumbs up your docs, and this must be a phone number. "
        "We recommend your to configure api key in $AIRBUS_HOME/airbus.cfg."
        ),
    type=str,
    )

ARG_YUQUE_THUMBSUP_PASSWORD = Arg(
    ('--thumbsup-password',),
    help=(
        "Password of other yuque account to thumbs up your docs. "
        "We recommend your to configure api key in $AIRBUS_HOME/airbus.cfg."
        ),
    type=str,
    )

ARG_YUQUE_THUMBSUP_NUM = Arg(
    ('-n', '--num'),
    help=(
        "Num of docs for thumbsup yuque account. "
        "We recommend your to configure api key in $AIRBUS_HOME/airbus.cfg."
        ),
    type=int,
    default=95
    )

YUQUE_COMMANDS = (
    ActionCommand(
        name='thumbsup',
        help='Thumbs up your docs by other yuque accounts',
        description=(
            'Every other account can only thumbs up 100 docs every day, '
            'and each thumbsup for a document can obtain 7 rice. '
            'You can obtain max 2000 rice(about 285 docs) every week, '
            'so thumbs up 95 docs may be best for each account!'),
        func=lazy_load_command('airbus.cli.commands.yuque.thumbsup'),
        args=(ARG_YUQUE_API_TOKEN, ARG_YUQUE_THUMBSUP_USER, ARG_YUQUE_THUMBSUP_PASSWORD, ARG_YUQUE_THUMBSUP_NUM),
        ),
    ActionCommand(
        name='follow',
        help='Thumbs up your docs by other yuque accounts',
        description=(
            'Every other account can only thumbs up 100 docs every day, '
            'and each thumbsup for a document can obtain 7 rice. '
            'You can obtain max 2000 rice(about 285 docs) every week, '
            'so thumbs up 95 docs may be best for each account!'),
        func=lazy_load_command('airbus.cli.commands.yuque.follow'),
        args=(ARG_YUQUE_API_TOKEN, ARG_YUQUE_THUMBSUP_USER, ARG_YUQUE_THUMBSUP_PASSWORD, ARG_YUQUE_THUMBSUP_NUM),
        ),

    ActionCommand(
        name='unfollow',
        help='Thumbs up your docs by other yuque accounts',
        description=(
            'Every other account can only thumbs up 100 docs every day, '
            'and each thumbsup for a document can obtain 7 rice. '
            'You can obtain max 2000 rice(about 285 docs) every week, '
            'so thumbs up 95 docs may be best for each account!'),
        func=lazy_load_command('airbus.cli.commands.yuque.unfollow'),
        args=(ARG_YUQUE_API_TOKEN, ARG_YUQUE_THUMBSUP_USER, ARG_YUQUE_THUMBSUP_PASSWORD, ARG_YUQUE_THUMBSUP_NUM),
        ),
    ActionCommand(
        name='review',
        help='Thumbs up your docs by other yuque accounts',
        description=(
            'Every other account can only thumbs up 100 docs every day, '
            'and each thumbsup for a document can obtain 7 rice. '
            'You can obtain max 2000 rice(about 285 docs) every week, '
            'so thumbs up 95 docs may be best for each account!'),
        func=lazy_load_command('airbus.cli.commands.yuque.review'),
        args=(ARG_YUQUE_API_TOKEN, ARG_YUQUE_THUMBSUP_USER, ARG_YUQUE_THUMBSUP_PASSWORD, ARG_YUQUE_THUMBSUP_NUM),
        ),
    ActionCommand(
        name='shorthand',
        help='Thumbs up your docs by other yuque accounts',
        description=(
            'Every other account can only thumbs up 100 docs every day, '
            'and each thumbsup for a document can obtain 7 rice. '
            'You can obtain max 2000 rice(about 285 docs) every week, '
            'so thumbs up 95 docs may be best for each account!'),
        func=lazy_load_command('airbus.cli.commands.yuque.shorthand'),
        args=(ARG_YUQUE_API_TOKEN, ARG_YUQUE_THUMBSUP_USER, ARG_YUQUE_THUMBSUP_PASSWORD, ARG_YUQUE_THUMBSUP_NUM),
        ),
    )

airbus_commands: List[CLICommand] = [
    GroupCommand(
        name='yuque',
        help='Collect Rice Reward',
        subcommands=YUQUE_COMMANDS,
        ),
    ]