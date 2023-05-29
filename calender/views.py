from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GoogleCalendarInitView(View):
    def get(self, request): # This is the URL that the user will visit to start the OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON, # This is the path to the client_secrets.json file that you downloaded from the Google API Console
            scopes=['https://www.googleapis.com/auth/calendar.readonly'] # This is the list of scopes that you want to request access to
        )
        authorization_url, _ = flow.authorization_url(prompt='consent') # This tells the flow that you want to be prompted every time you visit the authorization URL
        request.session['flow'] = flow # This stores the flow in the session so that the callback can access it later

        return redirect(authorization_url) # This redirects the user to the authorization URL


class GoogleCalendarRedirectView(View):
    def get(self, request):
        flow = request.session.get('flow') # This retrieves the flow from the session
        if not flow:
            return HttpResponseBadRequest('OAuth flow not found in session.')# This checks to make sure that the flow exists    

        flow.fetch_token( # This tells the flow to retrieve the access token
            authorization_response=request.build_absolute_uri(), # This tells the flow where to retrieve the authorization code from
        )

        credentials = flow.credentials # This retrieves the credentials from the flow

        # Use the credentials to build the Calendar API service
        service = build('calendar', 'v3', credentials=credentials)

        # Get list of events from the user's calendar
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        context = {
            'events': events, # This passes the list of events to the template
        }

        return render(request, 'calendar_events.html', context) # This renders the template with the list of events
