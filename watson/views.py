import json
import urllib
import documents
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from watson.forms.login import WatsonLoginForm
from watson.models import Sessions, State, ArticleTypes, SessionArticles, Type

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
            if state.session_id is not None:
                state = State.objects.get(user=request.user)
                session = state.session.name
                number = state.number
            else:
                sessions = Sessions.objects.all()[:1]
                session = sessions[0].name
        if number is None:
            number = 0

        state.updateState(session, number)
        if request.method == 'POST':
            return save(request, state)

        # get types and set current one
        types = Type.objects.all()
        categories = {}
        for type in types:
            if type.category not in categories.keys():
                categories[type.category] = []
            categories[type.category].append(type)
        at = getType(state)
        t = types.get(name=at.type.name) if at else False
        sa = SessionArticles.objects.get(session=state.session, number=state.number)
        if sa.article.wikitext is None or sa.article.html is None:
            sa.article.update()
        return render(request, 'main.html',
                      {
                          'state': {'session': session, 'number': number},
                          'url': sa.article.url,
                          'categories': categories,
                          'set': t
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


def save(request, state):
    sa = SessionArticles.objects.get(session=state.session, number=state.number)
    try:
        t = ArticleTypes.objects.get(user=request.user, article=sa.article)
    except ArticleTypes.DoesNotExist:
        t = ArticleTypes(user=request.user, article=sa.article)
    t.type = Type.objects.get(name=request.POST['type'])
    t.save()
    return HttpResponse(status=200)


def getType(state):
    try:
        sa = SessionArticles.objects.get(session=state.session, number=state.number)
    except SessionArticles.DoesNotExist:
        return False
    try:
        return ArticleTypes.objects.get(user=state.user, article=sa.article)
    except ArticleTypes.DoesNotExist:
        return False

def sessions_import_sites(request, id):
    d = documents.DocumentsGenerator()
    d.generate_session(int(id))
    from django.db import connection
    #for q in connection.queries:
    #    print q
    return HttpResponse("TEST %d" % int(id))
