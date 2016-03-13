from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import loader

from django.http import *
from .forms import *
from data.models import *


def get_user_info(request):

    info = {}

    if not request.user.is_anonymous():

        if str(request.user.get_full_name()) != '':
            info['full_name'] = str(request.user.get_full_name())

        else:
            info['full_name'] = str(request.user.username)

        info['username'] = str(request.user.username)
        info['since_date'] = str(request.user.date_joined.strftime('%b. %Y'))
        info['profile_image'] = 'profiles/default/profile_image.png'

    else:

        info['full_name'] = ''
        info['username'] = ''
        info['since_date'] = ''
        info['profile_image'] = 'profiles/default/profile_image.png'

    return info


def auth_login(request):

    logout(request)

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:

                if user.is_active:

                    login(request, user)

                    return HttpResponseRedirect(request.GET.get('next', reverse('dashboard')))

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'title': 'Inside Info Login'})


def auth_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('login'))


def lockscreen(request):

    if not request.user.is_anonymous():

        info = get_user_info(request)

        full_name = info['full_name']
        user_name = info['username']
        profile_image = 'profiles/default/profile_image.png'

    else:

        full_name = ''
        user_name = ''
        profile_image = 'profiles/default/profile_image.png'

    logout(request)

    if request.method == 'POST':

        form = LockoutForm(request.POST)

        if form.is_valid():

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:

                if user.is_active:

                    login(request, user)
                    return HttpResponseRedirect(request.GET.get('next', reverse('dashboard')))

    else:

        if user_name == '':
            return HttpResponseRedirect(reverse('login'))

        else:
            form = LockoutForm(initial={'username': user_name})

    return render(request, 'lockscreen.html', {'form': form, 'title': 'Session Timeout',
                                               'full_name': full_name, 'profile_image': profile_image})


@login_required(login_url='/login')
def home(request):
    return HttpResponseRedirect(reverse('dashboard', args=(1,)))
