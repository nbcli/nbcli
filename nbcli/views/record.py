from .base import BaseView
from ..core import endpoint_loc

class RecordView(BaseView):

    def table_view(self, obj):

        self.view['ID'] = obj.id
        self.view[endpoint_loc(obj)] = str(obj)


    def detail_view(self, obj):

        for key, value in dict(obj).items():
            print(str(key), str(value))
