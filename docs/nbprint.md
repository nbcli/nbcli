# nbprint()


```python
>>> from nbcli.views.tools import nbprint
```

```python
>>> devlist = Devices.filter('server')
>>> nbprint(devlist)
>>> nbprint(devlist, disable_header=True)
>>> nbprint(devlist, view='detail')
>>> nbprint(devlist, view='json')
>>> nbprint(devlist, cols=['name', 'device_type.manufacturer', 'device_type.model'])
>>> nbprint(devlist, cols=[('Name', 'name'), ('Manufacturer', 'device_type.manufacturer'), ('Model', 'device_type.model')])
>>> nbprint(devlist, view_model='MyDevicesView')
>>> from user_views import MyDevicesView
>>> nbprint(devlist, view_model=MyDevicesView)
```

```python
>>> from nbcli.views.tools import Formatter
>>> f = Formatter(devlist)
>>> f.string
```
