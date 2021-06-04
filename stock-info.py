import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-timeseries"

querystring = {"symbol":"IBM","period2":"1571590800","period1":"493578000","region":"US"}

headers = {
    'x-rapidapi-key': "9cd96d5e9fmshaf93b821f7ee83cp148371jsn0ad58e64259a",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)