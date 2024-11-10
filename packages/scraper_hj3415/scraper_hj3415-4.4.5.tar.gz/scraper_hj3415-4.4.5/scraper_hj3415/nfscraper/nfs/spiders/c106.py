import time
import scrapy
import pandas as pd
import selenium.common.exceptions
from scrapy.selector import Selector
from io import StringIO

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from scraper_hj3415.nfscraper.nfs import items

# 분기와 년도 2페이지를 스크랩함.


class C106Spider(scrapy.Spider):
    name = 'c106'
    allowed_domains = ['navercomp.wisereport.co.kr']

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
    }

    def __init__(self, *args, **kwargs):
        super(C106Spider, self).__init__(*args, **kwargs)
        self.codes = kwargs.get("codes", [])
        self.webdriver = kwargs.get("webdriver", None)

    def start_requests(self):
        total_count = len(self.codes)
        self.logger.info(f'entire codes list - {self.codes}')
        for i, one_code in enumerate(self.codes):
            # C106의 컬럼명을 얻기 위한 주소
            yield scrapy.Request(
                url=f'https://navercomp.wisereport.co.kr/v2/company/c1060001.aspx?cmp_cd={one_code}',
                callback=self.parse_c106_col,
                cb_kwargs=dict(code=one_code)
            )

    def parse_c106_col(self, response, code):
        print(f'<<< Parsing C106 columns ...{code}')
        self.webdriver.get(response.url)
        self.webdriver.implicitly_wait(10)
        WebDriverWait(self.webdriver, 10).until(
            EC.visibility_of_all_elements_located((By.ID, "cTB611_h"))
        )
        try:
            html = Selector(text=self.webdriver.page_source)
        except selenium.common.exceptions.UnexpectedAlertPresentException:
            self.logger.warning("Parsing error ... maybe 올바른 종목이 아닙니다.")
        else:
            # 컬럼명을 얻어 다음 request에 실어 보낸다.
            cols = []
            for i in range(1, 7):
                title_elements = html.xpath(f'//*[@id="cTB611_h"]/thead/tr/th[{i}]/text()').getall()
                # print(title_elements)
                try:
                    title_name = title_elements[0].strip().replace('.','')
                except IndexError:
                    raise Exception(f"IndexError: {title_elements}")
                if title_name == '항목':
                    cols.append('항목')
                    continue
                try:
                    title_code = title_elements[1].strip()
                except IndexError:
                    title_code = ''
                # 인덱스에 공칸일 경우 데이터베이스 저장시 에러가 발생하기 때문에 추가한 코드
                if title_name == '':
                    title_name = 'Unnamed'
                cols.append(title_name + '/' + title_code)
            print(f'{self.name} column names - {code} >>>> {cols}')

            titles = ['y', 'q']     # pipeline에서 테이블명으로 됨
            for title in titles:
                # C106의 내부의 iframe주소, 분기와 연간 2개임
                # reference from https://docs.scrapy.org/en/latest/topics/request-response.html (request 연쇄보내기)
                # ex - https://navercomp.wisereport.co.kr/company/cF6002.aspx?cmp_cd=005930&finGubun=MAIN&cmp_cd1=&cmp_cd2=&cmp_cd3=&cmp_cd4=&sec_cd=G453010&frq=Y
                yield scrapy.Request(
                    url=f'https://navercomp.wisereport.co.kr/company/cF6002.aspx?cmp_cd={code}'
                        f'&finGubun=MAIN&cmp_cd1=&cmp_cd2=&cmp_cd3=&cmp_cd4=&sec_cd=G453010&frq={title.upper()}',
                    callback=self.parse_c106_iframe,
                    cb_kwargs=dict(code=code, cols=cols, title=title)
                )

    def parse_c106_iframe(self, response, code, cols, title):
        time.sleep(2)
        print(f'<<< Parsing C106 iframes ...{code}')
        page = ''.join(['c106', title])
        print(f"Making dataframe - {code} / {page}..")
        df = C106Spider.get_df_from_html(response.text, cols)
        df['항목'] = (df['항목']
                    .str.replace(r'\(억\)', '', regex=True)
                    .str.replace(r'\(원\)', '', regex=True)
                    .str.replace(r'\(억원\)', '', regex=True)
                    .str.replace(r'\(%\)', '', regex=True))
        # print(df)
        # make item to yield
        item = items.C103468items()
        item['code'] = code
        item['page'] = page
        item['df'] = df
        yield item

    @staticmethod
    def get_df_from_html(html, cols):
        # 전체 html source에서 table 부위만 추출하여 데이터프레임으로 변환
        html_io = StringIO(html)
        df = pd.read_html(html_io)[0]
        # 인덱스 추가
        df.columns = cols
        df.dropna(how='all', inplace=True)
        return df

