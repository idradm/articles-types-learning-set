import json
import urllib
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from watson import documents
from watson.status import Status
from watson.forms.login import WatsonLoginForm
from watson.models import Sessions, State, Type
from watson.watson_exception import WatsonException

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
        status = Status(user=request.user)
        try:
            status.set(session, number)
        except WatsonException as e:
            return HttpResponse(e.args[0], status=400)

        if request.method == 'POST':
            status.set_type(request.POST['type'])
            return HttpResponse(status=200)
        return render(request, 'main.html',
                      {
                          'state': {'session': status.get_current_session_name(), 'number': status.get_current_number()},
                          'url': status.get_url(),
                          'categories': Type.get_categories(),
                          'set': status.get_current_type()
                      }
                      )
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
        output = json.dumps({"path": '/watson/%s/%d' % (urllib.quote(state.session.name), number)})
        return HttpResponse(output, content_type="application/json")
    else:
        raise HttpResponse(status=401)

def sessions_import_sites(request, id):
    d = documents.DocumentsGenerator()
    d.generate_session(int(id))
    from django.db import connection
    #for q in connection.queries:
    #    print q
    return HttpResponse("TEST %d" % int(id))
