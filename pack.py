# In the name of God

import json
import requests
from names_urls_tokens import text_api_base_url, api_key


def get_text_api_token():
    baseUrl = "http://api.text-mining.ir/api/"
    url = baseUrl + "Token/GetToken"
    querystring = {"apikey": api_key}
    response = requests.request("GET", url, params=querystring, timeout=30)
    data = json.loads(response.text)
    return data["token"]


text_api_token = get_text_api_token()


def normalize_text(text):
    payload = '{"text":"' + text + '", "refineSeparatedAffix":true}'

    url = text_api_base_url + "PreProcessing/NormalizePersianWord"
    return call_text_api(url, payload, text_api_token)


def find_language(text):
    url = text_api_base_url + "LanguageDetection/Predict"
    payload = '"' + text + '"'
    lang = call_text_api(url, payload, text_api_token)
    return lang


def call_text_api(url, data, token_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token_key,
        "Cache-Control": "no-cache",
    }
    response = requests.request(
        "POST", url, data=data.encode("utf-8"), headers=headers, timeout=30
    )
    return response.text
