import sys
import requests
import csv
import configparser
import time
import datetime
s = [None]
y = []
appis = None
path = None
date = None
def conf_parser():
    global s
    global appid
    global path
    #from configparser import configparser
    parser = configparser.ConfigParser()
    parser.read ('settings.cfg')
    appid = parser.get('params','appid')
    path = parser.get('params','path')
    s = parser.get('params','s')
    s = s.split(',')
    pass
def wind_der(deg):
     x = ['С','СВ','В','ЮВ','Ю','ЮЗ','З','СЗ']
     for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg>= min and deg <= max:
            res = x[i]
            break
     return res
def get_id():
    for i in range(len(s)):
        item = s[i]
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                 params={'q': item , 'type': 'like', 'units': 'metric', 'lang':'ru', 'APPID': appid })
            data = res.json()
            cities = ["{}({})".format(i['name'], i['sys']['country'])
                      for i in data['list']]
            city_id = data['list'][0]['id']
            y.append(city_id)
        except Exception as e:
                print (("Exception (get_id):", e))
                pass           
def main():
    for i in range(len(s)):
        item = s[i]
        try:
             res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id':  item , 'units': 'metric' ,'lang':'ru','APPID': appid })
             data = res.json()
             c_name = (data['city']['name'])
             for i in data['list']:
              date = time.strftime("%Y.%m.%d %H.%M", time.gmtime(time.time()))
              with open (((path)+(c_name)+ ' ' +(date)) + '.csv' , 'a', newline='') as csvfile:
                  csvwriter = csv.writer(csvfile)
                  csvwriter.writerow(((
                   data['city']['name'],data['city']['country'],data['city']['id'],
                   str(data['city']['coord']['lon'])+ " Долгота",
                   str(data['city']['coord']['lat'])+ " Широта",
                   (i['dt_txt'])[:16]),
                   str(i['main']['temp'])+"°c",
                   str(i['main']['temp_min'])+" Минимальная температура",
                   str(i['main']['temp_max'])+" Максимальная температура",
                   str((i['main']['pressure']*100)/133)+ " мм",
                   str((i['main']['sea_level'])*100/133)+ " мм на уровне моря",
                   str((i['main']['grnd_level'])*100/133)+ " мм на уровне земли",
                   str((i['main']['humidity']))+ "%",
                   str((i['wind']['speed'])) + "м/с",
                   str(wind_der(i['wind']['deg'])),
                   str(i['clouds']['all']),
                   str(i['weather'][0]['description'])))
                   #str(i(['rain']['3h'])),
                   #str(i['snow']['3h'])))
                  
        except Exception as e: 
             print ("Exception (main):", e)
             pass
if __name__ == '__main__':
 conf_parser()
 main()
