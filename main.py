from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from datetime import datetime, timedelta
import time

eng_mons = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
driver = webdriver.Chrome("chromedriver.exe")


def input_write(id, text, flag=False):
    elem = driver.find_element(By.ID, id)
    # elem.clear()
    elem.click()
    elem.send_keys(Keys.CONTROL + "A")  # ctrl + a 단축키
    elem.send_keys(text)

    if flag:
        elem.send_keys(Keys.ENTER)


def select_write(id, text, flag=False):
    elem = driver.find_element(By.ID, id)
    select = Select(elem)
    select.select_by_index(text)
    time.sleep(0.5)

    if flag:
        elem.send_keys(Keys.ENTER)

def getInputValue(id):
    elem = driver.find_element(By.ID, id)
    value = elem.get_attribute("value")
    return value

def getDateRange(start, end):
    start_day = datetime.strptime(start, "%Y-%m-%d")
    end_day = datetime.strptime(end, "%Y-%m-%d")

    dates = [(start_day + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end_day - start_day).days + 1)]
    return dates


def getSolarData(d):
    save_data = ''

    date = d.split('-')
    # 년
    input_write('yearbox', date[0])
    # 월
    input_write('mosbox', eng_mons[int(date[1]) - 1])
    # 일
    select_write('daybox', str(int(date[2]) - 1), True)

    sunrise_sunset = getSunrise_sunset()  # 일출 일몰 시간

    # sunrise = datetime.strptime(sunrise_sunset[0], "%H:%M")
    # sunset = datetime.strptime(sunrise_sunset[1], "%H:%M")
    # diff_minute = int((sunrise - sunset).seconds / 60) #시간 차이 분

    st_h = int(sunrise_sunset[0].split(":")[0])
    st_m = int(sunrise_sunset[0].split(":")[1])
    ed_h = int(sunrise_sunset[1].split(":")[0])
    ed_m = int(sunrise_sunset[1].split(":")[1])



    # 일출 일몰 시간 입력
    input_write('hrbox', st_h, True)
    input_write('scbox', "00", True)

    h = st_h
    m = st_m

    while True:
        input_write('mnbox', m, True)
        time.sleep(0.1)

        az = getInputValue('azbox')
        noon = getInputValue('noonbox')
        el = getInputValue('elbox')

        save_data += d + ' ' + str(h).zfill(2) + ':' + str(m).zfill(2) + "\t" +sunrise_sunset[0]+ "\t" +sunrise_sunset[1]+ "\t" +noon + '\t' + az +  '\t' + el + "\n"
        print(d + ' ' + str(h).zfill(2) + ':' + str(m).zfill(2) + '\t' + noon + '\t' + az + "\t" +  el + "\n")

        if (h == ed_h) & (m == ed_m):
            break

        m += 1

        if m == 60:
            h += 1
            m = 0
            input_write('hrbox', h, True)
            time.sleep(0.1)
    return save_data

def getSunrise_sunset():
    sunrise = getInputValue("risebox")
    sunset = getInputValue("setbox")

    return [sunrise, sunset]


if __name__ == '__main__':
    start = '2020-01-01'
    end = '2020-12-31'
    filename = "result/result_2020.txt"
    file = open(filename, 'w')
    file.write("datetime\tsunrise\tsunset\tnoon\tAz\tEl\n")

    dates = getDateRange(start, end)

    url = "https://gml.noaa.gov/grad/solcalc/"
    driver.get(url)

    input_write('latbox', "36.851221")
    input_write('lngbox', "127.152924")

    input_write('tz', "Asia/Seoul", True)

    for d in dates:
        text = getSolarData(d)
        file.write(text)
        # print(date)
    # file.close()
