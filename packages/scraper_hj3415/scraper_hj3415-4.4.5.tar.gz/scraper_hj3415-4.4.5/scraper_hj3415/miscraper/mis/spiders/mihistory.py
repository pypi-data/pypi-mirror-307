import time
import scrapy
import random
from scrapy.selector import Selector

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from scraper_hj3415.miscraper.mis import items

# 2초 이내는 데이터 캡쳐가 올바르게 안됨
rnd_wait = [3, 4, 5]


class MIHistory(scrapy.Spider):
    name = 'mihistory'
    allowed_domains = ['finance.naver.com']

    # 버튼 클릭시 페이지가 변하는 것이 일관되지 않는것을 해결하기 위한 세팅. 챗gpt 검색
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
    }

    def __init__(self, *args, **kwargs):
        super(MIHistory, self).__init__(*args, **kwargs)
        self.webdriver = kwargs.get("webdriver", None)
        # 과거 몇년치 데이터를 모을 것인가
        self.years = kwargs.get("years", 1)

        # 대략1년전 kospi, kosdaq -> 42, gbond3y -> 38, s&p -> 27, usdkrw -> 26, wti -> 38, gold -> 38, audchf -> 46
        self.last_page_kospi_kosdaq = int(42 * self.years)
        self.last_page_3bond3y = int(38 * self.years)
        self.last_page_sp500 = int(27 * self.years)
        self.last_page_usdkrw = int(26 * self.years)
        self.last_page_wti = int(38 * self.years)
        self.last_page_gold = int(38 * self.years)
        self.last_page_silver = int(38 * self.years)
        self.last_page_audchf = int(46 * self.years)

    def start_requests(self):
        urls = {
            self.parse_kospi: [
                f'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI&page={self.last_page_kospi_kosdaq}',
                self.last_page_kospi_kosdaq],
            self.parse_kosdaq: [
                f'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSDAQ&page={self.last_page_kospi_kosdaq}',
                self.last_page_kospi_kosdaq],
            self.parse_gbond3y: [
                f'https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page={self.last_page_3bond3y}',
                self.last_page_3bond3y],
            self.parse_aud: [
                f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?fdtc=4&marketindexCd=FX_USDAUD',
                self.last_page_audchf],
            self.parse_chf: [
                f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?fdtc=4&marketindexCd=FX_USDCHF',
                self.last_page_audchf],
            self.parse_usdkrw: [
                f'https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page={self.last_page_usdkrw}',
                self.last_page_usdkrw],
            self.parse_wti: [
                f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=OIL_CL&fdtc=2&page={self.last_page_wti}',
                self.last_page_wti],
            self.parse_gold: [
                f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=CMDT_GC&fdtc=2&page={self.last_page_gold}',
                self.last_page_gold],
            self.parse_silver: [
                f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=CMDT_SI&fdtc=2&page={self.last_page_silver}',
                self.last_page_silver],
            self.parse_sp500: [
                'https://finance.naver.com/world/sise.nhn?symbol=SPI@SPX',
                self.last_page_sp500],
        }
        # reference from https://docs.scrapy.org/en/latest/topics/request-response.html
        print(f'Start scraping Market Index history...{self.years} year..')

        for func, (url, page) in urls.items():
            yield scrapy.Request(url=url, callback=func, cb_kwargs=dict(page=page))

    def parse_kospi(self, response, page):
        print(f"Parsing ...kospi {page} page")
        item = items.MisItems()
        # print(response.text)

        time.sleep(random.choice(rnd_wait))

        for i in [12, 11, 10, 5, 4, 3]:
            item['title'] = 'kospi'
            item['date'] = response.xpath(f'/html/body/div/table[1]/tr[{i}]/td[1]/text()').get()
            item['value'] = response.xpath(f'/html/body/div/table[1]/tr[{i}]/td[2]/text()').get().replace(',', '')
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item
        if page > 1:
            yield scrapy.Request(
                url=f'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI&page={page - 1}',
                callback=self.parse_kospi,
                cb_kwargs=dict(page=page - 1),
            )

    def parse_kosdaq(self, response, page):
        print(f"Parsing ...kosdaq {page} page")
        item = items.MisItems()
        # print(response.text)

        time.sleep(random.choice(rnd_wait))

        for i in [12, 11, 10, 5, 4, 3]:
            item['title'] = 'kosdaq'
            item['date'] = response.xpath(f'/html/body/div/table[1]/tr[{i}]/td[1]/text()').get()
            item['value'] = response.xpath(f'/html/body/div/table[1]/tr[{i}]/td[2]/text()').get().replace(',', '')
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item
        if page > 1:
            yield scrapy.Request(
                url=f'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSDAQ&page={page - 1}',
                callback=self.parse_kosdaq,
                cb_kwargs=dict(page=page - 1),
            )

    def parse_gbond3y(self, response, page):
        print(f"Parsing ...gbond3y {page} page")
        item = items.MisItems()
        # print(response.text)

        time.sleep(random.choice(rnd_wait))

        for i in range(7, 0, -1):
            item['title'] = 'gbond3y'
            item['date'] = (response.css(f'body > div > table > tbody > tr:nth-child({i}) > td.date::text')
                            .extract()[0].replace('\n', '').replace('\t', ''))
            item['value'] = (response.css(f'body > div > table > tbody > tr:nth-child({i}) > td:nth-child(2)::text')
                .extract()[0])
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item
        if page > 1:
            yield scrapy.Request(
                url=f'https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page={page - 1}',
                callback=self.parse_gbond3y,
                cb_kwargs=dict(page=page - 1),
                )

    def parse_aud(self, response, page):
        print(f"Parsing ...aud {page} page")
        item = items.MisItems()
        # print(response.text)

        time.sleep(random.choice(rnd_wait))

        for i in range(7, 0, -1):
            item['title'] = 'aud'
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item
        if page > 1:
            yield scrapy.Request(
                url=f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?fdtc=4&marketindexCd=FX_USDAUD&page={page - 1}',
                callback=self.parse_aud,
                cb_kwargs=dict(page=page - 1),
                )

    def parse_chf(self, response, page):
        print(f"Parsing ...chf {page} page")
        item = items.MisItems()
        # print(response.text)

        time.sleep(random.choice(rnd_wait))

        for i in range(7, 0, -1):
            item['title'] = 'chf'
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item
        if page > 1:
            yield scrapy.Request(
                url=f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?fdtc=4&marketindexCd=FX_USDCHF&page={page - 1}',
                callback=self.parse_chf,
                cb_kwargs=dict(page=page - 1),
                )

    def parse_usdkrw(self, response, page):
        print(f"Parsing ...usdkrw {page} page")
        item = items.MisItems()
        # print(response.text)

        time.sleep(random.choice(rnd_wait))

        for i in range(10, 0, -1):
            item['title'] = 'usdkrw'
            item['date'] = response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[1]/text()').get()
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[2]/text()')
                             .get().replace(',', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item
        if page > 1:
            yield scrapy.Request(
                url=f'https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page={page - 1}',
                callback=self.parse_usdkrw,
                cb_kwargs=dict(page=page - 1),
            )

    def parse_wti(self, response, page):
        print(f"Parsing ...wti {page} page")
        item = items.MisItems()
        # print(response.text)

        time.sleep(random.choice(rnd_wait))

        for i in range(7, 0, -1):
            item['title'] = 'wti'
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item
        if page > 1:
            yield scrapy.Request(
                url=f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=OIL_CL&fdtc=2&page={page - 1}',
                callback=self.parse_wti,
                cb_kwargs=dict(page=page - 1),
            )

    def parse_gold(self, response, page):
        print(f"Parsing ...gold {page} page")
        item = items.MisItems()
        # print(response.text)

        time.sleep(random.choice(rnd_wait))

        for i in range(7, 0, -1):
            item['title'] = 'gold'
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item
        if page > 1:
            yield scrapy.Request(
                url=f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=CMDT_GC&fdtc=2&page={page - 1}',
                callback=self.parse_gold,
                cb_kwargs=dict(page=page - 1),
            )

    def parse_silver(self, response, page):
        print(f"Parsing ...silver {page} page")
        item = items.MisItems()
        # print(response.text)

        time.sleep(random.choice(rnd_wait))

        for i in range(7, 0, -1):
            item['title'] = 'silver'
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{i}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item
        if page > 1:
            yield scrapy.Request(
                url=f'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=CMDT_SI&fdtc=2&page={page - 1}',
                callback=self.parse_silver,
                cb_kwargs=dict(page=page - 1),
            )

    def parse_sp500(self, response, page):
        def yield_data():
            sel = Selector(text=self.webdriver.page_source)
            for i in range(10, 0, -1):
                item['title'] = 'sp500'
                item['date'] = sel.xpath(f'//*[@id="dayTable"]/tbody/tr[{i}]/td[1]/text()').get()
                item['value'] = (sel.xpath(f'//*[@id="dayTable"]/tbody/tr[{i}]/td[2]/span/text()')
                                 .get().replace(',', ''))
                print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
                yield item

        print(f"Parsing ...sp500 get {page} tables from ({response.url}) ")
        self.webdriver.get(response.url)
        self.webdriver.implicitly_wait(3)
        item = items.MisItems()
        # print(response.text)

        # last_page_sp500은 일별시세 테이블을 몇번째까지 바꿀것인지를 뜻함.
        for i in range(1, self.last_page_sp500 + 1):
            time.sleep(random.choice(rnd_wait)-2)
            num_btn = f'//*[@id="dayLink{i}"]'
            try:
                self.webdriver.find_element(By.XPATH, num_btn).click()
            except NoSuchElementException:
                # 현재 페이지에 누를 수 있는 버튼이 없는경우.. 다음 버튼을 누른다.
                next_btn = '//*[@id="dayPaging"]/a[11]'
                self.webdriver.find_element(By.XPATH, next_btn).click()
                print(f"Click the next button...")
                time.sleep(random.choice(rnd_wait)-2)
                self.webdriver.find_element(By.XPATH, num_btn).click()

            print(f"Click the {num_btn} button...")
            time.sleep(random.choice(rnd_wait))
            # 선택한 페이지의 dayTable에서 데이터 추출함.
            yield from yield_data()
