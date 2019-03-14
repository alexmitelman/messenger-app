from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.safestring import mark_safe
import json


@staff_member_required
def index(request):
    return render(request, 'messenger/contacts.html', {})


@staff_member_required
def chat(request, contact_name):
    return render(request, 'messenger/chat.html', {
        'contact_name': contact_name,
        'room_name_json': mark_safe(json.dumps(contact_name)),
        'username_json': mark_safe(json.dumps(request.user.username))
    })
