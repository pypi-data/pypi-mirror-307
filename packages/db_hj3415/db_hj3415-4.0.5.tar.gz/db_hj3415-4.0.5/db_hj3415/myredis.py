"""
redis 서버를 이용해서 mongodb의 데이터를 캐시한다.
데이터의 캐시 만료는 데이터를 업데이트 시키는 모듈인 scraper_hj3415에서 담당하고
여기서 재가공해서 만들어지는 데이터는 만료기간을 설정한다.
장고에서 필요한 데이터를 보내는 기능이 주임.
"""
import logging
import os
from json import JSONDecodeError

import redis
from db_hj3415 import mymongo
import json
from utils_hj3415 import utils,helpers
from typing import Tuple, List, Callable, Any, Optional
import datetime
from scraper_hj3415.krx import krx300

db_logger = helpers.setup_logger('db_logger', logging.WARNING)


def connect_to_redis(addr: str) -> redis.Redis:
    conn_str = f"Connect to Redis ..."
    print(conn_str, f"Server Addr : {addr}")
    return redis.Redis(host=addr, port=6379, db=0)


class Base:
    redis_client = connect_to_redis(os.getenv('REDIS_ADDR', 'redis'))

    # 기본 Redis 캐시 만료 시간 (1시간)
    DEFAULT_CACHE_EXPIRATION_SEC = 3600

    def __init__(self):
        if Base.redis_client is None:
            raise ValueError("myredis.Base.redis_client has not been initialized!")

    @classmethod
    def exists(cls, key_name: str) -> bool:
        # 키가 존재하는지 확인
        if cls.redis_client.exists(key_name):
            return True
        else:
            return False

    @classmethod
    def get_ttl(cls, redis_name: str) -> Optional[int]:
        # 해당 키의 남은 시간(TTL) 확인
        ttl = cls.redis_client.ttl(redis_name)

        if ttl == -1:
            db_logger.warning(f"{redis_name}는 만료 시간이 설정되어 있지 않습니다.")
        elif ttl == -2:
            db_logger.warning(f"{redis_name}는 Redis에 존재하지 않습니다.")
        else:
            db_logger.info(f"{redis_name}의 남은 시간은 {ttl}초입니다.")
            return ttl


    @classmethod
    def delete(cls, redis_name: str):
        """
        redis_name 에 해당하는 키/값을 삭제하며 원래 없으면 아무일 없음
        :param redis_name:
        :return:
        """
        db_logger.debug(Base.list_redis_names())
        cls.redis_client.delete(redis_name)
        db_logger.debug(Base.list_redis_names())

    @classmethod
    def delete_all_with_pattern(cls, pattern: str) -> bool:
        """
        pattern에 해당하는 모든 키를 찾아서 삭제한다.
        :param pattern: ex) 005930.c101* - 005930.c101로 시작되는 모든키 삭제
        :return:
        """
        # print(Redis.list_redis_names())
        # SCAN 명령어를 사용하여 패턴에 맞는 키를 찾고 삭제
        cursor = '0'
        while cursor != 0:
            cursor, keys = cls.redis_client.scan(cursor=cursor, match=pattern, count=1000)
            if keys:
                cls.redis_client.delete(*keys)

        db_logger.debug(Base.list_redis_names())
        return True

    @classmethod
    def list_redis_names(cls) -> list:
        """
        전체 레디스 아이템을 리스트로 반환한다.
        :return:
        """
        # byte를 utf-8로 디코드하고 정렬함.
        return sorted([item.decode('utf-8') for item in cls.redis_client.keys('*')])

    @classmethod
    def get_cached_data(cls, redis_name: str) -> str:
        """
        Redis에서 캐시된 데이터를 가져옵니다.
        :param redis_name:
        :return: 반환된 형식은 json 타입의 문자열로 json.loads()를 사용하여 리스트나 딕셔너리로 변환해서 사용해야함.
        """
        cached_data = cls.redis_client.get(redis_name)
        if cached_data is None:
            return None
        else:
            db_logger.debug(type(cached_data.decode('utf-8')))
            return json.loads(cached_data.decode('utf-8'))

    @classmethod
    def set_cached_data(cls, redis_name: str, data: Any, expiration_sec: int) -> None:
        """Redis에 데이터를 캐싱하고 만료 시간을 설정합니다."""
        cls.redis_client.setex(redis_name, expiration_sec, json.dumps(data))
        db_logger.info(f"Redis 캐시에 저장 (만료시간: {expiration_sec}초) - redis_name : {redis_name}")

    @classmethod
    def fetch_and_cache_data(cls, redis_name: str, refresh: bool, fetch_function: Callable, *args, timer=DEFAULT_CACHE_EXPIRATION_SEC) -> Any:
        """
        캐시에서 데이터를 가져오거나, 없으면 fetch_function을 호출하여 데이터를 계산 후 캐싱합니다.
        :param redis_name: 저장할 레디스이름
        :param refresh: 캐시에 데이터가 있어도 무조건 데이터베이스를 이용하여 캐시를 리프레시한다.
        :param fetch_function: 데이터베이스에서 데이터를 가지고 오는 함수
        :param timer: 캐시만료시간(초) - 기본 3600초(1시간)
        :param args: fetch_function에서 인자가 있는경우 사용한다.
        :return: 데이터 값은 json.loads()로 후처리를 해야할 수 있다.
        """
        if not refresh:
            cached_data = cls.get_cached_data(redis_name)
            if cached_data:
                ttl_hours = round(cls.redis_client.ttl(redis_name) / timer, 1)
                db_logger.info(f"Redis 캐시에서 데이터 가져오기 (남은시간: {ttl_hours} 시간) - redis_name : {redis_name}")
                db_logger.debug(type(cached_data))
                db_logger.debug(cached_data)
                if isinstance(cached_data, str):
                    try:
                        # 리스트나 딕셔너리의 경우 json.loads()으로 한번더 변환해야함.
                        return json.loads(cached_data)
                    except JSONDecodeError:
                        # 그냥 문자열인 경우
                        return cached_data
                else:
                    # cached_data 이미 리스트나 딕셔너리로 넘어온 경우
                    return cached_data

        # 캐시된 데이터가 없거나 refresh=True인 경우
        data = fetch_function(*args)

        if data:
            cls.set_cached_data(redis_name=redis_name, data=data, expiration_sec=timer)
        return data


class DartToday(Base):
    redis_name = 'dart_today'

    def save(self, data: List[dict]):
        # 이전 내용을 삭제하고...
        self.delete(self.redis_name)
        # 데이터를 Redis에 캐싱, 60분후 키가 자동으로 제거됨
        self.set_cached_data(self.redis_name, json.dumps(data), Base.DEFAULT_CACHE_EXPIRATION_SEC)


    def get(self) -> List[dict]:
        cached_data = self.get_cached_data(self.redis_name)
        db_logger.debug(type(cached_data))
        db_logger.debug(cached_data)
        if cached_data is None:
            db_logger.debug(f"dart today data : []")
            return []
        else:
            # rcept_no를 기준으로 정렬한다.
            sorted_list = sorted(json.loads(cached_data), key=lambda x: x['rcept_no'])
            db_logger.debug(f"dart today data(total:{len(sorted_list)}) : {sorted_list[:1]}..")
            return sorted_list


class Corps(Base):
    COLLECTIONS = mymongo.Corps.COLLECTIONS

    def __init__(self, code: str = '', page: str = ''):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        assert page in self.COLLECTIONS, f'Invalid value : {page}({self.COLLECTIONS})'
        self.code_page = code + '.' + page
        self._code = code
        self._page = page
        # redis에서 name으로 사용하는 변수의 기본으로 문미에 문자열을 추가로 첨가해서 사용하는 역할을 함.
        super().__init__()

    def __str__(self):
        return f"redis name : {self.code_page}"

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        self.code_page = code + self.code_page[6:]
        db_logger.info(f'Change code : {self.code} -> {code}')
        self._code = code

    @property
    def page(self) -> str:
        return self._page

    @page.setter
    def page(self, page: str):
        assert page in self.COLLECTIONS, f'Invalid value : {page}({self.COLLECTIONS})'
        self.code_page = self.code_page[:7] + page
        db_logger.info(f'Change page : {self.page} -> {page}')
        self._page = page

    def get_name(self, data_from='krx', refresh=False) -> Optional[str]:
        """
        종목명을 반환한다. 데이터소스는 data_from 인자로 결정하며 krx 또는 mongo가 가능하다.
        :param data_from: ['krx', 'mongo']
        :param refresh:
        :return:
        """
        redis_name = self.code + '_name'

        def fetch_get_name(code: str, data_from_in: str) -> str:
            """
            종목명을 반환한다. 데이터소스는 data_from인자로 결정하며 krx 또는 mongo가 가능하다.
            :param code:
            :param data_from_in: ['krx', 'mongo']
            :return:
            """
            assert data_from_in in ['krx', 'mongo'], "data_from 인자는 krx 또는 mongo 중 하나입니다."
            if data_from_in == 'krx':
                db_logger.info(f"{code} 종목명으로 krx로부터 받아옵니다.")
                return krx300.get_name(code)
            elif data_from_in == 'mongo':
                db_logger.info(f"{code} 종목명으로 mongo.C101로부터 받아옵니다.")
                return mymongo.Corps.get_name(code)

        return self.fetch_and_cache_data(redis_name, refresh, fetch_get_name, self.code, data_from)

    @classmethod
    def list_all_codes(cls, refresh=False) -> list:
        """
        redis_name = 'all_codes'
        :return:
        """
        redis_name = 'all_codes'

        def fetch_list_all_codes() -> list:
            codes = []
            for db_name in mymongo.Corps.list_db_names():
                if utils.is_6digit(db_name):
                    codes.append(db_name)
            return sorted(codes)

        return cls.fetch_and_cache_data(redis_name, refresh, fetch_list_all_codes)

    @classmethod
    def list_all_codes_names(cls, refresh=False) -> dict:
        """
        redis_name = 'all_codes_names'
        :return:
        """
        redis_name = 'all_codes_names'

        def fetch_list_all_codes_names() -> dict:
            corps = {}
            for code in cls.list_all_codes(refresh):
                corps[code] = mymongo.Corps.get_name(code)
            return corps

        return cls.fetch_and_cache_data(redis_name, refresh, fetch_list_all_codes_names)

    @classmethod
    def _list_rows(cls, func: mymongo.Corps, redis_name: str, refresh=False) -> list:
        """
        C103468에서 내부적으로 사용
        :param func:
        :param redis_name:
        :return:
        """
        def fetch_list_rows(func_in: mymongo.Corps) -> list:
            db_logger.debug(func_in.list_rows())
            return func_in.list_rows()
        return cls.fetch_and_cache_data(redis_name, refresh, fetch_list_rows, func)


class C101(Corps):
    def __init__(self, code: str):
        super().__init__(code, 'c101')
        self.mymongo_c101 = mymongo.C101(code)

    @property
    def code(self) -> str:
        return super().code

    @code.setter
    def code(self, code: str):
        # 부모의 세터 프로퍼티를 사용하는 코드
        super(C101, self.__class__).code.__set__(self, code)
        self.mymongo_c101.code = self.code

    def get_recent(self, refresh=False) -> dict:
        # code_page 앞 11글자가 코드와 c101 페이지임.
        redis_name = self.code_page + '_recent'

        def fetch_get_recent() -> dict:
           return self.mymongo_c101.get_recent(merge_intro=True)

        return self.fetch_and_cache_data(redis_name, refresh, fetch_get_recent)

    def get_trend(self, title: str, refresh=False) -> dict:
        """
        title에 해당하는 데이터베이스에 저장된 모든 값을 {날짜: 값} 형식의 딕셔너리로 반환한다.

        title should be in ['BPS', 'EPS', 'PBR', 'PER', '주가', '배당수익률', '베타52주', '거래량']

        리턴값 - 주가
        {'2023.04.05': '63900',
         '2023.04.06': '62300',
         '2023.04.07': '65000',
         '2023.04.10': '65700',
         '2023.04.11': '65900',
         '2023.04.12': '66000',
         '2023.04.13': '66100',
         '2023.04.14': '65100',
         '2023.04.17': '65300'}
        """
        # code_page 앞 11글자가 코드와 c101 페이지임.
        redis_name = self.code_page + '_trend'

        def fetch_get_trend(title_in) -> dict:
            return self.mymongo_c101.get_trend(title_in)

        return self.fetch_and_cache_data(redis_name, refresh, fetch_get_trend, title)


class C1034(Corps):
    def __init__(self, code: str, page: str):
        super().__init__(code, page)
        # 자식 클래스에서 C103이나 C104를 생성해서 할당함
        self.mymongo_c1034: Optional[mymongo.C1034] = None

    @property
    def code(self) -> str:
        return super().code

    @code.setter
    def code(self, code: str):
        # 부모의 세터 프로퍼티를 사용하는 코드
        super(C1034, self.__class__).code.__set__(self, code)
        self.mymongo_c1034.code = code

    @property
    def page(self) -> str:
        return super().page

    @page.setter
    def page(self, page: str):
        # 부모의 세터 프로퍼티를 사용하는 코드
        super(C1034, self.__class__).page.__set__(self, page)
        self.mymongo_c1034.page = page

    def list_rows(self, refresh=False):
        redis_name = self.code_page + '_rows'
        return super()._list_rows(self.mymongo_c1034, redis_name, refresh)

    def list_row_titles(self, refresh=False) -> list:
        redis_name = self.code_page + '_list_row_titles'

        def fetch_list_row_titles() -> list:
            return self.mymongo_c1034.list_row_titles()

        return self.fetch_and_cache_data(redis_name, refresh, fetch_list_row_titles)

    def latest_value(self, title: str, pop_count = 2, refresh=False) -> Tuple[str, float]:
        redis_name = self.code_page + f'_latest_value_pop{pop_count}_' + title

        def fetch_latest_value(title_in: str, pop_count_in: int) -> Tuple[str, float]:
            return self.mymongo_c1034.latest_value(title_in, pop_count_in)

        return self.fetch_and_cache_data(redis_name, refresh, fetch_latest_value, title, pop_count)

    def latest_value_pop2(self, title: str, refresh=False) -> Tuple[str, float]:
        redis_name = self.code_page + '_latest_value_pop2_' + title

        def fetch_latest_value_pop2(title_in: str) -> Tuple[str, float]:
            return self.mymongo_c1034.latest_value(title_in)

        return self.fetch_and_cache_data(redis_name, refresh, fetch_latest_value_pop2, title)

    def find(self, row_title: str, remove_yoy=False, del_unnamed_key=True, refresh=False) -> Tuple[int, dict]:
        """
        :param row_title: 해당하는 항목을 반환한다.
        :param remove_yoy: 전분기대비, 전년대비를 삭제할지 말지
        :param del_unnamed_key: Unnamed키를 가지는 항목삭제
        :param refresh:
        :return: 중복된 항목은 합쳐서 딕셔너리로 반환하고 중복된 갯수를 정수로 반환
        """
        if remove_yoy:
            suffix = '_find_without_yoy_'
        else:
            suffix = '_find_with_yoy_'

        redis_name = self.code_page + suffix + row_title

        def fetch_find(row_title_in: str, remove_yoy_in, del_unnamed_key_in) -> Tuple[int, dict]:
            return self.mymongo_c1034.find(row_title=row_title_in, remove_yoy=remove_yoy_in, del_unnamed_key=del_unnamed_key_in)

        return self.fetch_and_cache_data(redis_name, refresh, fetch_find, row_title, remove_yoy, del_unnamed_key)

    def find_yoy(self, row_title: str, refresh=False) -> float:
        """
        항목에서 전월/분기 증감율만 반환한다.
        중복되는 title 은 첫번째것 사용
        :param row_title:
        :param refresh:
        :return:
        """
        redis_name = self.code_page + '_find_yoy_' + row_title

        def fetch_find_yoy(row_title_in: str) -> float:
            return self.mymongo_c1034.find_yoy(row_title_in)

        return self.fetch_and_cache_data(redis_name, refresh, fetch_find_yoy, row_title)

    def sum_recent_4q(self, row_title: str, refresh=False) -> Tuple[str, float]:
        redis_name = self.code_page + '_sum_recent_4q_' + row_title

        def fetch_sum_recent_4q(row_title_in: str) -> Tuple[str, float]:
            return self.mymongo_c1034.sum_recent_4q(row_title_in)

        return self.fetch_and_cache_data(redis_name, refresh, fetch_sum_recent_4q, row_title)


class C103(C1034):
    PAGES = mymongo.C103.PAGES

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q', 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y'
        """
        super().__init__(code, page)
        self.mymongo_c1034 = mymongo.C103(code, page)


class C104(C1034):
    PAGES = mymongo.C104.PAGES

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c104y', 'c104q
        """
        super().__init__(code, page)
        self.mymongo_c1034 = mymongo.C104(code, page)


class C106(Corps):
    PAGES = mymongo.C106.PAGES

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c106y', 'c106q
        """
        super().__init__(code, page)
        self.mymongo_c106 = mymongo.C106(code, page)

    @property
    def code(self) -> str:
        return super().code

    @code.setter
    def code(self, code: str):
        # 부모의 세터 프로퍼티를 사용하는 코드
        super(C106, self.__class__).code.__set__(self, code)
        self.mymongo_c106.code = code

    @property
    def page(self) -> str:
        return super().page

    @page.setter
    def page(self, page: str):
        # 부모의 세터 프로퍼티를 사용하는 코드
        super(C106, self.__class__).page.__set__(self, page)
        self.mymongo_c106.page = page

    def list_row_titles(self, refresh=False) -> list:
        redis_name = self.code_page + '_list_row_titles'

        def fetch_list_row_titles() -> list:
            return self.mymongo_c106.list_row_titles()

        return self.fetch_and_cache_data(redis_name, refresh, fetch_list_row_titles)

    def list_rows(self, refresh=False):
        redis_name = self.code_page + '_rows'
        return super()._list_rows(self.mymongo_c106, redis_name, refresh)

    def find(self, row_title: str, refresh=False) -> dict:
        redis_name = self.code_page + '_find_' + row_title

        def fetch_find(row_title_in: str) -> dict:
            return self.mymongo_c106.find(row_title_in)

        return self.fetch_and_cache_data(redis_name, refresh, fetch_find, row_title)

    @classmethod
    def make_like_c106(cls, code: str, page: str, title: str, refresh=False) -> dict:
        redis_name = code + '.c106' + '_make_like_c106_' + page + '_' + title

        def fetch_make_like_c106(code_in, page_in, title_in) -> dict:
            return mymongo.C106.make_like_c106(code_in, page_in, title_in)

        return cls.fetch_and_cache_data(redis_name, refresh, fetch_make_like_c106, code, page, title)

    def get_rivals(self, refresh=False) -> list:
        redis_name = self.code_page + '_rivals'

        def fetch_get_rivals() -> list:
            return self.mymongo_c106.get_rivals()

        return self.fetch_and_cache_data(redis_name, refresh, fetch_get_rivals)


class C108(Corps):
    def __init__(self, code: str):
        super().__init__(code, 'c108')
        self.mymongo_c108 = mymongo.C108(code)

    @property
    def code(self) -> str:
        return super().code

    @code.setter
    def code(self, code: str):
        # 부모의 세터 프로퍼티를 사용하는 코드
        super(C108, self.__class__).code.__set__(self, code)
        self.mymongo_c108.code = code

    def list_rows(self, refresh=False):
        redis_name = self.code_page + '_rows'
        return super()._list_rows(self.mymongo_c108, redis_name, refresh)

    def get_recent_date(self, refresh=False) -> datetime.datetime | None:
        redis_name = self.code_page + '_get_recent_date'

        def fetch_get_recent_date() -> str:
            # json은 datetime 형식은 저장할 수 없어서 문자열로 저장한다.
            recent_date = self.mymongo_c108.get_recent_date()
            if recent_date is None:
                str_data_in = ''
            else:
                str_data_in = recent_date.isoformat()
            return str_data_in

        str_data = self.fetch_and_cache_data(redis_name, refresh, fetch_get_recent_date)
        if str_data == '':
            return None
        else:
            return datetime.datetime.fromisoformat(str_data)

    def get_recent(self, refresh=False) -> Optional[List[dict]]:
        redis_name = self.code_page + '_recent'

        def fetch_get_recent() -> Optional[List[dict]]:
            return self.mymongo_c108.get_recent()

        return self.fetch_and_cache_data(redis_name, refresh, fetch_get_recent)


class MI(Base):
    def __init__(self, index: str):
        """mi 데이터베이스 클래스

        Note:
            db - mi\n
            col - 'aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi', 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx' - 총 13개\n
            doc - date, value\n
        """
        assert index in mymongo.MI.COL_TITLE, f'Invalid value : {index}({mymongo.MI.COL_TITLE})'
        self.mymongo_mi = mymongo.MI(index)
        self.mi_index = 'mi' + '.' + index
        self._index = index
        super().__init__()

    def __str__(self):
        return f"redis name : {self.mi_index}"

    @property
    def index(self) -> str:
        return self._index

    @index.setter
    def index(self, index: str):
        assert index in mymongo.MI.COL_TITLE, f'Invalid value : {index}({mymongo.MI.COL_TITLE})'
        db_logger.info(f'Change index : {self.index} -> {index}')
        self.mymongo_mi.index = index
        self.mi_index = self.mi_index[:3] + index
        self._index = index

    def get_recent(self, refresh=False) -> Tuple[str, float]:
        redis_name = self.mi_index + '_recent'

        def fetch_get_recent() -> Tuple[str, float]:
            return self.mymongo_mi.get_recent()

        return self.fetch_and_cache_data(redis_name, refresh, fetch_get_recent)

    def get_trend(self, refresh=False) -> dict:
        redis_name = self.mi_index + '_trend'

        def fetch_get_trend() -> dict:
            return self.mymongo_mi.get_trend()

        return self.fetch_and_cache_data(redis_name, refresh, fetch_get_trend)
