import requests
from config_drone import BaseConfig as Config

# LDM과 드론을 연결한 후 대기(폴링 기법), 가시화 모듈에서 요청을 보내면(START_CHECKLIST) 체크리스트 수행
result = requests.get(Config.LDM_ADDRESS + 'check/drone_poling')

# 체크리스트 수행 요청이 들어오면 점검 시작
if result.text == 'START_CHECKLIST':
    # TODO: 체크리스트 수행
    # 이상 없으면 다음과 같은 요청 보냄
    requests.get(Config.LDM_ADDRESS + 'check/drone_checklist_result')
