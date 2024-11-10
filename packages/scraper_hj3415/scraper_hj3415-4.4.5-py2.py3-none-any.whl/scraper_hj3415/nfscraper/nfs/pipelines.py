import logging
import sys
from itemadapter import ItemAdapter
from db_hj3415 import mymongo, myredis
from pymongo.errors import BulkWriteError
from utils_hj3415 import noti, helpers

scraper_logger = helpers.setup_logger('scraper_logger', logging.WARNING)


class ValidationPipeline:
    def process_item(self, item, spider):
        print(f"\tIn ValidationPipeline.. code : {item['code']} / page : {item['page']}")
        if spider.name == 'c101':
            scraper_logger.info(f"Raw data - EPS:{item['EPS']} BPS:{item['BPS']} PER:{item['PER']} PBR:{item['PBR']}")
            if mymongo.Base.is_there(db=item['code'], table='c104q'):
                c104q = mymongo.C104(item['code'], 'c104q')
                scraper_logger.debug(f"EPS : {c104q.find('EPS', remove_yoy=True)[1]}")
                scraper_logger.debug(f"BPS : {c104q.find('BPS', remove_yoy=True)[1]}")
                d, cal_eps = c104q.sum_recent_4q('EPS')  # 최근 4분기 eps값을 더한다.
                d, cal_bps = c104q.latest_value('BPS')  # 마지막 분기 bps값을 찾는다.

                # per, pbr을 구하는 람다함수
                cal_ratio = (lambda eps_bps, pprice:
                             None if eps_bps is None or eps_bps == 0 else round(int(pprice) / int(eps_bps), 2))
                try:
                    cal_per = cal_ratio(cal_eps, item['주가'])
                    cal_pbr = cal_ratio(cal_bps, item['주가'])
                except ValueError:
                    scraper_logger.info("유효하지 않은 c104q 데이터로 인해 별도 계산 없이 c101 데이터를 사용합니다..")
                else:
                    scraper_logger.info(f"Calc data - EPS:{cal_eps} BPS:{cal_bps} PER:{cal_per} PBR:{cal_pbr}")
                    item['EPS'], item['BPS'], item['PER'], item['PBR'] = cal_eps, cal_bps, cal_per, cal_pbr
            else:
                scraper_logger.info("c104q 데이터가 없어서 별도 계산 없이 c101 데이터를 사용합니다..")
        elif 'c103' in spider.name:
            pass
        elif 'c104' in spider.name:
            pass
        elif spider.name == 'c106':
            pass
        elif spider.name == 'c108':
            pass
        return item


class RedisPipeline:
    def process_item(self, item, spider):
        print(f"\tIn RedisPipeline.. code : {item['code']} / page : {item['page']}")
        if spider.name == 'c101':
            pattern = item['code'] + '.c101*'
        elif 'c103' in spider.name:
            pattern = item['code'] + '.c103*'
        elif spider.name == 'c104y':
            pattern = item['code'] + '.c104y*'
        elif spider.name == 'c104q':
            pattern = item['code'] + '.c104q*'
        elif spider.name == 'c106':
            pattern = item['code'] + '.c106*'
        elif spider.name == 'c108':
            pattern = item['code'] + '.c108*'
        else:
            raise Exception
        print(f"\t\tDelete redis data has a pattern '{pattern}'")
        myredis.Base.delete_all_with_pattern(pattern)
        return item


class MongoPipeline:
    def process_item(self, item, spider):
        print(f"\tIn MongoPipeline.. code : {item['code']} / page : {item['page']}")
        if spider.name == 'c101':
            # print(item)
            mymongo.C101.save(item['code'], ItemAdapter(item).asdict())
        elif 'c103' in spider.name:
            # pprint.pprint(item['df'])
            mymongo.C103.save(item['code'], item['page'], item['df'])
        elif 'c104' in spider.name:
            # pprint.pprint(item['df'])
            try:
                mymongo.C104.save(item['code'], item['page'], item['df'])
            except BulkWriteError as e:
                err_str = f"{item['code']} / {item['page']} 서버 저장에 문제가 있습니다.({str(e)[:60]}..)"
                print('\t\t' + err_str, file=sys.stderr)
                noti.telegram_to('manager', err_str)
        elif spider.name == 'c106':
            # pprint.pprint(item['df'])
            mymongo.C106.save(item['code'], item['page'], item['df'])
        elif spider.name == 'c108':
            # pprint.pprint(item['df'].to_dict('records'))
            mymongo.C108.save(item['code'], item['df'])
        return item
