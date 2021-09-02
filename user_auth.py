import jwt, json

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .my_settings import SECRET_KEY, ALGORITHM
from users.models import User

def authentication(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)

            if not access_token:
                return JsonResponse({ 'MESSAGE' : 'NO TOKEN' }, status = 400)

            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user_id = payload['id']
            if User.objects.get(id = user_id):
                user = User.objects.get(id = user_id)
                request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({ 'MESSAGE' : 'INVALID TOKEN' }, status = 400)

        except User.DoesNotExist:
            return JsonResponse({ 'MESSAGE' : 'INVALID USER' }, status = 400)

        except Exception as e:
            return JsonResponse({ 'MESSAGE' : e}, status = 500)

        return func(self, request, *args, **kwargs)
    
    return wrapper
