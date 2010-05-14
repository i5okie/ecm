'''
This file is part of ICE Security Management

Created on 3 fev. 2010
@author: diabeteman
'''

from django.shortcuts import render_to_response
from ism.settings import MEDIA_URL

def home(request):
    return render_to_response("base.html", {'user' : 'diabou', 'MEDIA_URL' : MEDIA_URL})