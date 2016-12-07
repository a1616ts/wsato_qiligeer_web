from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework import status

from vm.models import Domains
from vm.forms import DomainForm
from vm.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from vm.models import OS_CHOICES
import io
import json
import requests

API_ENDPOINT_URL = 'http://localhost:8000/vm'

def login(request):
    if request.method is 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('vm:instance_list')
    else:
        form = LoginForm
        instance_id = 1
        return render(request, 'vm/login.html', dict(form=form, instance_id=instance_id))

@login_required(redirect_field_name='accounts')
def instance_list(request):
    user_id = request.user.id
    payload = {'user_id': user_id}
    response = requests.get(API_ENDPOINT_URL, payload)

    decoded_json = []
    if response.status_code is not status.HTTP_404_NOT_FOUND:
        decoded_json = json.loads(response.content.decode('utf-8'))

    return render(request,
                  'vm/instance_list.html',
                  {'instances': decoded_json, 'user_id': user_id})

@login_required(redirect_field_name='accounts')
def instance_create(request):
    domains = Domains()

    if request.method == 'POST':
        form = DomainForm(request.POST, instance=domains)
        if form.is_valid():
            payload = {
                'op': 'create',
                'os': OS_CHOICES[int(form.cleaned_data['os'])][1],
                'name': form.cleaned_data['name'],
                'user_id': str(request.user.id),
                'size': str(form.cleaned_data['size']),
                'ram': str(form.cleaned_data['ram']),
                'vcpus': str(form.cleaned_data['vcpus']),
            }
            response = requests.post(API_ENDPOINT_URL, payload)
            if response.status_code is status.HTTP_202_ACCEPTED:
                return redirect('vm:instance_list')
            else:
                return redirect('vm:error')
    else:
        form = DomainForm(instance=domains)

    return render(request, 'vm/instance_create.html', dict(form=form))

@login_required(redirect_field_name='accounts')
def instance_operation(request):
    if request.method is 'POST':
        op = None
        if 'button_start' in request.POST:
            op = 'start'
        elif 'button_close' in request.POST:
            op = 'close'
        elif 'button_resume' in request.POST:
            op = 'resume'
        elif 'button_suspend' in request.POST:
            op = 'suspend'
        elif 'button_delete' in request.POST:
            op = 'destory'
        else:
            return redirect('vm:error')

        payload = {
            'user_id': request.user.id,
            'name': request.POST['name'],
        }

        if op == 'destory':
            response = requests.delete(API_ENDPOINT_URL, data=payload)
        else:
            payload['op'] = op
            response = requests.put(API_ENDPOINT_URL, payload)

        if response.status_code == status.HTTP_202_ACCEPTED:
            return redirect('vm:instance_list')
        else:
            return redirect('vm:error')

@login_required(redirect_field_name='accounts')
def download(request, user_id, name):
    output = io.StringIO()
    response = requests.get(API_ENDPOINT_URL, {
        'user_id': user_id,
        'name': name,
    })
    decoded_json = []
    if response.status_code is status.HTTP_404_NOT_FOUND:
        return render(request, 'vm/error.html')
    else:
        decoded_json = json.loads(response.content.decode('utf-8'))
    f = open(decoded_json['sshkey_path'])
    data = f.read()
    f.close()
    response = HttpResponse(data, content_type='Content-Type: application/x-x509-user-cert')
    response['Content-Disposition'] = 'filename=key.pem'
    return response

@login_required(redirect_field_name='accounts')
def error(request):
    return render(request, 'vm/error.html')
