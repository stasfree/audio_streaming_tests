import requests
import pytest
import random
import string
import json
import os
from conftest import ValueStorage

rootUrl = 'http://45.132.107.112:8080'

def get_random_chars(num):
    return ''.join(random.choice(string.ascii_letters) for x in range(num))

def test_check_hello():
    url = rootUrl + '/hello'
    res = requests.get(url)
    assert res.status_code == 200
    print('\nPassed /hello check')

def test_check_user_registration():
    url = rootUrl + '/register'
    ValueStorage.email = get_random_chars(random.randint(3, 10)) + '@gmail.com'
    ValueStorage.password = get_random_chars(random.randint(3, 20))
    data = {
        "email": ValueStorage.email,
        "password": ValueStorage.password
    }
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*"
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    print('\nPassed user registration check')

def test_check_user_login():
    url = rootUrl + '/login'
    data =  data = {
        "email": ValueStorage.email,
        "password": ValueStorage.password
    }
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*"
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    ValueStorage.token = res.headers['Authorization']
    print('\nPassed user login check')

def test_check_all_audio():
    url = rootUrl + '/audio'
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*",
        "Authorization": ValueStorage.token
    }
    res = requests.get(url, headers=headers)
    assert res.status_code == 200
    res_json = json.dumps(res.json()[0])
    assert json.loads(res_json)['id'] != None
    assert json.loads(res_json)['id'] != ''
    ValueStorage.trackId = json.loads(res_json)['id']
    assert json.loads(res_json)['album'] != ''
    print('\nPassed all audio check')

def test_check_audio_by_trackId():
    url = rootUrl + '/audio/' + str(ValueStorage.trackId)
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*",
        "Authorization": ValueStorage.token
    }
    res = requests.get(url, headers=headers)
    assert res.status_code == 200
    print('\nPassed audio check by track id')

def test_check_audio_scan():
    url = rootUrl + '/audio/scan'
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*",
        "Authorization": ValueStorage.token
    }
    res = requests.get(url, headers=headers)
    assert res.status_code == 200
    assert res.text == 'SCANNED'
    print('\nPassed audio scan')


    
    