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
    cp -r tests/docker-compose.override.yml netbox-docker/ && \
    cd netbox-docker
```

### Start test Netbox service

!!! info "service usually take ~1 min to come up"

```bash
docker-compose pull && \
    docker-compose up -d
```

!!! done "The test Netbox instance should now be ready for testing!"

## After testing

Bring down test Netbox service and deactivate virtual environment.

```bash
docker-compose down -v && \
    deactivate
```
