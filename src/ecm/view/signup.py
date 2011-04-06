# The MIT License - EVE Corporation Management
# 
# Copyright (c) 2010 Robin Jarry
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__date__ = "2011 4 5"
__author__ = "diabeteman"


from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

from ecm.data.corp.models import Corp
from ecm.core.auth import basic_auth_required
from ecm.data.scheduler.models import ScheduledTask
from ecm.data.scheduler.threads import TaskThread
from ecm.data.common.forms import UserApiKeyForm, AccountCreationForm

import re
import httplib as http
from datetime import datetime
from ecm import settings
import time



#------------------------------------------------------------------------------
@csrf_protect
def enter_api_key(request):
    if request.method == 'POST':
        form = UserApiKeyForm(request.POST)
        if form.is_valid(): # All validation rules pass
            template = 'signup/create_account.html'
            characters = form.characters
            data = {
                'userID': form.cleaned_data['userID'], 
                'apiKey': form.cleaned_data['apiKey'],
                'character_ids': ','.join([ str(char.characterID) for char in characters if char.is_corped ])
            }
            form = AccountCreationForm(initial=data)
            form.characters = characters
        else:
            template = 'signup/enter_api.html'
    else: # request.method == 'GET'
        form = UserApiKeyForm() # empty form
        template = 'signup/enter_api.html'
        
    return render_to_response(template, 
                              { 'form': form }, 
                              context_instance=RequestContext(request))

#------------------------------------------------------------------------------
@csrf_protect
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid(): # All validation rules pass
            print "YEAH"
    else: # request.method == 'GET'
        return redirect('/user')
        
    return render_to_response('signup/create_account.html', 
                              { 'form': form }, 
                              context_instance=RequestContext(request))
