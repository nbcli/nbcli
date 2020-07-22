```
$ git clone https://github.com/ericgeldmacher/nbcli.git
$ cd nbcli
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install nbcli
$ export NBCLI_DIR=$(pwd)/.nbcli_dev
$ nbcli init
$ git clone https://github.com/netbox-community/netbox-docker.git
$ cp -r dev-env-files/* netbox-docker/
$ cd netbox-docker
$ docker-compose pull
$ docker-compose up -d
```
