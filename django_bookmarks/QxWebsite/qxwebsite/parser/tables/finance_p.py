from qxwebsite.parser.meta import table, basetable

class Finance(basetable.basetable):
    def __init__(self, data_list=None):
        super(Finance, self).__init__()
        self.header = ['no',
                       'date',
                       'payment',
                       'type',
                       'category',
                       'card_no',
                       'fee',
                       'balance',
                       'project',
                       'sponsor',
                       'financial_managers',
                       'description',
                       'name',
                       'detail',
                       'model_no',
                       'number',
                       'price',
                       'total',
                       'supplier',
                       'receipt',
                       'receipt_photo',
                       'reimbursement',
                       'bank_serial_number',
                       'signature',
                       'memo',
                       ]
        self.column = {'no'         :{'type': str},
                       'date'       :{'type': str},
                       'payment'    :{'type': str},
                       'type'       :{'type': str},
                       'category'   :{'type': str},
                       'card_no'    :{'type': str},
                       'fee'        :{'type': str},
                       'balance'    :{'type': str},
                       'project'    :{'type': str},
                       'sponsor'    :{'type': str},
                       'financial_managers' :{'type': str},
                       'description'    :{'type': str},
                       'name'       :{'type': str},
                       'detail'     :{'type': str},
                       'model_no'   :{'type': str},
                       'number'     :{'type': str},
                       'price'      :{'type': str},
                       'total'      :{'type': str},
                       'supplier'   :{'type': str},
                       'receipt'    :{'type': str},
                       'receipt_photo'  :{'type': str},
                       'reimbursement'  :{'type': str},
                       'bank_serial_number' :{'type': str},
                       'signature'  :{'type': str},
                       'memo'       :{'type': str},
                       }
        self.construct_items()
        if not data_list is None and not data_list == 'none':
            self.set_data(data_list)
            
    def transfer_db(self, finance_dbmodel):
        for item in self.header:
            finance_dbmodel.__setattr__(item, self.get_item(item))
        return finance_dbmodel
            
class FinanceTable(table.table):
    def __init__(self, data_list=None):
        super(FinanceTable, self).__init__(Finance)
        if data_list is not None and not data_list == 'none':
            self.add_rows(data_list)
    
    def save_db(self, fianance_dbmodel):
        for item in self:
            finace_item = fianance_dbmodel()
            item.transfer_db(finace_item).save()
       
import xlrd
def open_excel(file='file.xlsx'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception, e:
        print str(e)
             
def excel_table_byindex(file='file.xlsx', colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    colnames = table.row_values(colnameindex) 
    list = []
    for rownum in range(1, nrows):

        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i] 
            list.append(app)
    return list

def excel_table_byname(file='file.xlsx', colnameindex=0, by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows 
    colnames = table.row_values(colnameindex)
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        list.append(row)
    return list

def main():
    table_content = excel_table_byname()
    finance_t = FinanceTable()
    finance_t.add_rows(table_content)
    return finance_t

if __name__ == '__main__':
    from finance import models
    finance_t = main()
    finance_t.display()
#     finance_t.save_db(models.Finance)
    f = models.Finance.objects.all()
    for item in f:
        for att in finance_t.header:
            print item.__getattribute__(att),
        print