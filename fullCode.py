from datetime import datetime
import time
import json
import requests

DEBUG_MODE = True

# we need to get the cookie setion
cookies = {
    'WSS_FullScreenMode': 'false',
    '__cflb': '0H28vmtVNKrV3kf7sLBvbqCdSRxYVhGpHM9BQwWp1Zu',
}

headers = {
    'authority': 'www.rail.co.il',
    'accept': 'application/xml, text/xml, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'WSS_FullScreenMode=false; __cflb=0H28vmtVNKrV3kf7sLBvbqCdSRxYVhGpHM9BQwWp1Zu',
    'pragma': 'no-cache',
    'referer': 'https://www.rail.co.il/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

r = requests.get('https://www.rail.co.il/', cookies=cookies, headers=headers)

# from get the Station I save the Data and searching the object in Scripts
if DEBUG_MODE:
    w = r.text
    with open('r1.txt', 'w', encoding="utf8") as f:
        f.write(w)


# this will be the dynamic section, get it from args or for the http call
now = datetime.now()
requeuedTimeParamsDate = now.strftime('%Y%m%d')
requeuedTimeParamsTime = now.strftime('%H%M')
CountNextTrains = 2

params = {
    'OId': '4600',
    'TId': '680',
    'Date': '20220626',
    'Hour': '1230',
    'isGoing': 'true',
    'c': int(round(time.time() * 1000)),

}

# the headers for the getRoutes
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.rail.co.il/pages/trainsearchresultnew.aspx?FSID=${}&TSID=${}&Date=${}&Hour=${}&IOT=true&IBA=false&TSP=${}'.format(
        params["OId"], params["TId"], params["Date"], params["Hour"], params["c"]),
    # Requests sorts cookies= alphabetically
    # 'Cookie': '__cflb=04dTocH5b5KGxLrtMEvvFT4TgBYP2oGYroWiNDSQLB; _gcl_au=1.1.273731938.1656147133; WSS_FullScreenMode=false; _ga=GA1.3.807015627.1656147135; _gid=GA1.3.733973466.1656147135; __za_cd_19762596=%7B%22visits%22%3A%22%5B1656147135%5D%22%2C%22campaigns_status%22%3A%7B%2258244%22%3A1656150219%2C%2271325%22%3A1656150219%2C%2271643%22%3A1656150221%7D%7D; __za_19762596=%7B%22sId%22%3A114725058%2C%22dbwId%22%3A%221%22%2C%22sCode%22%3A%22bc90881fb2c84969aed5428105954f95%22%2C%22sInt%22%3A5000%2C%22aLim%22%3A2000%2C%22asLim%22%3A100%2C%22na%22%3A3%2C%22td%22%3A1%2C%22ca%22%3A%221%22%7D; __za_cds_19762596=%7B%22data_for_campaign%22%3A%7B%22country%22%3A%22IL%22%2C%22language%22%3A%22EN%22%2C%22ip%22%3A%2289.139.87.13%22%2C%22start_time%22%3A1656147133000%7D%7D; _hjSessionUser_957363=eyJpZCI6ImZkMzBiY2VkLTE3YWUtNWI0ZS1hOTM3LTBmOTkxYjVkNTUwMSIsImNyZWF0ZWQiOjE2NTYxNDcxODU5MjMsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample=0; _hjSession_957363=eyJpZCI6ImNlODRjZGNjLTliMmItNGE1YS1hZDUyLTAwODcyMjg1MTM1NCIsImNyZWF0ZWQiOjE2NTYxNTA3NzUyMzAsImluU2FtcGxlIjpmYWxzZX0=',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

# get the data from the site
response = requests.get('https://www.rail.co.il/apiinfo/api/Plan/GetRoutes',
                        params=params, cookies=r.cookies, headers=headers)


# for debug only, we can read the json file
if DEBUG_MODE:
    q = response.text
    with open('r2.json', 'w') as f:
        f.write(q)
    print(q)


# parse the selected time from the user to the Rail format
requeuedTime = datetime.strptime(
    params["Date"]+' '+params["Hour"], '%Y%m%d %H%M')


# parse the result to json
stud_obj = json.loads(response.text)
nextTrains = []
for i in stud_obj["Data"]["Routes"]:
    if len(nextTrains) == CountNextTrains:
        break
    dt = datetime.strptime(i["Train"][0]["DepartureTime"], '%d/%m/%Y %H:%M:%S')
    check = requeuedTime < dt
    if check:
        nextTrains.append(i["Train"][0])
    if DEBUG_MODE:
        print("requeuedTime is greater than dt : ", check)
        print("DepartureTime", i["Train"][0]["DepartureTime"])


# end with the api
print("done", nextTrains)
