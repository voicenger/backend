from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from decouple import config
import json
import requests

def index(request):
    return render(request,'index.html')

def profile(request):
    user=request.user

    auth0_user=user.social_auth.get(provider='auth0')

    user_data={
        'user_id':auth0_user.uid,
        'picture':auth0_user.extra_data['picture']
    }

    context={
        'user_data':json.dumps(user_data,indent=4),
        'auth0_user':auth0_user
    }
    # Получаем JWT токен
    jwt_token = get_jwt_token()

    # Сохраняем JWT токен в сессии пользователя
    request.session['jwt_token'] = jwt_token

    # Добавляем токен в контекст, если требуется использовать его на странице
    context['jwt_token'] = jwt_token

    return render(request,'profile.html', context)
    

def logout(request):
    django_logout(request)

    domain=config('APP_DOMAIN')
    client_id=config('APP_CLIENT_ID')
    return_to='http://127.0.0.1:8000/api/app/'
    
    return HttpResponseRedirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')

def get_jwt_token():
    domain = config('APP_DOMAIN')
    client_id = config('APP_CLIENT_ID')
    client_secret = config('APP_CLIENT_SECRET')
    audience = config('APP_AUDIENCE')

    url = f"https://{domain}/oauth/token"
    headers = {'content-type': 'application/json'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': audience
    }

    response = requests.post(url, json=data, headers=headers)
    
    # Добавляем вывод результата запроса на консоль
    print("Auth0 Response:", response.json())
    
    return response.json().get('access_token')