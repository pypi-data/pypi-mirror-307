import scrapy
from scraper_hj3415.nfscraper.nfs import items

# 여러 잡다한 기호를 없애거나 교체하는 람다함수
def cleaning(s):
    if s is None or s == 'N/A':
        return None
    return (
        s.strip().replace('\t', '').replace('\r', '').replace('\n', '').replace(',', '')
        .replace('원', '').replace('주', '').replace('억', '00000000').replace('%', '')
    )

# CSS Path 생성 함수
def css_path(i, j=None):
    if j:
        return f'#pArea>div.wrapper-table>div>table>tr:nth-child({i})>td>dl>dt:nth-child({j})>'
    return f'#cTB11>tbody>tr:nth-child({i})>'

# None일 때 빈 문자열 반환
def str_or_blank(s):
    return '' if s is None else str(s)

class C101Spider(scrapy.Spider):
    name = 'c101'
    allowed_domains = ['navercomp.wisereport.co.kr']  # https 주소

    def __init__(self, *args, **kwargs):
        super(C101Spider, self).__init__(*args, **kwargs)
        self.codes = kwargs.get("codes", [])

    def start_requests(self):
        total_count = len(self.codes)
        self.logger.info(f'Start scraping {self.name}, {total_count} items...')
        for one_code in self.codes:
            url = f'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={one_code}'
            yield scrapy.Request(url=url, callback=self.parse_c101, cb_kwargs=dict(code=one_code))

    def parse_c101(self, response, code):
        self.logger.info(f'Parsing {self.name} for {code}')
        item = items.C101items()

        try:
            item['date'] = (response.xpath('//*[@id="wrapper"]/div[1]/div[1]/div[1]/dl/dd[2]/p/text()').get()
                            .replace('[기준:', '').replace(']', ''))
        except AttributeError:
            self.logger.error(f'ERROR: Page not found for {code}')
            return

        item.update({
            'code': cleaning(response.css(css_path(1, 1) + 'b::text').get()),
            'page': 'c101',
            '종목명': response.css(css_path(1, 1) + 'span::text').get(),
            '업종': response.css(css_path(1, 4).rstrip('>') + '::text').get().replace('WICS : ', ''),
            'EPS': cleaning(response.css(css_path(3, 1) + 'b::text').get()),
            'BPS': cleaning(response.css(css_path(3, 2) + 'b::text').get()),
            'PER': cleaning(response.css(css_path(3, 3) + 'b::text').get()),
            '업종PER': cleaning(response.css(css_path(3, 4) + 'b::text').get()),
            'PBR': cleaning(response.css(css_path(3, 5) + 'b::text').get()),
            '배당수익률': cleaning(response.css(css_path(3, 6) + 'b::text').get()),
            '주가': cleaning(response.css(css_path(1) + 'td>strong::text').get()),
        })

        # 52주 최고/최저, 거래량/거래대금, 발행주식/유동비율 등 데이터 처리
        try:
            최고최저52주 = response.css(css_path(2) + 'td::text').get().split('/')
            item['최고52주'], item['최저52주'] = map(cleaning, 최고최저52주)

            거래량거래대금 = response.css(css_path(4) + 'td::text').get().split('/')
            item['거래량'], item['거래대금'] = map(cleaning, 거래량거래대금)

            발행주식유동비율 = response.css(css_path(7) + 'td::text').get().split('/')
            item['발행주식'], item['유동비율'] = map(cleaning, 발행주식유동비율)
        except (AttributeError, ValueError):
            self.logger.error(f'Parsing error for {code}')

        item.update({
            '시가총액': cleaning(response.css(css_path(5) + 'td::text').get()),
            '베타52주': cleaning(response.css(css_path(6) + 'td::text').get()),
            '외국인지분율': cleaning(response.css(css_path(8) + 'td::text').get()),
            'intro1': str_or_blank(response.xpath('//*[@id="wrapper"]/div[5]/div[2]/ul/li[1]/text()').get()),
            'intro2': str_or_blank(response.xpath('//*[@id="wrapper"]/div[5]/div[2]/ul/li[2]/text()').get()),
            'intro3': str_or_blank(response.xpath('//*[@id="wrapper"]/div[5]/div[2]/ul/li[3]/text()').get()),
        })

        self.logger.info(item)
        yield item