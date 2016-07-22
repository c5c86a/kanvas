import threading
import os
from django.core.management import call_command
import django
from time import sleep
from shutil import copy, copytree

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
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    copy(os.path.join(BASE_DIR, 'parent_unversioned_folder/db.sqlite3'), os.path.join(BASE_DIR, '../data/db'))
    dest = os.path.join(BASE_DIR, '../data')
    if os.listdir(dest) == []: 
        copytree(os.path.join(BASE_DIR, 'parent_unversioned_folder/media'), dest)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kanvas.settings")
    django.setup()
    call_command('makemigrations')
    call_command('migrate')
    call_command('runserver', '0.0.0.0:9000', use_reloader=False)

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
        self.url = "http://localhost:9000"
        try:
            response = requests.get(self.url)
        except:
            Server()
            sleep(2)
        self.browser = Surf().browser

    def test_site_is_up(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)
        assert 'Login' in response.content

    def test_site_content(self):
        self.browser.load(self.url)
        message = self.browser.locate("login id").text
        assert message == 'Login',  message


