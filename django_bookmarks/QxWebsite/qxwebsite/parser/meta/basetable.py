'''
Created on Jan 5, 2014

@author: euacdeq
'''

class basetable(object):
    '''Base data structure for CI. Every table can be parsed by using this structure.'''
    def __init__(self):
        self.header = []
        self.column = {}
        self.items = {}
    def construct_items(self):
        for key in self.column.keys():
            if self.column[key]['type'] is str:
                self.set_str_default(key)
            elif self.column[key]['type'] is list:
                self.items[key] = []
            elif self.column[key]['type'] is dict:
                self.set_dict_default(key)
            else:
                self.set_table_default(key)

    def set_str_default(self, col):
        try:
            default = self.column[col]['default']
        except:
            default = ''
        self.items[col] = default
    
    def set_dict_default(self, col):
        try:
            '''keep every property has a default value'''
            default = self.column[col]['default']
        except:
            default = []
            for prop in self.column[col]['props']:
                default.append('')
        '''set default value'''
        self.items[col] = dict(zip(self.column[col]['props'], default))
    
    def set_table_default(self, col):
        self.items[col] = self.column[col]['type']()
    
    def register(self, header, column):
        self.header = header
        self.column = column
        self.construct_items()
        
    def set_item(self, name, value):
        self.items[name] = value
        
    def get_item(self, name):
        return self.items[name]
        
    def parser_str(self, col, data):
        if not isinstance(data, str):
#             global logger
#             print col, data
#             print ('the data: %s input is not a string'%(data))
            data = str(data)
        else:
            pass
        self.items[col] = self.column[col]['type'](data)
    def parser_list(self, col, data):
#         global logger
        if data == 'none' or data == '':
            print ('column (%s) has nothing'%(col))
            self.items[col] = []
        elif not isinstance(data, list):
            print ('the data "%s" is not a list'%(data))
            print ('transfer data "%s" into a list'%(data))
            self.items[col].append(data)
        elif len(data) == 0:
            print ('no data in column(%s)'%(col))
        else:
            self.items[col] = []
            for sub in data:
                self.items[col].append(self.column[col]['subtype'](sub))
                
                
    def parser_dict(self, col, data ):
#         global logger
        ''' restriction = 'ignore', 
            restriction = 'append',
            restriction = 'value', a list of values
            restriction = 'restrict'
        '''
        try:
            restriction = self.column[col]['restriction']
        except:
            restriction = ''
        
        if not isinstance(data, list):
            print ('the properties(%s) defined is illegal(%s)'%(col,data))
        elif len(data) == 0:
            print ('no property(%s) in data(%s)'%(col,data))
            '''do nothing, keep properties in defaults'''
        else:
            '''parser properties'''
            props = self.column[col]['props']
            if restriction == 'value':
                index = 0
                for prop in props:
                    self.items[col][prop] = data[index]
                    index += 1
                if index < len(data):
                    print ('the extra data will be ignored: %s'%(data[index:]))
            else:
                '''[{charg_char, 0}, {rat_type, eutran},{priv_ext_create, '2aab020103'}, {priv_ext_update, '2aab020103'},{imsi_series, 100270},{msisdn_series, 467270}]}.'''
                index = 0
                data_list = []
                '''this for loop is used to handle list nested'''
                for ele in (data):
                    if isinstance(ele, list):
                        data_list.extend(ele)
                    else:
                        data_list.append(ele)
                act_prop = data_list[::2]
                act_value = data_list[1::2]
                for p in act_prop:
                    if props.count(p) == 0:
                        try:
                            if restriction == 'restrict':
                                print ('(%s) is not one property of (%s)'%(p, col))
                                raise Exception
                            if restriction == 'append':
                                print ('adding property(%s) to (%s)'%(p, col))
                                self.items[col][p] = act_value[index]
                            if restriction == 'ignore':
                                pass
                        except:
                            pass
                    else:
                        self.items[col][p] = act_value[index]
                    index += 1
                    
    def parser_table(self, col, data):
        self.items[col] = self.column[col]['type'](data)
                    
    def set_data(self, data_list):
#         global logger
        if not len(self.header) == len(data_list):
            print len(self.header), len(data_list)
            print 'the column(%s) length is not matched with the table(%s). Please check the input'%(self.header, data_list)
            print ('the column(%s) length is not matched with the table(%s). Please check the input'%(self.header, data_list))
            raise Exception
            return False
        index = 0
        for col in self.header:
            if self.column[col]['type'] is str :
                self.parser_str(col, data_list[index])
            elif self.column[col]['type'] is list:
                self.parser_list(col, data_list[index])
            elif self.column[col]['type'] is dict:
                self.parser_dict(col, data_list[index])
            else:
                self.parser_table(col, data_list[index])
            index += 1
        return True
    def add_column(self, item_name, column_type, index = -1):
#         global logger
        if self.header.count(item_name) > 0:
            print ('the column(%s) has been exist.'%(item_name))
            return False
        self.header.insert(index, item_name)
        self.column[item_name] = column_type
        return True
    def filter(self, rule={}):
#         global logger
        if rule is None or len(rule)==0:
            print ('you do not input any rules')
            return True
        for key in rule.keys():
            '''traverse all the rules user input'''
            if self.header.count(key) == 0:
                print ('the table has not this column(%s), please check your input'%(key))
                return False
            value = rule[key]
            if value == '':
                continue
            if self.column[key]['type'] is dict:
                '''find in dict'''
                props = self.column[key]['props']
                for k in value.keys():
                    if props.count(k) == 0:
                        print ('the dict does not contain this property:%s'%(k))
                        return False
                    else:
                        if value[k] == self.items[key][k]:
                            pass
                        else:
                            if value[k].startswith('!') and not value[k].endswith(self.items[key][k]):
                                pass
                            else:
                                return False
            elif self.column[key]['type'] is str:
                '''find in str'''
                if value == self.items[key]:
                    pass
                else:
                    if value.startswith('!') and not value.endswith(self.items[key]):
                        pass
                    else:
                        return False
            elif self.column[key]['type'] is list:
                '''find in list'''
                if self.column[key]['subtype'] is str:
                    if self.items[key].count(value)>0:
                        pass
                    else:
                        return False
                else:
                    '''subtype = is a type of basetable'''
                    flag = False
                    for item in self.items[key]:
                        if item.filter(value):
                            flag = True
                            break 
                    if not flag:
                        return False
            else:
                return self.items[key].filter(value)
        return True

    def select(self, key, value):
        if self.get_item(key) == value:
            return True
        return False

    def display(self):
        print self.to_string()
        
    def to_string(self):
        return str(self.to_list()).replace('\'', '')
        
    def to_list(self):
        tolist = []
        for h in self.header:
            type = self.column[h]['type']
            if type is str:
                tolist.append(self.items[h])
            elif type is dict:
                tolist.append(self.items[h])
            elif type is list:
                if self.items[h] is None:
                    tolist.append(None)
                elif self.column[h]['subtype'] is str:
                    sublist = []
                    for item in self.items[h]:
                        sublist.append(item) 
                    tolist.append(sublist)
                else:
                    sublist = []
                    for item in self.items[h]:
                        sublist.append(item.to_list())
                    tolist.append(sublist)
            else:
                tolist.append(self.items[h].to_list())
        return tolist

    def to_html_row(self):
        tolist = []
        html = ''
        for h in self.header:
            html += '<td   align="center" style="white-space:nowrap">'
            type = self.column[h]['type']
            content = ''
            if type is str:
                content = self.items[h]
            elif type is dict:
                content = str(self.items[h])
            elif type is list:
                if self.items[h] is None:
                    content = 'None'
                elif self.column[h]['subtype'] is str:
                    sublist = []
                    for item in self.items[h]:
                        sublist.append(item) 
                    tolist.append(sublist)
                    content = ','.join(sublist)
                else:
                    for item in self.items[h]:
                        content += item.to_html_table()
            else:
                content = self.items[h].to_html_table()
            html += content.replace('\'', '')
            html += '</td>'
        return html
