'''
Created on Jan 9, 2014

@author: euacdeq
'''

class table(list):
    def __init__(self, table_type):
        self._type = table_type
        self.__meta = table_type()
        self.header = self.__meta.header
        self.column = self.__meta.column
        
    def register(self, header, column):
        self.header = header
        self.column = column

    def add_rows(self, data_list):
        for data in data_list:
            self.add_row(data)
            
    def add_row(self, data, instance = None):
        if instance is not None:
            row = self._type()
            row.register(instance.header, instance.column)
            row.set_data(data)
        else:
            row = self._type(data)
        self.append(row)
        
    def append(self, row):
        if not isinstance(row, self._type):
            raise Exception
        super(table, self).append(row)
        
    '''the following functions will be implemented in the future'''
    def select_in_table_single(self, key, value):
        if self.header.count(key) == 0:
            raise Exception
        items = []
        for item in self:
            if item.get_item(key) == value:
                items.append(item)
        return items

    def select_in_table(self, maps):
        items = []
        for item in self:
            result = True
            for key in maps.keys():
                value = maps[key]
                if self.header.count(key) == 0:
                    raise Exception
                if item.select(key, value) is False:
                    result = False
                    break
            if result:
                items.append(item)
        return items

    def set_foreign_table(self, foreign_tables):
        self.fk_t = {}
        for f_table_name, f_table in foreign_tables:
            for fk, fk_t_name in self.fk:
                if f_table_name == fk_t_name().__class__.__name__:
                    self.fk_t[fk] = f_table

    def select_cross_table(self, query):
        for sub_query in query:
            items = self.select_in_table(sub_query)

    def store_db(self, db_conn, additional_maps = {}):
        cursor = db_conn.cursor()
        insert_string = 'insert into table_name(%s) values(%s);'

    def build_foreign_key(self):
        self.fk = {}
    '''the above functions will be implemented in the future'''

    def filter(self, rules):
        for row in self:
            if row.filter(rules):
                return True
        return False
    
    def display(self):
        for item in self.to_list():
            print str(item).replace('\'', '')
        
    def to_list(self):
        to_list = []
        for row in self:
            to_list.append(row.to_list())
        return to_list
    
    def to_html_table(self, style = 'border="1" cellpadding="5" frame="box"'):
        html = '<table ' + style + '>'
        html += '<tr>'
        for h in self.header:
            html += '<th align="center" >' + h + '</th>'
        html += '</tr>'
        for row in self:
            html += '<tr>'
            html += row.to_html_row() 
            html += '</tr>'
        html += '</table>\n'
        return html

