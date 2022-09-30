import os
import random
import sys
from datetime import datetime, date
from time import localtime
from datetime import datetime
from requests import get, post
from zhdate import ZhDate

def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token

def get_date():
    # 构造一个将来的时间
    future = datetime.strptime('2022-12-24 08:00:00', '%Y-%m-%d %H:%M:%S')
    # 当前时间
    now = datetime.now()
    # 求时间差
    delta = future - now
    hour = delta.seconds / 60 / 60
    minute = (delta.seconds - hour * 60 * 60) / 60
    seconds = delta.seconds - hour * 60 * 60 - minute * 60
    print_now = now.strftime('%Y-%m-%d %H:%M:%S')
    data = "现在是{}，距离考研还有{}天".format(print_now,delta.days)
    return data


def get_weather(region):
    #获取天气
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    key = config["weather_key"]
    region_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(region, key)
    response = get(region_url, headers=headers).json()
    if response["code"] == "404":
        print("推送消息失败，请检查地区名是否有误！")
        os.system("pause")
        sys.exit(1)
    elif response["code"] == "401":
        print("推送消息失败，请检查和风天气key是否正确！")
        os.system("pause")
        sys.exit(1)
    else:
        # 获取地区的location--id
        location_id = response["location"][0]["id"]
    weather_url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # 天气
    weather = response["now"]["text"]
    # 当前温度
    temp = response["now"]["temp"] + u"\N{DEGREE SIGN}" + "C"
    # 风向
    wind_dir = response["now"]["windDir"]
    # 获取逐日天气预报
    url = "https://devapi.qweather.com/v7/weather/3d?location={}&key={}".format(location_id, key)
    response = get(url, headers=headers).json()
    # 最高气温
    max_temp = response["daily"][0]["tempMax"] + u"\N{DEGREE SIGN}" + "C"
    # 最低气温
    min_temp = response["daily"][0]["tempMin"] + u"\N{DEGREE SIGN}" + "C"
    # 日出时间
    sunrise = response["daily"][0]["sunrise"]
    # 日落时间
    sunset = response["daily"][0]["sunset"]
    url = "https://devapi.qweather.com/v7/air/now?location={}&key={}".format(location_id, key)
    response = get(url, headers=headers).json()
    if response["code"] == "200":
        # 空气质量
        category = response["now"]["category"]
        # pm2.5
        pm2p5 = response["now"]["pm2p5"]
    else:
        # 国外城市获取不到数据
        category = ""
        pm2p5 = ""
    id = random.randint(1, 16)
    url = "https://devapi.qweather.com/v7/indices/1d?location={}&key={}&type={}".format(location_id, key, id)
    response = get(url, headers=headers).json()
    proposal = ""
    if response["code"] == "200":
        proposal += response["daily"][0]["text"]
    return weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal


def get_tianhang():
    #获取早安一言
    try:
        key = config["tian_api"]
        url = "http://api.tianapi.com/zaoan/index?key={}".format(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded'

        }
        response = get(url, headers=headers).json()
        if response["code"] == 200:
            chp = response["newslist"][0]["content"]
        else:
            chp = ""
    except KeyError:
        chp = ""
    return chp

def get_wanan():
    #获取晚安一言
    try:
        key = config["tian_api"]
        url = "http://api.tianapi.com/wanan/index?key={}".format(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded'

        }
        response = get(url, headers=headers).json()
        if response["code"] == 200:
            chp = response["newslist"][0]["content"]
        else:
            chp = ""
    except KeyError:
        chp = ""
    return chp

def get_caihongpi():
    #获取彩虹屁
    try:
        key = config["tian_api"]
        url = "http://api.tianapi.com/caihongpi/index?key={}".format(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded'

        }
        response = get(url, headers=headers).json()
        if response["code"] == 200:
            chp = response["newslist"][0]["content"]
        else:
            chp = ""
    except KeyError:
        chp = ""
    return chp

def get_hotreview():
    #获取网易云热评
    try:
        key = config["tian_api"]
        url = "http://api.tianapi.com/hotreview/index?key={}".format(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded'

        }
        response = get(url, headers=headers).json()

        if response["code"] == 200:
            chp = response["newslist"][0]["content"]
            str1 = response["newslist"][0]["source"]

        else:
            chp = ""
    except KeyError:
        chp = ""

    result = "{}--{}".format(chp,str1)
    return result

def get_pyqwenan():
    #获取朋友圈文案
    try:
        key = config["tian_api"]
        url = "http://api.tianapi.com/pyqwenan/index?key={}".format(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded'

        }
        response = get(url, headers=headers).json()
        if response["code"] == 200:
            chp = response["newslist"][0]["content"]
            str1 = response["newslist"][0]["source"]
        else:
            chp = ""
    except KeyError:
        chp = ""
    result = "{}--{}".format(chp,str1)
    return result

def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 获取农历生日的生日
        try:
            year_date = ZhDate(year, r_mouth, r_day).to_datetime().date()
        except TypeError:
            print("请检查生日的日子是否在今年存在")
            os.system("pause")
            sys.exit(1)

    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_ciba():
    #获取金山词霸金句
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en


def send_message(to_user, access_token):
    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入地区获取天气信息
    region = config["region"]
    weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal = get_weather(region)
    note_ch = config["note_ch"]
    note_en = config["note_en"]
    if note_ch == "" and note_en == "":
        # 获取词霸每日金句
        note_ch, note_en = get_ciba()
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    #提醒吃午饭的一言，支持自己定义（按照格式哦）。

    wufan = ["到了吃午饭的时间啦，每个人都会累都会有emo的时候..一个人也要好好吃饭~",
             "到了吃午饭的时间啦,人是铁，饭是刚，不管发生什么记得按时吃饭。",
             "到了吃午饭的时间啦,记得按时吃饭，好好生活，好好爱自己。",
             "到了吃午饭的时间啦,尊敬的客户：现已到吃饭时间，你已较长时间没有进食了，请抓紧时间吃饭，逾期将收取滞纳期限。",
             "到了吃午饭的时间啦,生活要不断给自己解压让自己开心，再难也要记得吃饭。",
             "到了吃午饭的时间啦,不管走到哪，一个人也要记得好好吃饭。",
             "到了吃午饭的时间啦,或许一个人对生活最大的仪式感就是，有规律地活着，按时睡觉，按时吃饭。",
             "到了吃午饭的时间啦,原来世上最长期的关怀，是记得按时吃饭！",
             "到了吃午饭的时间啦,恋爱可以慢慢谈，肉必须趁热吃。",
             "到了吃午饭的时间啦,或许一个人对生活最大的仪式感就是，有规律地活着，按时睡觉，按时吃饭。",

             ]
    #提醒吃晚饭的一言，支持自己定义（按照格式哦）。
    wanfan = ["记得吃晚饭哦,一人食”一个人也要好好吃饭，比起白天的熙熙攘攘，更喜欢夜的安静，生活简单纯粹即喜乐~",
             "记得吃晚饭哦,人是铁，饭是刚，不管发生什么记得按时吃饭。",
             "记得吃晚饭哦,记得按时吃饭，好好生活，好好爱自己。",
             "记得吃晚饭哦,尊敬的客户：现已到吃饭时间，你已较长时间没有进食了，请抓紧时间吃饭，逾期将收取滞纳期限。",
             "记得吃晚饭哦,生活要不断给自己解压让自己开心，再难也要记得吃饭。",
             "记得吃晚饭哦,不管走到哪，一个人也要记得好好吃饭。",
             "记得吃晚饭哦,或许一个人对生活最大的仪式感就是，有规律地活着，按时睡觉，按时吃饭。",
             "记得吃晚饭哦,原来世上最长期的关怀，是记得按时吃饭！",
             "记得吃晚饭哦,恋爱可以慢慢谈，肉必须趁热吃。",
             "记得吃晚饭哦,或许一个人对生活最大的仪式感就是，有规律地活着，按时睡觉，按时吃饭。",
             "记得吃晚饭哦,余生不长，要好好吃饭好好睡觉好好爱自己。",
             "记得吃晚饭哦,好好吃饭好好睡觉，心里的垃圾定期倒一倒。",
             "记得吃晚饭哦,无论心情怎么糟糕，都不要打破生活的规律，按时吃饭按时睡觉。"

             ]
    #晚安一言，支持自己定义，按照下面的格式
    wa= [
        "到了睡觉时间了哦，要好好休息哟，明天依旧光芒万丈哦~",
        "忙忙碌碌地生活着真好啊，根本没时间伤春悲秋，每天的念头就只有，干完今天的活就可以睡觉啦。",
        "睡觉吧，不然我待会儿又要想你了。晚安好梦。",
        "温山软水.繁星万千.不及你眉眼半分。晚安好梦。",
        "跨过银河迈过月亮去迎接最好的自己。晚安好梦。",
        "有些人有些事，当我们懂得的时候已不在年轻。晚安！",
        "我绝不会为我的信仰而献身，因为我可能是错的。晚安。",
        "我贪恋的人间烟火，不偏不倚，刚好是你，晚安，余生是你。",
        "我的梦想不多：兜里有糖.卡里有钱.身边有你。晚安，亲爱的！",
        "不要放弃心里的希望，希望就如一片土壤，能生长出许多美好。晚安！",
        "懂得珍惜，暗自努力，相信自己，你就是你人生唯一的负责人，晚安。",
        "单枪匹马你别怕，一腔孤勇又如何，这一路你可以哭，但不能怂。晚安！",
        "如果你真的愿意去努力，你人生最坏的结果，也不过是大器晚成。晚安。",
        "世上最好的保鲜就是不断进步，让自己成为一个更好和更值得爱的人，晚安。",
        "你说吧，你想吃啥，是烧烤还是零食，我明天给你拿，今晚先好好睡觉。晚安！",
        "今天太宝贵，不应该为酸苦的忧虑和辛涩的悔恨所销蚀，抬起下巴，抓住今天，它不再回来。晚安。",
        "做一个温暖的人.用加法去爱人.用减法去怨恨.用乘法去感恩.你会发现全世界都会向你微笑，愿你好梦。",
        "太阳有个心愿就是照亮月亮，星星有个心愿就是点缀月光，我有个心愿就是让月亮美丽属于你，让月光浪漫照亮你。亲爱的，晚安。"
        ]
    #随机选择一句提醒午饭的话
    i = random.randint(0,len(wufan)-1)
    #随机选择一句提醒晚饭的话
    j = random.randint(0,len(wanfan)-1)
    #随机选择一句晚安的话
    k = random.randint(0,len(wa)-1)
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {#日期，星期几，模板中用法{{date.DATA}}
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "region": {#地区，模板中用法{{region.DATA}}
                "value": region,
                "color": get_color()
            },
            "weather": {#天气，模板中用法{{weather.DATA}}
                "value": weather,
                "color": get_color()
            },
            "temp": {#当前气温，模板中用法{{temp.DATA}}
                "value": temp,
                "color": get_color()
            },
            "wind_dir": {#风向，模板中用法{{wind_dir.DATA}}
                "value": wind_dir,
                "color": get_color()
            },
            "love_day": {#相爱的天数（距离在一起的日子的天数），模板中用法{{love_day.DATA}}
                "value": love_days,
                "color": get_color()
            },
            "note_en": {#金山金句(英文)，模板中用法{{note_en.DATA}}
                "value": note_en,
                "color": get_color()
            },
            "note_ch": {#金山金句(中文)，模板中用法{{note_ch.DATA}}
                "value": note_ch,
                "color": get_color()
            },
            "max_temp": {#最高气温，模板中用法{{max_temp.DATA}}
                "value": max_temp,
                "color": get_color()
            },
            "min_temp": {#最低气温，模板中用法{{min_temp.DATA}}
                "value": min_temp,
                "color": get_color()
            },
            "sunrise": {#日出时间，模板中用法{{sunrise.DATA}}
                "value": sunrise,
                "color": get_color()
            },
            "sunset": {#日落时间，模板中用法{{sunset.DATA}}
                "value": sunset,
                "color": get_color()
            },
            "category": {#空气质量，模板中用法{{category.DATA}}
                "value": category,
                "color": get_color()
            },
            "pm2p5": { #pm2.5值，模板中用法{{pm2p5.DATA}}
                "value": pm2p5,
                "color": get_color()
            },
            "proposal": { #今日建议，模板中用法{{proposal.DATA}}
                "value": proposal,
                "color": get_color()
            },
            "chp": { #早安心语，模板中用法{{chp.DATA}}
                "value": get_tianhang(),
                "color": get_color()
            },
            "wanan":{#晚安心语，模板中用法{{wanan.DATA}}
                "value": get_wanan(),
                "color": get_color()
            },
            "caihongpi": {#彩虹屁，模板中用法{{caihongpi.DATA}}
                "value": get_caihongpi(),
                "color": get_color()
            },
            "day": {#倒数日，模板中用法{{day.DATA}}
                "value": get_date(),
                "color": get_color()
            },
            "hotreview": {#网易云热评，模板中用法{{hotreview.DATA}}
                "value": get_hotreview(),
                "color": get_color()
            },
            "pyqwenan": {#朋友圈文案，模板中用法{{pyqwenan.DATA}}
                "value": get_pyqwenan(),
                "color": get_color()
            },
            "wufan": {#提醒吃午饭的一言，模板中用法{{wufan.DATA}}
                "value": wufan[i],
                "color": get_color()
            },
            "wanfan": {#提醒吃晚饭的一言，模板中用法{{wanfan.DATA}}
                "value": wanfan[j],
                "color": get_color()
            },
            "wa": {#晚安的一言，模板中用法{{wa.DATA}}
                "value": wa[k],
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = "今天{}生日哦，祝{}生日快乐！".format(value["name"], value["name"])
        else:
            birthday_data = "距离{}的生日还有{}天".format(value["name"], birth_day)
        # 将生日数据插入data
        data["data"][key] = {"value": birthday_data, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)
        #如果发送失败，一直重发
        response = post(url, headers=headers, json=data).json()
        while(response["errcode"] != 0):
            response = post(url, headers=headers, json=data).json()



if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入地区获取天气信息

    # 公众号推送消息
    for user in users:
        send_message(user, accessToken)
    os.system("pause")
