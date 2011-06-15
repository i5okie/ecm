# Copyright (c) 2010-2011 Robin Jarry
# 
# This file is part of EVE Corporation Management.
# 
# EVE Corporation Management is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or (at your 
# option) any later version.
# 
# EVE Corporation Management is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
# more details.
# 
# You should have received a copy of the GNU General Public License along with 
# EVE Corporation Management. If not, see <http://www.gnu.org/licenses/>.

__date__ = "2011-03-13"
__author__ = "diabeteman"


import json

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, Http404
from django.core.exceptions import ObjectDoesNotExist

from ecm.view.decorators import check_user_access
from ecm.view import extract_datatable_params, get_members
from ecm.data.roles.models import Role, RoleType, Member
from ecm.data.common.models import ColorThreshold


#------------------------------------------------------------------------------
@check_user_access()
def role(request, role_typeName, role_id):
    try:
        type = RoleType.objects.get(typeName=role_typeName)
        role = Role.objects.get(roleType=type, roleID=int(role_id))
        role.accessLvl = role.get_access_lvl()
    except ObjectDoesNotExist:
        raise Http404()
    
    data = {
        'colorThresholds' : ColorThreshold.as_json(),
        'directorAccessLvl' : Member.DIRECTOR_ACCESS_LVL,
        'role_types' : RoleType.objects.all(),
        'role' : role,
        'direct_member_count' : role.members.count(),
        'total_member_count' : role.members_through_titles().count()
    }
    return render_to_response("roles/role_details.html", data, RequestContext(request))

#------------------------------------------------------------------------------
@check_user_access()
@cache_page(3 * 60 * 60) # 3 hours cache
def role_data(request, role_typeName, role_id):
    try:
        params = extract_datatable_params(request)
        type = RoleType.objects.get(typeName=role_typeName)
        role = Role.objects.get(roleType=type, roleID=int(role_id))
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    except:
        return HttpResponseBadRequest()

    total_members,\
    filtered_members,\
    members = get_members(query=role.members_through_titles(with_direct_roles=True),
                          first_id=params.first_id, 
                          last_id=params.last_id,
                          search_str=params.search,
                          sort_by=params.column, 
                          asc=params.asc)
    json_data = {
        "sEcho" : params.sEcho,
        "iTotalRecords" : total_members,
        "iTotalDisplayRecords" : filtered_members,
        "aaData" : members
    }
    
    return HttpResponse(json.dumps(json_data))