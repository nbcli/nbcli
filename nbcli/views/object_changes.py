from .base import BaseView

class ExtrasObjectChangesView(BaseView):

    def table_view(self, obj):

        self.view['ID'] = obj.id
        self.view['Time'] = str(obj.time).split('.')[0].replace('T', ' ')
        self.view['User'] = obj.user.username
        self.view['Action'] = str(obj.action)
        self.view['Type'] = str(obj.changed_object_type).split('.')[-1]
        self.view['Object'] = str(obj.changed_object)
        self.view['RequestID'] = obj.request_id
