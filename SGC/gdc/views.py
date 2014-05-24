from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
# Custom imports
from models import ModificationRequest
from des.models import Item
import forms
# Create your views here.

@login_required(login_url='/login/')
def list_requests(request):
    user = request.user # Get logged in user
    requests = user.modificationrequest_set.all() # Get all modification requests to user
    ctx = {'requests':requests}
    return render(request, 'gdc/request/list_requests.html', ctx)

@login_required(login_url='/login/')
def create_request(request, id_item):
    
    if request.method == "POST":
        form = forms.CreateModificationRequestForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            item = Item.objects.get(id=id_item)
            committee = item.phase.project.committee
            total_requests = committee.count()
            ModificationRequest.objects.create(title=title, item=item, description=description, committee=committee, total_requests=total_requests)
            ctx = {'id_project':item.phase.project.id,'id_phase':item.phase.id}
            return redirect(reverse('list_items', kwargs=ctx))
            
    if request.method == "GET":
        ctx = {'id_item':id_item}
        return render(request, 'gdc/request/create_request.html', ctx)

@login_required(login_url='/login/')
def accept_request(request, id_request):
    
    if request.method == "GET":
        mod_request = ModificationRequest.objects.get(id=id_request)
        mod_request.accepted_requests += 1
        percentage = int(mod_request.total_requests / mod_request.accepted_requests * 100)
        if percentage >= 70:
            # Do something
            ModificationRequest.objects.get(id=id_request).delete()
            
        ctx = {'id_request':id_request}
        return redirect(reverse('list_requests', kwargs=ctx))

@login_required(login_url='/login/')
def reject_request(request, id_request):
    
    if request.method == "GET":
        mod_request = ModificationRequest.objects.get(id=id_request)
        mod_request.rejected_requests += 1
        percentage = int(mod_request.total_requests / mod_request.rejected_requests * 100)
        if percentage >= 30:
            # Do something
            ModificationRequest.objects.get(id=id_request).delete()
            
        ctx = {'id_request':id_request}
        return redirect(reverse('list_requests', kwargs=ctx))
    
@login_required(login_url='/login/')        
def visualize_request(request, id_request):
    mod_request = ModificationRequest.objects.get(id=id_request)
    ctx = {'mod_request':mod_request}
    return render(request, 'gdc/request/visualize_request.html', ctx)