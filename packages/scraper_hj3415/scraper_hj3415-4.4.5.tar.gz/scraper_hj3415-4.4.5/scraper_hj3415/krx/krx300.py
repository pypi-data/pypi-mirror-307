import logging
import time
import os
import shutil
import datetime

import sqlite3
import pandas as pd
from io import StringIO
from typing import List

import selenium.common.exceptions
from webdriver_hj3415 import drivers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db_hj3415 import mymongo
from scraper_hj3415.nfscraper import run as nfs_run

from utils_hj3415 import helpers

scraper_logger = helpers.setup_logger('scraper_logger', logging.WARNING)

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = os.path.join(WORKING_DIR, '_down_krx')
EXCEL_FILEPATH = os.path.join(TEMP_DIR, 'PDF_DATA.xls')
DB_FILEPATH= os.path.join(WORKING_DIR, 'krx.db')

def _is_file_old(file_path: str, period: int = 30) -> bool:
    # 파일의 생성 시간 가져오기
    try:
        creation_time = os.path.getctime(file_path)
    except FileNotFoundError:
        scraper_logger.error(f"{os.path.basename(file_path)}이 없습니다.")
        return True
    creation_time_readable = datetime.datetime.fromtimestamp(creation_time)
    now = datetime.datetime.now()

    scraper_logger.debug(f"파일 경로: {file_path}")
    scraper_logger.debug(f"파일 생성 시간: {creation_time_readable}")
    scraper_logger.debug(f"현재 시간: {now}")

    timedelta = now - creation_time_readable

    if timedelta.days >= period:
        scraper_logger.warning(f"{os.path.basename(file_path)}은 기준값 {period}일 보다 오래 되었습니다.({timedelta.days}일전 생성됨) ")
        return True
    else:
        scraper_logger.info(f"{os.path.basename(file_path)}은 기준값 {period}일 보다 오래 되지 않았습니다..({timedelta.days}일전 생성됨) ")
        return False


def _download_krx300(headless=False):
    """
    tigeretf 사이트에서 krx300 구성종목 파일을 다운로드한다.
    파일다운은 save_to 에 설정된 파일경로를 사용한다.
    :return:
    """
    # 임시폴더 정리
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

    print(f'Download krx300 file and save to {TEMP_DIR}.')
    # tiger etf krx300 주소
    url = "https://www.tigeretf.com/ko/product/search/detail/index.do?ksdFund=KR7292160009"

    webdriver = drivers.get_chrome(headless=headless, temp_dir=TEMP_DIR)

    webdriver.get(url)
    webdriver.implicitly_wait(10)

    # 구성 종목 다운 버튼
    btn_xpath = '//*[@id="formPdfList"]/div[2]/div[1]/div/div/a'

    trying = 0
    while trying < 3:
        try:
            WebDriverWait(webdriver, 10).until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
            button = webdriver.find_element(By.XPATH, btn_xpath)
            button.click()
            time.sleep(2)  # 파일 다운로드 대기
            break
        except selenium.common.exceptions.TimeoutException:
            trying += 1
            scraper_logger.error("다운로드 버튼이 준비되지 않아서 다시 시도합니다.")
            webdriver.refresh()
            time.sleep(2)
            if trying >= 3:
                raise Exception(f"{url} 페이지 로딩에 문제가 있습니다.")
    webdriver.close()


def make_db(period: int, headless: bool):
    scraper_logger.info(f"krx300 사이트에서 데이터를 받아 {os.path.basename(DB_FILEPATH)}로 저장합니다.(갱신주기 {period}일)")
    # krx 종목구성 파일이 30일이전 것이라면 새로 받는다.
    if _is_file_old(EXCEL_FILEPATH, period):
        scraper_logger.info(f"{os.path.basename(EXCEL_FILEPATH)}파일이 오래되어 새로 다운 받습니다.")
        _download_krx300(headless=headless)
    else:
        scraper_logger.info(f"{os.path.basename(EXCEL_FILEPATH)}파일이 아직 갱신주기 전이라 그대로 사용합니다.")

    # 파일 읽기 시도
    trying = 0
    while trying < 3:
        try:
            with open(EXCEL_FILEPATH, 'r', encoding='utf-8') as file:
                html_content = file.read()
            break
        except FileNotFoundError:
            trying += 1
            scraper_logger.error(f"{EXCEL_FILEPATH} 파일이 없습니다. 다운로드 시도 중...")
            _download_krx300(headless=headless)
            if trying >= 3:
                raise Exception(f"{EXCEL_FILEPATH} 파일 다운로드에 문제가 있습니다.")

    # HTML 형식의 데이터를 DataFrame으로 변환
    df = pd.read_html(StringIO(html_content), skiprows=2, header=0, index_col=0)[0]

    if os.path.exists(DB_FILEPATH):
        os.remove(DB_FILEPATH)
        scraper_logger.info(f"{os.path.basename(DB_FILEPATH)} 파일이 삭제 되었습니다.")

    # SQLite에 데이터 저장
    with sqlite3.connect(DB_FILEPATH) as conn:
        tablename = 'krx300'
        df.to_sql(tablename, conn, if_exists='replace', index=False)
    creation_time = os.path.getctime(DB_FILEPATH)
    creation_time_readable = datetime.datetime.fromtimestamp(creation_time)
    scraper_logger.info(f"{os.path.basename(DB_FILEPATH)}({creation_time_readable}) 파일이 새로 생성 되었습니다.")


def get_codes() -> list:
    if not os.path.exists(DB_FILEPATH):
        scraper_logger.warning(f"{os.path.basename(DB_FILEPATH)} 파일이 존재하지 않아 새로 생성합니다.")
        make_db(period=7, headless=True)
    with sqlite3.connect(DB_FILEPATH) as conn:
        # 종목코드와 종목명을 가져오는 쿼리
        query = f"SELECT 종목코드 FROM krx300 WHERE 종목코드 LIKE '______'"
        codes = pd.read_sql(query, conn)['종목코드'].tolist()
    return codes

def get_code_names() -> List[list]:
    if not os.path.exists(DB_FILEPATH):
        scraper_logger.warning(f"{os.path.basename(DB_FILEPATH)} 파일이 존재하지 않아 새로 생성합니다.")
        make_db(period=7, headless=True)
    with sqlite3.connect(DB_FILEPATH) as conn:
        # 종목코드와 종목명을 가져오는 쿼리
        query = f"SELECT 종목코드, 종목명 FROM krx300 WHERE 종목코드 LIKE '______'"
        code_names = pd.read_sql(query, conn).values.tolist()
    return code_names

# 종목명으로 종목코드를 찾는 함수
def get_name(code: str):
    for code_sql, name_sql in get_code_names():
        if code == code_sql:
            return name_sql
    return None  # 종목명을 찾지 못한 경우 None 반환

def sync_with_mongo():
    in_mongo_codes = mymongo.Corps.list_all_codes()
    in_sqlite_codes = get_codes()
    scraper_logger.info(f"In mongodb: {len(in_mongo_codes)} - {in_mongo_codes}")
    scraper_logger.info(f"In sqlite3: {len(in_sqlite_codes)} - {in_sqlite_codes}")

    del_difference = list(set(in_mongo_codes) - set(in_sqlite_codes))
    add_difference = list(set(in_sqlite_codes) - set( in_mongo_codes))

    if len(add_difference) == 0 and len(del_difference) == 0:
        print(f"mongodb와 krx300의 sync는 일치합니다.(총 {len(in_mongo_codes)} 종목)")
    else:
        print(f"mongodb에서 삭제될 코드: {len(del_difference)} - {del_difference}")
        print(f"mongodb에 추가될 코드: {len(add_difference)} - {add_difference}")

        # 몽고디비에서 불필요한 종목 삭제하고 서버에 기록.
        for code in del_difference:
            mymongo.Logs.save(table='db', log_text=f"{code}/{mymongo.Corps.get_name(code)}를 삭제 했습니다.")
            mymongo.Corps.drop_code(code)

        # 몽고디비에 새로운 종목 추가하고 서버에 기록.
        if len(add_difference) != 0:
            nfs_run.all_spider(*add_difference)
            for code in add_difference:
                mymongo.Logs.save(table='db', log_text=f"{code}/{get_name(code)}을 추가 했습니다.")




