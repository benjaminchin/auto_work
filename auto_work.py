# pylint: disable=E1101
from __future__ import print_function
from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    driver = webdriver.Chrome()
    driver.get('https://app.joinhomebase.com/accounts/sign_in')

    email_form = driver.find_element_by_id('account_login')
    email_form.send_keys('EMAIL_HIDDEN_FOR_PRIVACY')

    password_form = driver.find_element_by_id('account_password')
    password_form.send_keys('PASSWORD_HIDDEN_FOR_PRIVACY')
    password_form.send_keys(Keys.RETURN)

    time.sleep(4)
    schedule = driver.find_element_by_class_name('js-shifts-list')
    shifts = schedule.find_elements_by_tag_name('li')
    for item in shifts:
        info = item.text

        lst = info.split()
        print(lst)
        month = get_month(lst)
        day = get_day(lst)
        hour = get_hour(lst)
        minutes = get_minutes(lst)
        year = lst[3]

        end_hour = get_end_hour(lst)
        end_minutes = get_end_minutes(lst)

        start_date = year + '-' + month + '-' + day + 'T' + hour + ':' + minutes + ':' + '00-05:00'
        print(start_date)
        end_date = year + '-' + month + '-' + day + 'T' + end_hour + ':' + end_minutes + ':' + '00-05:00'
        print(end_date)
        
        event = {
            'summary': 'Bounce U',
            'start': {
                'dateTime': start_date,
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end_date,
                'timeZone': 'America/New_York'
            }
        }
        print(event)
        
        add_event = service.events().insert(calendarId='EMAIL_HIDDEN_FOR_PRIVACY', body=event).execute()
        print('Event created: %s' % (add_event.get('htmlLink')))


def get_day(date):
    # DAY fix for 1-9 to convert to proper 2 place
    day = date[2]
    day = day[:-1]

    if int(day) < 10:
        if day == '1':
            return '01'
        elif day == '2':
            return '02'
        elif day == '3':
            return '03'
        elif day == '4':
            return '04'
        elif day == '5':
            return '05'
        elif day == '6':
            return '06'
        elif day == '7':
            return '07'
        elif day == '8':
            return '08'
        elif day == '9':
            return '09'
    else:
        return day


def get_month(date):
    m = date[1]
    if m == 'Jan':
        return '01'
    elif m == 'Feb':
        return '02'
    elif m == 'Mar':
        return '03'
    elif m == 'Apr':
        return '04'
    elif m == 'May':
        return '05'
    elif m == 'Jun':
        return '06'
    elif m == 'Jul':
        return '07'
    elif m == 'Aug':
        return '08'
    elif m == 'Sep':
        return '09'
    elif m == 'Oct':
        return '10'
    elif m == 'Nov':
        return '11'
    elif m == 'Dec':
        return '12'
    else:
        print("Error with month.")


def get_hour(date):
    # HOUR fix if in PM
    hour = date[4]
    if 'PM' in hour:
        return str(int(hour[0]) + 12)
    else:
        index = hour.find(':')
        return hour[:index]


def get_end_hour(date):
    # HOUR fix if in PM
    hour = date[6]
    if 'PM' in hour:
        return str(int(hour[0]) + 12)
    else:
        index = hour.find(':')
        return hour[:index]


def get_minutes(date):
    # MINUTES
    minutes = date[4]
    colon_index = minutes.find(':') + 1
    end_index = len(minutes) - 2
    return minutes[colon_index:end_index]


def get_end_minutes(date):
    # MINUTES
    minutes = date[6]
    colon_index = minutes.find(':') + 1
    end_index = len(minutes) - 2
    return minutes[colon_index:end_index]


if __name__ == '__main__':
    main()
