# -*- encoding: utf-8 -*-


from typing import ForwardRef
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

from django.middleware import csrf
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import User_Content
import json

@login_required(login_url="/login/")
def open_grapesjs(request, version):
    
    context = {}
    context['segment'] = ''
    context['csrf'] = csrf.get_token(request)
    context['version'] = version

    html_template = loader.get_template( 'grapesjs/grapesjs.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def activate_version(request, version):

    User_Content.objects.filter(userid=request.user).exclude(version=version).update(active=False)
    

    user_content = User_Content.objects.get(userid=request.user, version=version)
    user_content.active = True
    user_content.save()

    return redirect(reverse('grapesjs:user_created_pages'))

@login_required(login_url="/login/")
def create_new(request):
       
        user_content = User_Content.objects.filter(userid=request.user)

        if not user_content.exists():
            new_entry_version = 1
        else:
            user_content = User_Content.objects.filter(userid=request.user).latest('version')
            new_entry_version = user_content.version + 1

        user_content = User_Content()
        user_content.userid = request.user
        user_content.version = new_entry_version
       
        user_content.save()
        return redirect(reverse('grapesjs:user_created_pages'))

@login_required(login_url="/login/")
def delete_version(request, version):
       
        user_content = User_Content.objects.filter(userid=request.user, version=version)

        if user_content.exists():
            user_content.delete()

        return redirect(reverse('grapesjs:user_created_pages'))

@login_required(login_url="/login/")
def show_user_created_pages(request):
    context = {}

    load_template = 'grapesjs/user_created_pages.html'
    context['segment'] = load_template.split('/')[-1]
    context['username'] = request.user.username

    user_content = User_Content.objects.filter(userid=request.user)
    if user_content.exists():
        context['versions'] = user_content

    html_template = loader.get_template( load_template )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def save_user_content(request):
    if request.method == 'POST':
        if request.META['HTTP_GJSCONTENT_VERSION'] is None:
            return HttpResponseBadRequest('version missing')
        
        user_content = User_Content.objects.filter(userid=request.user, version=request.META['HTTP_GJSCONTENT_VERSION'])

        if not user_content.exists():
            user_content = User_Content()
            user_content.userid = request.user
            user_content.version = 1
            user_content.save()

        user_content = User_Content.objects.get(userid=request.user, version=request.META['HTTP_GJSCONTENT_VERSION'])

        user_content.configuration = request.body.decode('utf8').replace("'", '"')
        
        json_data = json.loads(user_content.configuration)
        user_content.html = json_data['gjs-html']
        user_content.css = json_data['gjs-css']
        
        user_content.save()   
        return HttpResponse(status=200)

    return HttpResponseBadRequest('wrong')

@login_required(login_url="/login/")
def load_user_content(request):
    if request.method == 'GET':
        if request.META['HTTP_GJSCONTENT_VERSION'] is None:
            return HttpResponseBadRequest('version missing')
        
        user_content = User_Content.objects.filter(userid=request.user, version=request.META['HTTP_GJSCONTENT_VERSION'])

        if not user_content.exists():
            return HttpResponse(status=200) # no data exists, create new layout in frontend

        user_content = User_Content.objects.get(userid=request.user, version=request.META['HTTP_GJSCONTENT_VERSION'])
        return HttpResponse(user_content.configuration)

    return HttpResponseBadRequest('wrong')

def user_content(request, username):
    context = {}    
    User = get_user_model()
    users = User.objects.filter(is_staff=False)

    if users.filter(username=username).exists():
        users = User.objects.get(username=username)
        user_content = User_Content.objects.filter(userid=users.id, active=True)
        if user_content.exists():
            user_content = User_Content.objects.get(userid=users.id, active=True)
            context['user_content_css'] = user_content.css
            context['user_content_html'] = user_content.html
            user_template = loader.get_template( 'grapesjs/user_content_base.html' )
            return HttpResponse(user_template.render(context, request))

    # fallback if not all of the conditions do match 
    html_template = loader.get_template( 'page-404.html' )
    return HttpResponse(html_template.render(context, request))