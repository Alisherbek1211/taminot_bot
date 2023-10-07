import requests
from environs import Env

env = Env()
env.read_env()
BASE_URL = env.str('URL')
import json


def post_user(phone_number,user_id):
    response = requests.post(f"{BASE_URL}/garden/detail/",data={'phone_number':phone_number,'user_id': user_id})
    return json.loads(response.text)

def get_garden(telegram_id):
    response = requests.get(f"{BASE_URL}/garden/check/{telegram_id}")
    return json.loads(response.text)
def order_product(telegram_id):
    response = requests.get(f"{BASE_URL}/products/{telegram_id}/")
    return json.loads(response.text)

def limit_item(telegram_id):
    response = requests.get(f"{BASE_URL}/products/{telegram_id}/")
    return json.loads((response.text))

def order(data):
    response = requests.post(f"{BASE_URL}/order/create/",data=data)
    return json.loads(response.text)
