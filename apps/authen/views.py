import requests
from django.conf import settings
from django.shortcuts import redirect, HttpResponse
from django.urls import reverse


def get_graph_token():
    try:
        url = settings.ADFS_URL
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "scope": "https://graph.microsoft.com/.default"
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        token_response = response.json()
        if 'access_token' in token_response:
            return token_response
        else:
            print(f"Error: 'access_token' not found in response. Response: {token_response}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


def login(request):
    return redirect(reverse("django_auth_adfs:login"))


def login_success(request):
    graph_token = get_graph_token()
    if graph_token:
        access_token = graph_token.get('access_token')
        if access_token:
            url = f"https://graph.microsoft.com/v1.0/users/{request.user.username}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                user = response.json()
                print(user)
            except requests.RequestException as e:
                print(f"Request error while fetching user info: {e}")
                print(f"Response Content: {e.response.text if e.response else 'No response content'}")
        else:
            print("Error: Access token is missing.")
    else:
        print("Error: Failed to retrieve graph token.")
    return HttpResponse("Login success")


def logout(request):
    return redirect(reverse("django_auth_adfs:logout"))


def login_no_sso(request):
    return redirect(reverse("django_auth_adfs:login-no-sso"))
