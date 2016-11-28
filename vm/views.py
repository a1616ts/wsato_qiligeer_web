from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from vm.models import Domains
from vm.forms import DomainForm
from vm.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

import requests
import json

API_ENDPOINT_URL = 'http://localhost:8000/vm'

def login(request):
    """login"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # TODO 認証
            # TODO その人のインスタンス一覧をとる
            print(form.cleaned_data['display_name'])
            # form.cleaned_data['user']
            return redirect('vm:instance_list')
    else:
        form = LoginForm
        instance_id = 1
        return render(request, 'vm/login.html', dict(form=form, instance_id=instance_id))

@login_required(redirect_field_name='accounts')
def instance_list(request):
    payload = {'user_id': request.user.id}
    response = requests.get(API_ENDPOINT_URL, payload)
    print(response)
    decoded_json = json.loads(response.content.decode('utf-8'))
    return render(request,
                  'vm/instance_list.html',
                  {'instances': decoded_json})

def instance_create(request):
    domains = Domains()

    if request.method == 'POST':
        form = DomainForm(request.POST, instance = domains)
        if form.is_valid():
            form.cleaned_data['name']

            payload = {
                'op':  'create',
                'name': form.cleaned_data['name'],
                'user_id': request.user.id,
                'size': form.cleaned_data['size'],
                'ram': form.cleaned_data['ram'],
                'vcpus': form.cleaned_data['vcpus'],
            }
            requests.post(API_ENDPOINT_URL, data = json.dumps(payload))
            return redirect('vm:instance_list')
    else:    # GET の時
        form = DomainForm(instance = domains)

    return render(request, 'vm/instance_create.html', dict(form=form))


def instance_operation(request):
    op = ''
    if 'button_start' in request.POST:
        op = 'start'
    elif 'button_close' in request.POST:
        op = 'close'
    elif 'button_resume' in request.POST:
        op = 'resume'
    elif 'button_suspend' in request.POST:
        op = 'suspend'
    elif 'button_destroy' in request.POST:
        op = 'destory'

    if request.method == 'POST':
        payload = {
            'user_id': request.user.id,
            'op':   op,
            'name': request.POST['name'],
        }
        requests.put(API_ENDPOINT_URL, data = json.dumps(payload))
        return redirect('vm:instance_list')
