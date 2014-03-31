import json
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.template import Template, RequestContext
from watson.forms.login import WatsonLoginForm
from watson.models import Sessions

# Create your views here.
def login(request):
  if request.method == 'POST':
    form = WatsonLoginForm(request.POST)
    if form.is_valid():
      user = authenticate(username=request.POST['user'], password=request.POST['password'])
      if user is not None:
        if user.is_active:
          auth_login(request, user)
          return redirect('main')
  else:
    form = WatsonLoginForm()

  return render(request, 'login.html', {'form': form})


def main(request):
  if request.user.is_authenticated():
    return render(request, 'main.html')
  else:
    return redirect('login')

def sessions(request):
  data = Sessions.objects.all()
  json = serializers.serialize('json', data)
  return HttpResponse(json, content_type="application/json")