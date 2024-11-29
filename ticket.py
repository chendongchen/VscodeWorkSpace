import requests
import random
import time

# 配置信息
BASE_URL = 'https://kyfw.12306.cn'
LOGIN_URL = BASE_URL + '/otn/login/userLogin'
CHECK_TICKET_URL = BASE_URL + '/otn/leftTicket/queryTicketPrice'
SELECT_TICKET_URL = BASE_URL + '/otn/leftTicket/submitOrderRequest'

# 用户信息
USERNAME = 'your_username'
PASSWORD = 'your_password'
TRAIN_DATE = '2025-10-01'
FROM_STATION = '北京'
TO_STATION = '上海'
TRAIN_NUMBER = 'G1'

# 登录函数
def login(session):
    payload = {
        'username': USERNAME,
        'password': PASSWORD
    }
    response = session.post(LOGIN_URL, data=payload)
    if response.status_code == 200:
        print("登录成功")
    else:
        print("登录失败")
        exit(1)

# 检查车票状态
def check_ticket_status(session):
    params = {
        'train_date': TRAIN_DATE,
        'from_station': FROM_STATION,
        'to_station': TO_STATION,
        'purpose_codes': 'ADULT'
    }
    response = session.get(CHECK_TICKET_URL, params=params)
    if response.status_code == 200:
        ticket_data = response.json()
        for train in ticket_data['data']:
            if train['train_no'] == TRAIN_NUMBER:
                return train['canWebBuy']
    return False

# 抢票函数
def select_ticket(session):
    payload = {
        'secretStr': 'your_secret_str',  # 这里需要从查询结果中获取
        'train_date': TRAIN_DATE,
        'from_station': FROM_STATION,
        'to_station': TO_STATION,
        'purpose_codes': 'ADULT',
        'passengerTicketStr': '1,0,1,张三,1,320123199001011234,18612345678,N',
        'oldPassengerStr': '张三,1,320123199001011234,1_'
    }
    response = session.post(SELECT_TICKET_URL, data=payload)
    if response.status_code == 200:
        result = response.json()
        if result['status']:
            print("抢票成功")
        else:
            print("抢票失败:", result['messages'])
    else:
        print("抢票失败")

# 主函数
def main():
    with requests.Session() as session:
        login(session)
        while True:
            ticket_status = check_ticket_status(session)
            if ticket_status:
                select_ticket(session)
                break
            else:
                print("车票不可抢，等待1-10ms后重试...")
                time.sleep(random.uniform(0.001, 0.01))

if __name__ == '__main__':
    main()