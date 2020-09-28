=================================
nbcli: NetBox Command-line Client
=================================

Extensible command-line interface for `Netbox <https://netbox.readthedocs.io/en/stable/>`_
using the `pynetbox <https://pynetbox.readthedocs.io/en/latest/>`_ module. 

The full nbcli documentation can be found on `Read the Docs <https://nbcli.readthedocs.io/en/release/>`_.

.. warning::
    | nbcli is still in development.  
    | Syntax of commands are subject to change.

::

    usage: nbcli [-h] <command> ...

    Extensible CLI for Netbox

    optional arguments:
      -h, --help  show this help message and exit

    Commands:
      <command>
        init      Initialize nbcli.
        search    Search Netbox Objects
        filter    Filter NetBox objects.
        create    Create/Update objects with YAML file.
        shell     Launch interactive shell

    General Options:
      -h, --help           show this help message and exit
      -v, --verbose        Show more logging messages
      -q, --quiet          Show fewer logging messages

Core Commands
-------------

.. toctree::
    :maxdepth: 1

    commands/init
    commands/nbsearch
    commands/filter
    commands/create
    commands/shell

Extend and Customize
--------------------

.. toctree::
    :maxdepth: 1

    extend/views
    extend/commands

Utilities
---------

.. toctree::
    :maxdepth: 1

    nbprint

Setting up a Test Environment
-----------------------------

.. toctree::
    :maxdepth: 1

    test-env

Notable Features
----------------

- Search Netbox instance

- Filter Netbox objects

- Create and update Netbox objects with YAML file

- Shell with preloaded pynetbox endpoints

    - Run scripts in shell environment

- Customizable table/detail views

- Extensible by adding custom commands
