from django.shortcuts import render


def index(request):
    return render(request, 'messenger/chat.html', {})
