import time
import pandas as pd
from typing import Tuple, List
from io import StringIO
import random

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from utils_hj3415 import helpers

scraper_logger = helpers.setup_logger('scraper_logger')

# 2초 이내는 데이터 캡쳐가 올바르게 안됨
rnd_wait = [3, 4, 5]


def click_buttons(driver: WebDriver, buttons: List[Tuple[str, str]]) -> bool:
    """
    하부 클래스에서 buttons 리스트를 입력받아 실제 버튼을 클릭하는 함수
    :return: 함수 작업이 무사히 완료되면 True
    """
    scraper_logger.debug(f'*** Setting page by clicking buttons ***')
    # print(buttons)
    for name, xpath in buttons:
        # print(f'- Click the {name} / {xpath} button')
        try:
            # 엘리먼트가 로드될 때까지 x초 대기
            element = WebDriverWait(driver, random.choice(rnd_wait) * 2).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            # 엘리먼트 클릭
            # element.click()
            driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            print(f"{name} 엘리먼트를 찾지 못했습니다.")
            return False
        time.sleep(random.choice(rnd_wait))
    scraper_logger.debug('*** Buttons click done ***')
    return True


def get_df_from_html(selector, xpath, table_num):
    """
    C103,C104에서 사용
    펼치지 않은 네이버 테이블의 항목과 내용을 pandas 데이터프레임으로 변환시킴
    reference from http://hleecaster.com/python-pandas-selecting-data/(pandas 행열 선택)
    reference from https://blog.naver.com/wideeyed/221603778414(pandas 문자열 처리)
    reference from https://riptutorial.com/ko/pandas/example/5745/dataframe-%EC%97%B4-%EC%9D%B4%EB%A6%84-%EB%82%98%EC%97%B4(pandas 열이름 나열)
    """
    # 전체 html source에서 table 부위만 추출하여 데이터프레임으로 변환
    tables_list = []
    for table in selector.xpath(xpath).getall():
        tables_list.append(StringIO(table))

    df = pd.read_html(tables_list[table_num])[0]

    # 항목열의 펼치기 스트링 제거
    df['항목'] = df['항목'].str.replace('펼치기', '').str.strip()
    # reference from https://stackoverflow.com/questions/3446170/escape-string-for-use-in-javascript-regex(정규표현식 특수기호처리)
    # 인덱스행의 불필요한 스트링 제거
    df.columns = (df.columns.str.replace('연간컨센서스보기', '', regex=False)
                  .str.replace('연간컨센서스닫기', '', regex=False)
                  .str.replace('(IFRS연결)', '', regex=False)
                  .str.replace('(IFRS별도)', '', regex=False)
                  .str.replace('(GAAP개별)', '', regex=False)
                  .str.replace('(YoY)', '', regex=False)
                  .str.replace('(QoQ)', '', regex=False)
                  .str.replace('(E)', '', regex=False)
                  .str.replace('.', '', regex=False)
                  .str.strip())
    return df
