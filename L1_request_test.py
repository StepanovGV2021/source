
import requests


responce0 = requests.get('http://127.0.0.1:8000') #пустой
responce1 = requests.get('http://127.0.0.1:8000/Asia/Tomsk') #Тут
responce2 = requests.get('http://127.0.0.1:8000/America/Los_Angeles') #Лос-Анджелес
responce3 = requests.get('http://127.0.0.1:8000/America/New_York') #Нью-Йорк
responce4 = requests.get('http://127.0.0.1:8000/Europe/London') #Лондон
responce5 = requests.get('http://127.0.0.1:8000/Europe/Paris') #Париж
responce6 = requests.get('http://127.0.0.1:8000/Europe/Moscow') #Москва
responce7 = requests.get('http://127.0.0.1:8000/Asia/Tokyo') #Токио


responce8 = requests.post("http://127.0.0.1:8000/convert", json = {
    "date":"2021-12-20 22:21:05", 
    "first_tz":"EST",
    "target_tz":"Europe/Moscow"
})


responce9 = requests.post("http://127.0.0.1:8000/convert", json = {
    "date":"2020-10-27 09:30:00", 
    "first_tz":"Europe/Moscow",
    "target_tz":"Asia/Tomsk"
})

responce9 = requests.post("http://127.0.0.1:8000/convert", json = {
    "date":"2020-10-27 13:30:00", 
    "first_tz":"Asia/Tomsk",
    "target_tz":"Europe/Moscow"
})

responce10 = requests.post("http://127.0.0.1:8000/diff", json = {
   "first_date":"2020-10-24 10:29:58", 
   "first_tz":"Europe/Moscow", 
   "second_date":"2020-10-25 10:29:58", 
   "second_tz":"Europe/Moscow"
}) #разница сутки. Значит в секундах должно быть 86400 секунд.

responce11 = requests.post("http://127.0.0.1:8000/diff", json = {
    "first_date":"2021-12-20 22:21:05", 
    "first_tz":"EST", 
    "second_date":"2021-12-01 12:30:00", 
    "second_tz":"Europe/Moscow"
})#разность в секундах отрицательная т.к из второй даты вычитал первую.
