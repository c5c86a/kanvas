import threading
import os
from django.core.management import call_command
import django
from time import sleep

import unittest
import requests
from browser import Browser


def get(url):
    response = None
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        assert False, "Failed to connect to " + url
    return response

def start_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kanvas.settings")
    django.setup()
    call_command('runserver', use_reloader=False)

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class Server:
    def __init__(self):
        self.server = threading.Thread(target=start_django)
        self.server.daemon = True
        self.server.start()

@singleton
class Surf:
    def __init__(self):
        self.browser = Browser()


class TestSite(unittest.TestCase):
    
    def setUp(self):
        self.browser = Surf().browser
        Server()
        sleep(2)

    def test_site_is_up(self):
        url = "http://localhost:8000"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        assert 'Login' in response.content

    def test_site_content(self):
        self.browser.load("http://localhost:8000")
        message = self.browser.locate("login id").text
        assert message == 'Login', message


