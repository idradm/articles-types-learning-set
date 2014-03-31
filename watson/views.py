import json
from urllib import parse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.template import Template, RequestContext
from watson.forms.login import WatsonLoginForm
from watson.models import Sessions, State

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


def main(request, session, number):
  if request.user.is_authenticated():
    try:
      state = State.objects.get(user=request.user)
    except State.DoesNotExist:
      state = State(user=request.user)

    if session is None:
      if state.session is not None:
        state = State.objects.get(user=request.user)
        return redirect('/watson/' + state.session.name + '/' + str(state.number))
      else:
        sessions = Sessions.objects.all()[:1]
        session = sessions[0].name
    if number is None:
      return redirect('/watson/' + session + '/0')

    state.updateState(session, number)
    return render(request, 'main.html', {"state": {'session': session, 'number': number}})
  else:
    return redirect('login')

def sessions(request):
  if request.user.is_authenticated():
    result = []
    data = Sessions.objects.all()
    for item in data:
      result.append({'name': item.name})
    output = json.dumps(result)
    return HttpResponse(output, content_type="application/json")
  else:
    raise HttpResponse(status=401)

def next(request):
  if request.user.is_authenticated():
    state = State.objects.get(user=request.user)
    if state.session.size > state.number + 1:
      number = state.number + 1
    else:
      number = 0
    output = json.dumps({"path": '/watson/' + parse.quote(state.session.name) + '/' + str(number)})
    return HttpResponse(output, content_type="application/json")
  else:
    raise HttpResponse(status=401)
