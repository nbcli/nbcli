# Setting up a test environment  

Instructions should work on Mac and Linux.  
Instructions require python >= 3.6, git, and docker-compose to be installed.

## Clone nbcli repo

```bash
git clone https://github.com/ericgeldmacher/nbcli.git && \
    cd nbcli
```

## Set up a virtual environment

!!! info "Optional"

```bash
python3 -m venv venv && \
    source venv/bin/activate
```

## Install nbcli

* From Pypi

    ```bash
    pip3 install nbcli
    ```

* From source

    ```bash
    pip3 install -e .
    ```

## Set an alternate nbcli directory

!!! info "Optional"

```bash
export NBCLI_DIR=$(pwd)/.nbcli_testing
```

## Initialize nbcli

!!! info "The default values in user_config.yml should work"

```bash
nbcli init
```

## Create test server

### Clone netbox-docker repo

and copy needed files into netbox-docker directory

```bash
git clone https://github.com/netbox-community/netbox-docker.git && \
    cp -r tests/dev-env-files/* netbox-docker/ && \
    cd netbox-docker
```

### Create sample objects for netbox-docker

!!! info "Optional"

```bash
python3 create_initializers.py
```

### Start test Netbox service

and wait for service to be ready

!!! info "service usually take ~1 min to come up"
    `wait_for_service.py` will time out after 5 min

```bash
docker-compose pull && \
    docker-compose up -d && \
    python3 wait_for_service.py
```

!!! done "The test Netbox instance should now be ready for testing!"

## After testing

Bring down test Netbox service and deactivate virtual environment.

```bash
docker-compose down -v && \
    deactivate
```
