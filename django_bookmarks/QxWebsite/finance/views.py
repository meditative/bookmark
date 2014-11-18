from django.shortcuts import render_to_response
from django.template import RequestContext
import models
print models

def get_finance(request):
    finances = models.Finance.objects.all()
    variables = RequestContext(request, {'finances': finances})
    return render_to_response('finances.html', variables)