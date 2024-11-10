import logging
import argparse
from utils_hj3415 import noti, utils, helpers
from scraper_hj3415.nfscraper import run as nfs_run
from decouple import Config, RepositoryEnv
import os
# import pprint

db_logger = helpers.setup_logger('db_logger', logging.INFO)


def load_env_to_environ(env_filename):
    # .env 파일을 읽어와 Config 객체로 로드
    project_root = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(project_root, env_filename)
    repo = RepositoryEnv(env_path)

    os.environ['MONGO_ADDR'] = repo.data['MONGO_ADDR']
    os.environ['REDIS_ADDR'] = repo.data['REDIS_ADDR']

    # 설정된 환경변수 확인
    print("MONGO_ADDR (환경변수):", os.getenv('MONGO_ADDR'))
    print("REDIS_ADDR (환경변수):", os.getenv('REDIS_ADDR'))


def db_manager():
    parser = argparse.ArgumentParser(description="데이터베이스 주소 관리 프로그램")
    db_subparsers = parser.add_subparsers(dest='db_type', help='데이터베이스 종류를 지정하세요(mongo, redis)', required=True)

    # 'mongo' 명령어 서브파서
    mongo_parser = db_subparsers.add_parser('mongo', help=f"mongodb 데이터베이스")
    mongo_subparser = mongo_parser.add_subparsers(dest='command', help='mongodb 데이터베이스 관련된 명령')

    # mongo - repair 파서
    mongo_repair_parser = mongo_subparser.add_parser('repair', help=f"mongodb의 모든 종목의 컬렉션 유효성을 확인하고 없으면 채웁니다.")
    mongo_repair_parser.add_argument('targets', nargs='*', type=str, help="대상 종목 코드를 입력하세요. 'all'을 입력하면 전체 종목을 대상으로 합니다.")
    mongo_repair_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # 'redis' 명령어 서브파서
    redis_parser = db_subparsers.add_parser('redis', help=f"redis 데이터베이스")
    redis_subparser = redis_parser.add_subparsers(dest='command', help='redisdb 데이터베이스 관련된 명령')

    # redis - reset 파서
    redis_subparser.add_parser('reset', help=f"redis 주소를 기본값으로 초기화합니다.")

    args = parser.parse_args()

    if args.db_type in ['mongo', 'redis']:
        if args.db_type == 'mongo' and args.command == 'repair':
            from db_hj3415 import mymongo
            if len(args.targets) == 1 and args.targets[0] == 'all':
                all_codes_in_db = mymongo.Corps.list_all_codes()
                print(f"**** 모든 종목({len(all_codes_in_db)})의 데이터베이스를 검사합니다. ****")
                missing_dict = mymongo.Corps.chk_integrity(*all_codes_in_db)
            else:
                # 입력된 종목 코드 유효성 검사
                invalid_codes = [code for code in args.targets if not utils.is_6digit(code)]
                if invalid_codes:
                    print(f"다음 종목 코드의 형식이 잘못되었습니다: {', '.join(invalid_codes)}")
                    return
                print(f"**** {args.targets} 종목의 데이터베이스를 검사합니다. ****")
                missing_dict = mymongo.Corps.chk_integrity(*args.targets)

            repairable_codes = list(missing_dict.keys())
            if len(repairable_codes) != 0:
                print(f"**** {repairable_codes} 종목에서 이상이 발견되어서 스크랩하겠습니다. ****")
                nfs_run.all_spider(*repairable_codes)
                if args.noti:
                    noti.telegram_to('manager', f"{repairable_codes}의 데이터베이스를 수리했습니다.")
        else:
            parser.print_help()
    else:
        parser.print_help()

if __name__ == '__main__':
    print(get_env('dev'))