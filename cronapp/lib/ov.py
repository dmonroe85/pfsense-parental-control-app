import requests
from lib.config import API_HOST

def get_overrides():
    return requests.get(API_HOST + '/get_config').json()
