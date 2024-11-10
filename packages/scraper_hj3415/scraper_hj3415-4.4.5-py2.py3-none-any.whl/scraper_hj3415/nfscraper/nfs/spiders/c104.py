import time
import scrapy
from scrapy.selector import Selector
from selenium.webdriver.remote.webdriver import WebDriver

from scraper_hj3415.nfscraper.nfs import items
from scraper_hj3415.nfscraper import common

'''
# XPATH 상수
수익성 = '//*[ @id="val_tab1"]'
성장성 = '//*[ @id="val_tab2"]'
안정성 = '//*[ @id="val_tab3"]'
활동성 = '//*[ @id="val_tab4"]'

연간 = '//*[@id="frqTyp0"]'
분기 = '//*[@id="frqTyp1"]'
검색 = '//*[@id="hfinGubun"]'

가치분석연간 = '//*[@id="frqTyp0_2"]'
가치분석분기 = '//*[@id="frqTyp1_2"]'
가치분석검색 = '//*[@id="hfinGubun2"]'
'''


class C104(scrapy.Spider):
    name = 'c104'
    allowed_domains = ['navercomp.wisereport.co.kr']

    # 버튼 클릭시 페이지가 변하는 것이 일관되지 않는것을 해결하기 위한 세팅. 챗gpt 검색
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
    }

    def __init__(self, *args, **kwargs):
        super(C104, self).__init__(*args, **kwargs)
        self.codes = kwargs.get("codes", [])
        self.webdriver = kwargs.get("webdriver", None)

    @staticmethod
    def make_df(webdriver: WebDriver, code: str, page: str, title: str):
        # html에서 table을 추출하여 dataframe생성
        html = Selector(text=webdriver.page_source)
        table_xpath = '//table[@class="gHead01 all-width data-list"]'

        # 테이블명을 _을 기준으로 나눠 리스트를 만든다.
        title_list = title.split('_')

        # dataframe 리스트를 만든다.
        df_list = []
        for i in range(2):
            # 상위테이블 0, 하위테이블 1
            df_list.append(common.get_df_from_html(html, table_xpath, i))
        # print(df_list)

        # 테이블명리스트와 df리스트를 매치하여 데이터베이스에 저장하기 위해 yield시킴
        for _, df in list(zip(title_list, df_list)):
            # print(df)
            # make item to yield
            item = items.C103468items()
            item['code'] = code
            item['page'] = page
            item['df'] = df
            yield item

    def start_requests(self):
        # reference from https://docs.scrapy.org/en/latest/topics/request-response.html
        total_count = len(self.codes)
        print(f'Start scraping {self.name}, {total_count} items...')
        self.logger.info(f'entire codes list - {self.codes}')

        # 실제로 페이지를 스크랩하기위해 호출
        for i, one_code in enumerate(self.codes):
            yield scrapy.Request(
                url=f'https://navercomp.wisereport.co.kr/v2/company/c1040001.aspx?cmp_cd={one_code}',
                callback=getattr(self, 'parse_c104'),
                cb_kwargs=dict(code=one_code)
            )


class C104YSpider(C104):
    name = 'c104y'
    # 순서를 바꾸지 말것
    btns = {
        '수익성y_가치분석y': [
            ('수익성', '//*[ @id="val_tab1"]'),
            # ('연간', '//*[@id="frqTyp0"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
            ('가치분석연간', '//*[@id="frqTyp0_2"]'),
            # ('가치분석검색', '//*[@id="hfinGubun2"]'),
        ],
        '성장성y': [
            ('성장성', '//*[ @id="val_tab2"]'),
            # ('연간', '//*[@id="frqTyp0"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
        '안정성y': [
            ('안정성', '//*[ @id="val_tab3"]'),
            # ('연간', '//*[@id="frqTyp0"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
        '활동성y': [
            ('활동성', '//*[ @id="val_tab4"]'),
            # ('연간', '//*[@id="frqTyp0"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
    }

    def __init__(self, *args, **kwargs):
        super(C104YSpider, self).__init__(*args, **kwargs)

    def parse_c104(self, response, code):
        print(f'<<< Parsing C104Y ...{code}')
        self.webdriver.get(response.url)
        self.webdriver.implicitly_wait(10)
        for title, btn_list in C104YSpider.btns.items():
            print(f"Making dataframe - {code} / c104y {title}..")
            common.click_buttons(self.webdriver, btn_list)
            yield from C104.make_df(self.webdriver, code, 'c104y', title)


class C104QSpider(C104):
    name = 'c104q'

    # 순서를 바꾸지 말것
    btns = {
        '수익성q_가치분석q': [
            ('수익성', '//*[ @id="val_tab1"]'),
            ('분기', '//*[@id="frqTyp1"]'),
            ('검색', '//*[@id="hfinGubun"]'),
            ('가치분석분기', '//*[@id="frqTyp1_2"]'),
            ('가치분석검색', '//*[@id="hfinGubun2"]'),
        ],
        '성장성q': [
            ('성장성', '//*[ @id="val_tab2"]'),
            # ('분기', '//*[@id="frqTyp1"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
        '안정성q': [
            ('안정성', '//*[ @id="val_tab3"]'),
            # ('분기', '//*[@id="frqTyp1"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
        '활동성q': [
            ('활동성', '//*[ @id="val_tab4"]'),
            # ('분기', '//*[@id="frqTyp1"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
    }

    def __init__(self, *args, **kwargs):
        super(C104QSpider, self).__init__(*args, **kwargs)

    def parse_c104(self, response, code):
        print(f'<<< Parsing C104Q ...{code}')
        self.webdriver.get(response.url)
        self.webdriver.implicitly_wait(10)
        for title, btn_list in C104QSpider.btns.items():
            print(f"Making dataframe - {code} / c104q {title}..")
            common.click_buttons(self.webdriver, btn_list)
            yield from C104.make_df(self.webdriver, code, 'c104q', title)








