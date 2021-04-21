# Custom Views

## Example custom view

```python
from nbcli.views.tools import BaseView

class DcimRUsView(BaseView):

    def table_view(self):

        self.add_col('Name', self.get_attr('name'))
        self.add_col('Device', self.get_attr('device'))


class MyDevicesView(BaseView):

    def table_view(self):

        self.add_col('Name', self.get_attr('name'))
        self.add_col('Site', self.get_attr('site'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('Site', self.get_attr('site'))
        self.add_col('Rack', self.get_attr('rack'))

        manuf = self.get_attr('device_type.manufacturer')
        dtype = self.get_attr('device_type')

        self.add_col('Type', '{} {}'.format(manuf, dtype))
```
