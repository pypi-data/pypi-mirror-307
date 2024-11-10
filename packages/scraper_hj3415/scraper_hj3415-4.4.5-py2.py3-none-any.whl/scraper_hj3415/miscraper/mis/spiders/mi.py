import scrapy
from scraper_hj3415.miscraper.mis import items


class MiSpider(scrapy.Spider):
    name = 'mi'
    allowed_domains = ['finance.naver.com']

    def start_requests(self):
        urls = {
            'aud': [self.parse_aud, 'https://finance.naver.com/marketindex/worldDailyQuote.nhn?fdtc=4&marketindexCd=FX_USDAUD'],
            'chf': [self.parse_chf, 'https://finance.naver.com/marketindex/worldDailyQuote.nhn?fdtc=4&marketindexCd=FX_USDCHF'],
            'gbond3y': [self.parse_gbond3y, 'https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y'],
            'gold': [self.parse_gold, 'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=CMDT_GC&fdtc=2'],
            'silver': [self.parse_silver, 'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=CMDT_SI&fdtc=2'],
            'usdidx': [self.parse_usdidx, 'https://finance.naver.com/marketindex/worldExchangeDetail.nhn?marketindexCd=FX_USDX'],
            'usdkrw': [self.parse_usdkrw, 'https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW'],
            'wti': [self.parse_wti, 'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=OIL_CL&fdtc=2'],
            'kosdaq': [self.parse_kosdaq, 'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSDAQ'],
            'kospi': [self.parse_kospi, 'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI'],
            'sp500': [self.parse_sp500, 'https://finance.naver.com/world/sise.nhn?symbol=SPI@SPX'],
        }
        print(f'Start scraping Market Index ...')
        for title, (func, url) in urls.items():
            yield scrapy.Request(url=url, callback=func, cb_kwargs=dict(title=title))

    def parse_sp500(self, response, title):
        print(f'<<< Parsing {title}...')
        item = items.MisItems()
        # print(response.text)

        for r in range(3, 0, -1):
            item['title'] = title
            item['date'] = response.xpath(f'//*[@id="dayTable"]/tbody/tr[{r}]/td[1]/text()').get()
            item['value'] = (response.xpath(f'//*[@id="dayTable"]/tbody/tr[{r}]/td[2]/span/text()')
                             .get().replace(',', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item

    def parse_kospi(self, response, title):
        print(f'<<< Parsing {title}...')
        item = items.MisItems()
        # print(response.text)

        for i in range(3, 6):
            item['title'] = title
            item['date'] = response.xpath(f'/html/body/div/table[1]/tr[{i}]/td[1]/text()').get()
            item['value'] = response.xpath(f'/html/body/div/table[1]/tr[{i}]/td[2]/text()').get().replace(',', '')
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item

    def parse_kosdaq(self, response, title):
        print(f'<<< Parsing {title}...')
        item = items.MisItems()
        # print(response.text)

        for r in range(3, 6):
            item['title'] = title
            item['date'] = response.xpath(f'/html/body/div/table[1]/tr[{r}]/td[1]/text()').get()
            item['value'] = response.xpath(f'/html/body/div/table[1]/tr[{r}]/td[2]/text()').get().replace(',', '')
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item

    def parse_wti(self, response, title):
        print(f'<<< Parsing {title}...')
        item = items.MisItems()
        # print(response.text)

        for r in range(3, 0, -1):
            item['title'] = title
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item

    def parse_usdkrw(self, response, title):
        print(f'<<< Parsing usd/krw ...')
        item = items.MisItems()
        # print(response.text)

        for r in range(3, 0, -1):
            item['title'] = title
            item['date'] = response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[1]/text()').get()
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[2]/text()')
                             .get().replace(',', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item

    def parse_usdidx(self, response, title):
        print(f'<<< Parsing dollar index ...')
        item = items.MisItems()
        # print(response.text)

        # 최근 데이터를 스크랩한다.
        # date - //*[@id="content"]/div[1]/div[2]/span[1]
        # value - //*[@id="content"]/div[1]/div[1]/p[1]/em
        value = []
        for span in response.xpath(f'//*[@id="content"]/div[1]/div[1]/p[1]/em/span'):
            value.append(span.xpath('text()').get())

        item['title'] = title
        item['date'] = response.xpath('//*[@id="content"]/div[1]/div[2]/span[1]/text()').get()
        item['value'] = ''.join(value)

        print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
        yield item

    def parse_silver(self, response, title):
        print(f'<<< Parsing {title}...')
        # print(response.text)
        item = items.MisItems()

        for r in range(3, 0, -1):
            item['title'] = title
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item

    def parse_gold(self, response, title):
        print(f'<<< Parsing {title}...')
        # print(response.text)
        item = items.MisItems()

        for r in range(3, 0, -1):
            item['title'] = title
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item

    def parse_gbond3y(self, response, title):
        print(f'<<< Parsing {title}...')
        # print(response.text)
        item = items.MisItems()

        for r in range(3, 0, -1):
            item['title'] = title
            item['date'] = (response.css(f'body > div > table > tbody > tr:nth-child({r}) > td.date::text')
                            .extract()[0].replace('\n', '').replace('\t', ''))
            item['value'] = (response.css(f'body > div > table > tbody > tr:nth-child({r}) > td:nth-child(2)::text')
                .extract()[0])
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item

    def parse_chf(self, response, title):
        print(f'<<< Parsing usd/{title}...')
        # print(response.text)
        item = items.MisItems()

        for r in range(3, 0, -1):
            item['title'] = title
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item

    def parse_aud(self, response, title):
        print(f'<<< Parsing usd/{title}...')
        # print(response.text)
        item = items.MisItems()

        for r in range(3, 0, -1):
            item['title'] = title
            item['date'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[1]/text()')
                            .get().replace('\t', '').replace('\n', ''))
            item['value'] = (response.xpath(f'/html/body/div/table/tbody/tr[{r}]/td[2]/text()')
                             .get().replace(',', '').replace('\t', '').replace('\n', ''))
            print(f"title: {item['title']}, date : {item['date']}, value : {item['value']}")
            yield item





