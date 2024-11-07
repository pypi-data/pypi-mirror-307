from pandas.core.accessor import register_dataframe_accessor

@register_dataframe_accessor("mydf")
class MyDataFramesAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
    
    def show(self):
        return self._obj.head(10).style.set_table_attributes('style="width:100%; white-space: nowrap;"')