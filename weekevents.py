from __future__ import print_function

import datetime
import pytz
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

#for i in range(3):
#    # Gets the start and end times and strips them so that days can be added 
#    # and to check if the current day is a weekend
#    startStrip = datetime.datetime.strptime(event_start, "%Y-%m-%dT%H:%M:%S")
#    endStrip = datetime.datetime.strptime(event_end, "%Y-%m-%dT%H:%M:%S")
#    dayOfWeek = startStrip + datetime.timedelta(days=i)
#    # les bons formats
#    currentStart = str(startStrip + datetime.timedelta(days=i)).replace(" ", "T")
#    currentEnd = str(endStrip + datetime.timedelta(days=i)).replace(" ", "T")
#    calendarEnd = str(endStrip + datetime.timedelta(days=i + 1)).replace(" ", "T")
#
#    # If the current day is a weekend, add 2 days
#    if dayOfWeek.weekday() > 4:
#        currentStart = str(startStrip + datetime.timedelta(days=i + 2)).replace(" ", "T")
#        currentEnd = str(endStrip + datetime.timedelta(days=i + 2)).replace(" ", "T")
#        calendarEnd = str(endStrip + datetime.timedelta(days=i + 3)).replace(" ", "T")
#    else:
#        print("Looking...")
#
#    # Call the Calendar API
#    # Finds the event for the current day
#    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
#    events_result = service.events().list(calendarId='primary', timeMin=currentStart + "-00:00",
#                                          maxResults=30, timeMax=calendarEnd + "-00:00",
#                                          singleEvents=True, orderBy='startTime').execute()
#    events = events_result.get('items', [])
#
#    currentEmployees = []
#    for event in events:
#        currentEmployees.append(event['summary'])
#
#
def main():
    print_events('Europe/London')
    print_events('Europe/Berlin')
    print_events('America/New_York')
    print_events('America/Denver')
    print_events('America/Los_Angeles')

def print_events(tzname):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now(pytz.timezone(tzname)).isoformat()
        sevendays = (datetime.datetime.now(pytz.timezone(tzname)) + datetime.timedelta(days=7)).isoformat() 

        print('\nGetting next 3 events in a week in timezone: ' + tzname)
        events_result = \
        service.events().list(calendarId='c_q6et1saokf97f5fb9924865ueg@group.calendar.google.com', timeMin=now, timeMax=sevendays, timeZone=tzname, \
                                maxResults=3, singleEvents=True, \
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()

