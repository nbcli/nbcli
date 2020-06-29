from .base import BaseView
from ..core import app_model_loc

class RecordView(BaseView):

    def table_view(self, obj):

        self.view['ID'] = obj.id
        self.view[app_model_loc(obj)] = str(obj)


    def detail_view(self, obj):

        for key, value in dict(obj).items():
            print(str(key), str(value))
