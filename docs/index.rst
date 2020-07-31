=================================
nbcli: NetBox Command-line Client
=================================

.. contents::
    :local:

Extensible command-line interface for Netbox using pynetbox module. 

.. code:: text

    usage: nbcli [-h] <command> ...

    Extensible CLI for Netbox

    optional arguments:
      -h, --help  show this help message and exit

    Commands:
      <command>
        init      Initialize nbcli.
        search    Search Netbox Objects
        show      Show detail view of Netbox Object
        shell     Launch interactive shell
        pynb      Wrapper for pynetbox

    General Options:
      -h, --help           show this help message and exit
      -v, --verbose        Show more logging messages
      -q, --quiet          Show fewer logging messages

Core Commands
-------------

.. toctree::
    :maxdepth: 1

    init
    nbsearch
    show
    pynb
    shell

Extend and Customize
--------------------

.. toctree::
    :maxdepth: 1

    views
    commands

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

- Search Netbox instance from command line
- Show detail view of objects
- Command line wrapper for pynetbox
- Shell with preloaded pynetbox endpoints
    - Run scripts in shell environment.
- Customizable table/detail views
- Extensible by adding custom commands
