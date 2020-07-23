# Setting up a test environment

Below are instructions for setting up a test environment for nbcli.  
Instructions should work on Mac and Linux.  
Instructions require git and docker-compose to be installed.

* Clone nbcli repo
```
$ git clone https://github.com/ericgeldmacher/nbcli.git
$ cd nbcli
```

* Optionally set up a virtual environment and activate.
```
$ python3 -m venv venv
$ source venv/bin/activate
```

* Install nbcli
  - From Pypi
  ```
  $ pip install nbcli
  ```
  or
  - From source
  ```
  $ pip install -e .
  ```

* Optionally set an alternate nbcli directory
```
$ export NBCLI_DIR=$(pwd)/.nbcli_dev
```

* Initialize nbcli
```
$ nbcli init
```

* Clone netbox-docker repo
```
$ git clone https://github.com/netbox-community/netbox-docker.git
```

* Copy needed files into netbox-docker directory
```
$ cp -r test/dev-env-files/* netbox-docker/
```

* Start test Netbox service and wait for service to be ready
```
$ cd netbox-docker
$ docker-compose pull
$ docker-compose up -d
$ python3 wait_for_service.py
```

* Bring down test Netbox service and deactivate virtual environment 
```
$ docker-compose down -v
$ deactivate
```
