import json

from django.http import JsonResponse

from .models import Subscriber


def api_add_subscriber(request):
    data = json.loads(request.body)
    email = data['email']

    if email != '':
        Subscriber.objects.create(email=email)
    else:
        return JsonResponse({'success': False})

    return JsonResponse({'success': True})
