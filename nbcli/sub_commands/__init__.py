from .init import add_init
from .shell import add_shell
from .pynb import add_pynb

def add_subcommands(subparsers):
    add_init(subparsers)
    add_shell(subparsers)
    add_pynb(subparsers)
