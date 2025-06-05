# yourapp/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import redirect

from .client import oAuth2Client
from core.settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTHORIZE_URL, TOKEN_URL, RESOURCE_OWNER_URL

# class OAuthAuthorizationView(APIView):
#     def get(self, request, *args, **kwargs):
#         client = oAuth2Client(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTHORIZE_URL, TOKEN_URL, RESOURCE_OWNER_URL)
#         return redirect(client.get_authorization_url())
    

class OAuthAuthorizationView(APIView):
    def get(self, request, *args, **kwargs):
        client = oAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            authorize_url=AUTHORIZE_URL,
            token_url=TOKEN_URL,
            resource_owner_url=RESOURCE_OWNER_URL
        )
        authorization_url = client.get_authorization_url()
        print(authorization_url, "SALOM")
        return Response(
            {
                'authorization_url': authorization_url
            },
            status=status.HTTP_200_OK)


class OAuthCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "Missing authorization code"}, status=400)

        client = oAuth2Client(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTHORIZE_URL, TOKEN_URL, RESOURCE_OWNER_URL)
        token_data = client.get_access_token(code)

        if 'access_token' not in token_data:
            return Response({"error": "Failed to retrieve access token", "details": token_data}, status=401)

        user_info = client.get_user_details(token_data['access_token'])
        return Response({"user_info": user_info, "access_token": token_data['access_token']})
