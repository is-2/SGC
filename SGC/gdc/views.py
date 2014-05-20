from django.shortcuts import render
# Custom imports
from models import ModificationRequest
# Create your views here.

def list_requests(request):
    user = request.user # Get logged in user
    requests = user.modificationrequest_set.all() # Get all modification requests to user
    ctx = {'requests':requests}
    return render(request, 'gdc/request/list_requests.html', ctx)

def visualize_request(request, id_request):
    mod_request = ModificationRequest.objects.get(id=id_request)
    ctx = {'mod_request':mod_request}
    return render(request, 'gdc/request/visualize_request.html', ctx)
