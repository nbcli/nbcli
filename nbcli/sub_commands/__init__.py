from .init import add_init
from .shell import add_shell
from .cmd import add_cmd

def add_subcommands(subparsers):
    add_init(subparsers)
    add_shell(subparsers)
    add_cmd(subparsers)
