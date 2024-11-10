import scrapy
import time
from scrapy.selector import Selector
from selenium.webdriver.remote.webdriver import WebDriver

from scraper_hj3415.nfscraper.nfs import items
from scraper_hj3415.nfscraper import common


'''
# XPATH 상수
손익계산서 = '//*[@id="rpt_tab1"]'
재무상태표 = '//*[@id="rpt_tab2"]'
현금흐름표 = '//*[@id="rpt_tab3"]'
연간 = '//*[@id="frqTyp0"]'
분기 = '//*[@id="frqTyp1"]'
검색 = '//*[@id="hfinGubun"]'
'''


class C103(scrapy.Spider):
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
        super(C103, self).__init__(*args, **kwargs)
        self.codes = kwargs.get("codes", [])
        self.webdriver = kwargs.get("webdriver", None)

    @staticmethod
    def make_df(webdriver: WebDriver, code: str, page: str):
        # html에서 table을 추출하여 dataframe생성
        html = Selector(text=webdriver.page_source)
        table_xpath = '//table[2]'

        df = common.get_df_from_html(html, table_xpath, 1)
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
                url=f'https://navercomp.wisereport.co.kr/v2/company/c1030001.aspx?cmp_cd={one_code}',
                callback=getattr(self, 'parse_c103'),
                cb_kwargs=dict(code=one_code)
            )


class C103YSpider(C103):
    name = 'c103y'

    # 순서 바꾸지 말것
    btns = {
        "손익계산서y": [
            ('손익계산서', '//*[@id="rpt_tab1"]'),
            # ('연간', '//*[@id="frqTyp0"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
        "재무상태표y": [
            ('재무상태표', '//*[@id="rpt_tab2"]'),
            # ('연간', '//*[@id="frqTyp0"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
        "현금흐름표y": [
            ('현금흐름표', '//*[@id="rpt_tab3"]'),
            # ('연간', '//*[@id="frqTyp0"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
    }

    def __init__(self, *args, **kwargs):
        super(C103YSpider, self).__init__(*args, **kwargs)

    def parse_c103(self, response, code):
        print(f'<<< Parsing C103Y ...{code}')
        self.webdriver.get(response.url)
        self.webdriver.implicitly_wait(10)
        for title, btn_list in C103YSpider.btns.items():
            page = self.name[:-1] + title
            print(f"Making dataframe - {code} / {page}..")
            common.click_buttons(self.webdriver, btn_list)
            yield from C103.make_df(self.webdriver, code, page)


class C103QSpider(C103):
    name = 'c103q'

    # 순서 바꾸지 말것
    btns = {
        "손익계산서q": [
            ('손익계산서', '//*[@id="rpt_tab1"]'),
            ('분기', '//*[@id="frqTyp1"]'),
            ('검색', '//*[@id="hfinGubun"]'),
        ],
        "재무상태표q": [
            ('재무상태표', '//*[@id="rpt_tab2"]'),
            # ('분기', '//*[@id="frqTyp1"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
        "현금흐름표q": [
            ('현금흐름표', '//*[@id="rpt_tab3"]'),
            # ('분기', '//*[@id="frqTyp1"]'),
            # ('검색', '//*[@id="hfinGubun"]'),
        ],
    }

    def __init__(self, *args, **kwargs):
        super(C103QSpider, self).__init__(*args, **kwargs)

    def parse_c103(self, response, code):
        print(f'<<< Parsing C103Q ...{code}')
        self.webdriver.get(response.url)
        self.webdriver.implicitly_wait(10)
        for title, btn_list in C103QSpider.btns.items():
            page = self.name[:-1] + title
            print(f"Making dataframe - {code} / {page}..")
            common.click_buttons(self.webdriver, btn_list)
            yield from C103.make_df(self.webdriver, code, page)
