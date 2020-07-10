from nbcli.views.tools import BaseView

class ExtrasObjectChangesView(BaseView):

    def table_view(self):

        self.add_col('ID', self.get_attr('id'))
        self.add_col('Time', self.get_attr('time').split('.')[0].replace('T', ' '))
        self.add_col('User', self.get_attr('user.username'))
        self.add_col('Action', self.get_attr('action'))
        self.add_col('Type', self.get_attr('changed_object_type').split('.')[-1])
        self.add_col('Object', self.get_attr('changed_object'))
        self.add_col('RequestID', self.get_attr('request_id'))
