from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from watson.forms.login import WatsonLoginForm

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