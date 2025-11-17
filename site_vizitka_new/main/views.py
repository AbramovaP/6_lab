from django.shortcuts import render
from django.core.mail import send_mail
from datetime import datetime

def index(request):
    context = {
        'name': 'Абрамова Полина',
        'profession': 'Python / Django разработчик',
        'github_url': 'https://github.com/AbramovaP',
        'projects': [],
        'now': datetime.now(),
    }
    return render(request, 'main/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')

        send_mail(
            subject=f'Сообщение с сайта от {name}',
            message=message,
            from_email='pollina6abramova@yandex.ru',
            recipient_list=['pollina6abramova@yandex.ru'],
        )

    context = {
        'name': 'Абрамова Полина',
        'profession': 'Python / Django разработчик',
        'github_url': 'https://github.com/AbramovaP',
        'projects': [],
        'now': datetime.now(),
    }
    return render(request, 'main/index.html', context)
