
#1)GET /<tz name> else <tz name> может быть пустым - тогда в GMT        (Получилось)

#2)о запросу POST /api/v1/convert - преобразует дату/время из одного часового пояса в другой        (Получилось)
#принимает: параметр date - json формата {"date":"12.20.2021 22:21:05", "tz": "EST"}  и target_tz - строку с определением зоны

#3)по запросу POST /api/v1/datediff- отдает число секунд между между двумя датами из параметра data -json форматa     (Получилось)

#1)Пост или Гет (Получилось)
#2)Конверт или Диф  (Получилось)

import json
import pytz
import datetime


def json_exctractor(environ): 
    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    request_body = environ['wsgi.input'].read(request_body_size) 
    data = json.loads(request_body) #получается словарь
    #print(type(request_body), request_body)
    #print(type(data), data)
    return data


def parse_str(str, path_info):
    
    if path_info == "/diff":
        #print(str)
        l1 = str.find(':')
        l2 = str.find(',')
        data_time_first = str[l1 + 3:l2 - 1] # работает
    
        str = str[l2 + 1: len(str) - 1] # срезали скобку }
        #print(str)
        l1 = str.find(':')
        l2 = str.find(',')
        #print(l1, l2)
        first_timezone = str[l1 + 3:l2 - 1] # работает

        str = str[l2 + 1:len(str)]
        #print(str)
        l1 = str.find(':')
        l2 = str.find(',')
        #print(l1, l2)
        data_time_second  = str[l1 + 3:l2 - 1] # работает

        str = str[l2 + 1:len(str)]
        #print(str)
        l1 = str.find(':')
        #print(l1, l2)
        second_timezone  = str[l1 + 3:len(str) - 1]
        return data_time_first, first_timezone, data_time_second, second_timezone # готово
    else:
        #"date":"12.20.2021 22:21:05", 
        #"tz": "EST",
        #"target_tz" : "Europe/Moscow"

        #print(str)
        l1 = str.find(':')
        l2 = str.find(',')
        data_time_first = str[l1 + 3:l2 - 1] # работает

        str = str[l2 + 1: len(str) - 1] 
        #print(str)
        l1 = str.find(':')
        l2 = str.find(',')
        #print(l1, l2)
        first_timezone = str[l1 + 3:l2 - 1] # работает

        str = str[l2 + 1:len(str)]
        #print(str)
        l1 = str.find(':')
        #print(l1, l2)
        need_timezone  = str[l1 + 3:len(str) - 1]

        return data_time_first, first_timezone, need_timezone


def difference_seconds(data_time_first, first_timezone, data_time_second, second_timezone):
    format = "%Y-%m-%d %H:%M:%S"
    
    t_one = datetime.datetime.strptime(data_time_first, format)
    f_tz = pytz.timezone(first_timezone)
    f_dt = f_tz.localize(datetime.datetime(t_one.year, t_one.month, t_one.day, t_one.hour, t_one.minute, t_one.second))
    #print(t_one, f_tz, f_dt)
    
    t_two = datetime.datetime.strptime(data_time_second, format)
    s_tz = pytz.timezone(second_timezone)
    s_dt = s_tz.localize(datetime.datetime(t_two.year, t_two.month, t_two.day, t_two.hour, t_two.minute, t_two.second))
    #print(t_two, s_tz, s_dt)

    duration = s_dt - f_dt

    return print(duration.total_seconds(), " seconds")


def convert_timezone(data_time_first, first_timezone, need_timezone):
    format = "%Y-%m-%d %H:%M:%S"
    
    t_one = datetime.datetime.strptime(data_time_first, format)
    f_tz = pytz.timezone(first_timezone)
    f_dt = f_tz.localize(datetime.datetime(t_one.year, t_one.month, t_one.day, t_one.hour, t_one.minute, t_one.second))

    n_tz = pytz.timezone(need_timezone)
    n_dt = f_dt.astimezone(n_tz)
    
    return print(n_dt.strftime(format))

def select_timezone(path_info):
    format = "%Y-%m-%d %H:%M:%S"
    if path_info == '/':# and not ()
        print("\n")
        greenwich_timezone = pytz.timezone("Greenwich")
        time = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)
        time_greenwich = time.astimezone(greenwich_timezone)
        return ["\n", print(time_greenwich.strftime(format)), "\n"]
    else:
        print("\n")
        path_info = path_info[1:len(path_info)] # удаляем первый слеш
        timezone = pytz.timezone(path_info)
        time = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)
        timezone_time = time.astimezone(timezone)
        return  ["\n", print(timezone_time.strftime(format)), "\n"]       #готово


from wsgiref.simple_server import make_server


def is_post_or_get_request(environ):
    
    if environ["REQUEST_METHOD"].upper() != "POST":
        path_info = environ.get("PATH_INFO", '')
        return select_timezone(path_info)
    else:
        path_info = environ.get("PATH_INFO", '')
        if path_info == "/diff":
            print("\n")
            data = dict(json_exctractor(environ)) 
            data = str(data)
            data_time_first, first_timezone, data_time_second, second_timezone = parse_str(data, path_info)
            return ["\n", difference_seconds(data_time_first, first_timezone, data_time_second, second_timezone), "\n"] 

        if path_info == "/convert":
            print("\n")
            data = dict(json_exctractor(environ)) 
            data = str(data)
            data_time_first, first_timezone, need_timezone = parse_str(data, path_info)
            return ["\n", convert_timezone(data_time_first, first_timezone, need_timezone), "\n"] 

    
def web_app(environ, responce):
 
    is_post_or_get_request(environ)
   
    status = "200 OK"
    headers = [("Content-type", "text/html; charset=utf-8")]
        
    responce(status, headers)

    return [b'']

with make_server('', 8000, web_app) as server:
    print("Serving on port 8000...\nVisit http://127.0.0.1:8000\n")
    server.serve_forever()
