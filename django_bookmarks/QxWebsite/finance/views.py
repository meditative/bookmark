from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
import models

def get_finance(request):
    finances = models.Finance.objects.all()

    variables = RequestContext(request, {'finances': finances})
    return render_to_response('finances.html', variables)

def _to_json(attrs, data_models):
	jsons = []
	for data in data_models:
		json = {}
		for attr in attrs:
			json[attr] = data.__getattribute__(attr)
		jsons.append(json)
	return jsons

def save(request):
	ajax = request.GET.has_key('ajax')
	finance_item = request.GET.getlist('finance[]')
	finance_id = finance_item[0]
	query_finances = models.Finance.objects.filter(id=int(finance_id))
	# print query_finances[0]
	print len(query_finances)
	# if request.method =='POST':
	# 	print request.POST.has_key('finance')
	# 	if request.POST.has_key('finance'):
	# 		finance = request.POST['finance']
	# 		print finance
	# 		finance_id = finance[0]
	# 		query_finances = models.Finance.objects.filter(id=int(finance_id))
	if query_finances:
		finance_instance = query_finances[0]
	else:
		finance_instance = models.Finance()
	print finance_instance.id
	print finance_item
	print len(finance_item)
	print finance_instance.attrs
	print len(finance_instance.attrs)
	for index in range(0,len(finance_item)):
		print finance_instance.attrs[index], finance_item[index]
		finance_instance.__setattr__(finance_instance.attrs[index], finance_item[index])
	print finance_instance.date
	finance_instance.save()
	return HttpResponse('fail')

def bigFileView(request):
    # do something...

    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    file_name = "sqlite3.exe"
    # open(file_name, 'wb').close()
    response = HttpResponse(readFile(file_name), mimetype='application/vnd.ms-excel')

    return response