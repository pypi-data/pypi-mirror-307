import requests


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjkxZDAzOTQyLWEzNjEtNGE1Yy1iZDU5LTgwYTE3YTY1MTY0ZSJ9.eyJpc3MiOiJodHRwczovL3hsdXNlci1zc2wueHVubGVpLmNvbSIsInN1YiI6Ijk3MzEzNDk3MiIsImF1ZCI6IlhxcDBrSkJYV2h3YVRwQjYiLCJleHAiOjE3MzEzNTc2NzUsImlhdCI6MTczMTMxNDQ3NSwiYXRfaGFzaCI6InIuczd0R0VuVEpRWFNoLVNad25MVkNkZyIsInNjb3BlIjoicHJvZmlsZSBwYW4gc3NvIHVzZXIiLCJwcm9qZWN0X2lkIjoiMnJ2azRlM2drZG5sN3Uxa2wwayIsIm1ldGEiOnsiYSI6IkZFdFdOb05PcjZQc3FVNUZJaDBEZTBRcG9EU3BySzVPajZjV2lmVThkZ3M9In19.ciMVkkYJc2PSmNCSJtNF2Lmy8kAwGbVlXAyt97GS1nO8_HbcKuUz9VuyJO-PTogvmtoWHlUsMaWscjFs78SRow55pSgCi6T5dZjAx0DyHpHPOA2vTjiyr9R3X0z2BpNCLoWC8Tb7DBCxEdEzZLaetB1UHw7sqWkjdBclQ5QDYlJCU_cWefm6C958KH_c3zPlfhBJqwWMF68nXwEbjL59aV8p2pxeMjcUBja1RnxZMj3PdnlBZtfu6ne6YS-wlGRYYBDCjXjTb3iu90Rh29YnGeZmmrKX-fFMst33Pvr1BOiTgnVlUg0mnjeO94b_8Fl7vjNRuncSH8EU9mNlv6Vzlg",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://pan.xunlei.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://pan.xunlei.com/",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-captcha-token": "ck0.97eAYbMEvFR9SwPkloIWJjKfqmP8ydBnSy1f6xZk-A4f5FcLEt0XzX6viaaAizIGiVNaiknlxfDOAMkqusH294BIPLl8k9p7_sYzxoy1BSghaO6qKvoln19aJmWQPKqDx1KjueGGHZwJuO7A9mXxauxiNOXA7wh5bEro9_ioSkZIbTqKDnQos_u_I8b6nQt-8VIColKv8QaMqTZiJh8mAzQu6ZvYqxMxLzUuOV3FKEnysJyl-tXDpJjKhcsxU9TAQCyDripQKoayi2Z2DexEZMWU1EKrrNZYYn0GFr43cLhBEUJ2sPDv75aw_uBQffk8dmNHNRtdfjL_y1KI2KuLRQzjrqmwhwUHaRLDCooav9_RYZSJUONzzy0QpLZoq0tox4i5J0_Yr493LzM0h2MhzQ.ClMImMqJ07EyEhBYcXAwa0pCWFdod2FUcEI2GgYxLjkwLjciDnBhbi54dW5sZWkuY29tKiBmZDdjZGUzYThhZDU5OGNmNjY1NWQzMGE1M2IwZTNmNBKAAQ1MgQ3xHv8A9fo_GjwMl1ADX-r96YJ2jH4zoDoCkDa2_oJ-rkFfpCSvB7ckZ3TTxldGpfH309m2Dd8se7-FcWHw3j5r5vdcp62LBqpiRhh3muJ000b5ai4EDLbPCDR8TNbYN3piNrZcOBlhY1OoVNGrfptFq7KPs5OM4-ONbde_",
    "x-client-id": "Xqp0kJBXWhwaTpB6",
    "x-device-id": "fd7cde3a8ad598cf6655d30a53b0e3f4"
}
url = "https://api-pan.xunlei.com/drive/v1/files"
params = {
    "parent_id": "*",
    "filters": "{\"trashed\":{\"eq\":true}}",
    "with_audit": "true",
    "thumbnail_size": "SIZE_SMALL",
    "limit": "50"
}
response = requests.get(url, headers=headers, params=params)

print(response.text)
print(response)