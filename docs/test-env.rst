=======
Testing
=======

.. contents::
    :local:

Setting up a test environment
-----------------------------

Instructions should work on Mac and Linux.  
Instructions require git and docker-compose to be installed.

* Clone nbcli repo

    .. code:: bash

        $ git clone https://github.com/ericgeldmacher/nbcli.git
        $ cd nbcli

* Optionally set up a virtual environment and activate.

    .. code:: bash

        $ python3 -m venv venv
        $ source venv/bin/activate

* Install nbcli

    * From Pypi

        .. code:: bash

            $ pip install nbcli

    * From source

        .. code:: bash

            $ pip install -e .

* Optionally set an alternate nbcli directory

    .. code:: bash

        $ export NBCLI_DIR=$(pwd)/.nbcli_testing


* Initialize nbcli

    *The default values in user_config.yml should work*

    .. code:: bash

        $ nbcli init

* Clone netbox-docker repo and copy needed files into netbox-docker directory

    .. code:: bash

        $ git clone https://github.com/netbox-community/netbox-docker.git
        $ cp -r tests/dev-env-files/* netbox-docker/

* Start test Netbox service and wait for service to be ready

    * *service usually take ~1 min to come up*

    * :code:`wait_for_service.py` *will time out after 5 min*

    .. code:: bash

        $ cd netbox-docker
        $ docker-compose pull
        $ docker-compose up -d
        $ python3 wait_for_service.py

**The test Netbox instance should now be ready for testing!**

* After testing, bring down test Netbox service and deactivate virtual environment 

    .. code:: bash

        $ docker-compose down -v
        $ deactivate
