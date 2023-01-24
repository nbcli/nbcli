## Install

```
$ pip3 install nbcli
```
## Configure

```
$ nbcli init
Edit pynetbox 'url' and 'token' entries in user_config.yml:
        ~/.nbcli/user_config.yml
```

At the very minimum, you need to specify a url and token in the user_config.yml file

```yaml
pynetbox:
  url: http://localhost:8080
  token: 0123456789abcdef0123456789abcdef01234567
```

If you need to disable SSL verification, add (or uncomment) the following to your user_config.yml file. 

```yaml
requests:
  verify: false
```

## Info

List version info

```
$ nbcli info

nbcli version: 0.8.0.dev1
NetBox version: 2.11
pynetbox version: 6.6.2
```

List information on supported Netbox object types

```
$ nbcli info --models
Model                         Lookup   Endpoint
tenant_group                  name     tenancy/tenant-groups
tenant                        name     tenancy/tenants
region                        name     dcim/regions
site                          name     dcim/sites
location                      name     dcim/locations
rack_role                     name     dcim/rack-roles
rack                          name     dcim/racks
...
```

```
$ nbcli info --models device

Model: device
Lookup: name
View Name: DcimDevicesView
API Endpoint: http://localhost:8080/api/dcim/devices

```


## Search

Simple search of Netbox objects with searchterm.

```
$ nbcli search compute

Device
======
Name       Status  Tenant  Site  Rack  Role    Type    IP Address
compute-1  Active  ENCOM   DC 1  1.2   Server  A-BL-S  10.0.0.1
compute-2  Active  ENCOM   DC 1  1.2   Server  A-BL-S  10.0.0.2
compute-3  Active  ENCOM   DC 1  1.2   Server  A-BL-S  10.0.0.3
compute-4  Active  ENCOM   DC 1  1.2   Server  A-BL-S  10.0.0.4

Address
=======
IP Address   Vrf  Status  Role  Tenant  Parent  Interface  DNS Name               Description
10.0.0.1/24  -    Active  -     ENCOM   -       -          compute-1.example.com  -
10.0.0.2/24  -    Active  -     ENCOM   -       -          compute-2.example.com  -
10.0.0.3/24  -    Active  -     ENCOM   -       -          compute-3.example.com  -
10.0.0.4/24  -    Active  -     ENCOM   -       -          compute-4.example.com  -

```

## Filter

Filter specified Netbox object type with searchterm, keyword arguments, or auto-resolve arguments

```
$ nbcli filter device web
Name         Status  Tenant  Site  Rack  Role    Type    IP Address
web-1        Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
web-2        Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
web-3        Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
web-proxy-1  Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
```

```
$ nbcli filter device role=server
Name         Status  Tenant  Site  Rack  Role    Type    IP Address
compute-1    Active  ENCOM   DC 1  1.2   Server  A-BL-S  -
compute-2    Active  ENCOM   DC 1  1.2   Server  A-BL-S  -
compute-3    Active  ENCOM   DC 1  1.2   Server  A-BL-S  -
compute-4    Active  ENCOM   DC 1  1.2   Server  A-BL-S  -
db-1         Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
db-2         Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
web-1        Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
web-2        Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
web-3        Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
web-proxy-1  Active  ENCOM   DC 1  1.1   Server  A-1U-S  -
```

```
$ nbcli filter device rack:1.2
Name       Status  Tenant  Site  Rack  Role     Type    IP Address
chassis-1  Active  ENCOM   DC 1  1.2   Chassis  A-2U-C  -
compute-1  Active  ENCOM   DC 1  1.2   Server   A-BL-S  -
compute-2  Active  ENCOM   DC 1  1.2   Server   A-BL-S  -
compute-3  Active  ENCOM   DC 1  1.2   Server   A-BL-S  -
compute-4  Active  ENCOM   DC 1  1.2   Server   A-BL-S  -
```

## Create

Create and update objects defined in a yaml file

```
$ nbcli create create-test.yml
[INFO](nbcli.create): Creating region with data: {'name': 'USA', 'slug': 'usa'}
[INFO](nbcli.create): Creating region with data: {'name': 'New York', 'slug': 'newyork', 'parent': 1}
[INFO](nbcli.create): Creating region with data: {'name': 'LA', 'slug': 'la', 'parent': 1}
[INFO](nbcli.create): Creating region with data: {'name': 'UK', 'slug': 'uk'}
[INFO](nbcli.create): Creating region with data: {'name': 'London', 'slug': 'london', 'parent': 4}
[INFO](nbcli.create): Creating site with data: {'name': 'NY DC-1', 'slug': 'ny-dc-1', 'region': 2, 'status': 'active'}
[INFO](nbcli.create): Creating site with data: {'name': 'LA DC-1', 'slug': 'la-dc-1', 'region': 3, 'status': 'active'}
[INFO](nbcli.create): Creating site with data: {'name': 'London DC-1', 'slug': 'london-dc-1', 'region': 5, 'status': 'active'}
[INFO](nbcli.create): Creating manufacturer with data: {'name': 'Cisco', 'slug': 'cisco'}
[INFO](nbcli.create): Creating manufacturer with data: {'name': 'Dell', 'slug': 'dell'}
[INFO](nbcli.create): Creating manufacturer with data: {'name': 'Hitachi', 'slug': 'hitachi'}
[INFO](nbcli.create): Creating manufacturer with data: {'name': 'IBM', 'slug': 'ibm'}
[INFO](nbcli.create): Creating device_type with data: {'model': 'R640', 'manufacturer': 3, 'slug': 'r640', 'u_height': 1}
```

## Shell

Interactive shell with preloaded pynetbox objects.

```
$ nbcli shell
Python 3.8.1 | NetBox 2.11 | pynetbox 5.3.1
Root pynetbox API object: Netbox
Additional utilities available:
        lsmodels(), nbprint(), nblogger
>>> nbprint(Device.filter('web'))
Name         Status  Tenant  Site     Rack  Role    Type    IP Address
web-1        Active  ENCOM   NY DC-1  1.1   Server  A-1U-S  -
web-2        Active  ENCOM   NY DC-1  1.1   Server  A-1U-S  -
web-3        Active  ENCOM   NY DC-1  1.1   Server  A-1U-S  -
web-proxy-1  Active  ENCOM   NY DC-1  1.1   Server  A-1U-S  -
>>>
```
