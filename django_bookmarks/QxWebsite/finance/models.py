from django.db import models

# Create your models here.
class Finance(models.Model):
    no = models.CharField(max_length = 6)
    date = models.CharField(max_length = 12)
    payment = models.CharField(max_length = 12)
    type = models.CharField(max_length = 12)
    category = models.CharField(max_length = 12)
    card_no = models.CharField(max_length = 12)
    fee= models.CharField(max_length = 12)
    balance = models.CharField(max_length = 12)
    project = models.CharField(max_length = 12)
    sponsor = models.CharField(max_length = 12)
    financial_managers = models.CharField(max_length = 12)
    description = models.CharField(max_length = 12)
    name = models.CharField(max_length = 12)
    detail = models.CharField(max_length = 12)
    model_no = models.CharField(max_length = 12)
    number = models.CharField(max_length = 12)
    price = models.CharField(max_length = 12)
    total = models.CharField(max_length = 12)
    supplier = models.CharField(max_length = 12)
    receipt = models.CharField(max_length = 12)
    receipt_photo = models.CharField(max_length = 12)
    reimbursement = models.CharField(max_length = 12)
    bank_serial_number  = models.CharField(max_length = 12)
    signature = models.CharField(max_length = 12)
    memo = models.CharField(max_length = 12)

    attrs = ['id', 'no', 'date', 'payment', 'type', 'category', 'card_no', 'fee',\
                'balance', 'project', 'sponsor', 'financial_managers', 'description', \
                'name', 'detail', 'model_no', 'number', 'price', 'total', 'supplier', \
                'receipt', 'receipt_photo', 'reimbursement', 'bank_serial_number', 'signature', 'memo']
    
    def __str__(self):
        attrs_value = []
        for attr in self.attrs:
            attrs_value.append(str(self.__getattribute__(attr)))
        return ', '.join(attrs_value)
