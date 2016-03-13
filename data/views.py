from django.contrib.auth.decorators import login_required
from django.template import loader

from dbMarket.views import get_user_info
from data.models import *

from django.http import *

__all__ = ['master_data', 'custom_data', 'view_members', 'segment', 'code_lookup', 'setup_client']


@login_required(login_url='/login')
def master_data(request, organization="1"):

    template = loader.get_template('master_data.html')

    context = get_user_info(request)

    context['title'] = 'Master Data Import'
    context['organizations'] = Organization.objects.all()
    context['current_org'] = Organization.objects.get(pk=organization)

    return HttpResponse(template.render(request=request, context=context))


@login_required(login_url='/login')
def custom_data(request, organization="1"):

    template = loader.get_template('custom_data.html')

    context = get_user_info(request)

    context['title'] = 'Custom Data Import'
    context['organizations'] = Organization.objects.all()
    context['current_org'] = Organization.objects.get(pk=organization)

    return HttpResponse(template.render(request=request, context=context))


@login_required(login_url='/login')
def view_members(request, organization="1"):

    template = loader.get_template('view_members.html')

    context = get_user_info(request)

    context['title'] = 'View Members'
    context['organizations'] = Organization.objects.all()
    context['current_org'] = Organization.objects.get(pk=organization)

    return HttpResponse(template.render(request=request, context=context))


@login_required(login_url='/login')
def segment(request, organization="1"):

    template = loader.get_template('segment.html')

    context = get_user_info(request)

    context['title'] = 'Segment'
    context['organizations'] = Organization.objects.all()
    context['current_org'] = Organization.objects.get(pk=organization)

    return HttpResponse(template.render(request=request, context=context))


@login_required(login_url='/login')
def code_lookup(request, organization="1"):

    template = loader.get_template('code_lookup.html')

    context = get_user_info(request)

    context['title'] = 'Code Lookup'
    context['organizations'] = Organization.objects.all()
    context['current_org'] = Organization.objects.get(pk=organization)

    return HttpResponse(template.render(request=request, context=context))


@login_required(login_url='/login')
def setup_client(request):

    template = loader.get_template('setup_client.html')

    context = get_user_info(request)

    context['title'] = 'Setup New Client'
    context['organizations'] = Organization.objects.all()
    context['current_org'] = Organization.objects.get(pk=1)

    return HttpResponse(template.render(request=request, context=context))


@login_required(login_url='/login')
def dashboard(request, organization="1"):

    template = loader.get_template('dashboard.html')

    context = get_user_info(request)

    context['title'] = 'Dashboard'
    context['organizations'] = Organization.objects.all()
    context['current_org'] = Organization.objects.get(pk=organization)

    return HttpResponse(template.render(request=request, context=context))
