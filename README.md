# 비행 기록 FastAPI 서버
## HTTP POST로 전송 된 비행기록을 DB Cache 및 저장하는 FastAPI 서버
> Python 3.8.10 이상에서 실행 권장

> DB는 SQLite3 사용하였음(추후 다른 DB로 변경 될 수 있음).

1. 종속성 패키지 설치
```
pip3 install -r requirements.txt
```
2. gunicorn으로 실행
```
gunicorn --bind 0:45555 main:app --worker-class uvicorn.workers.UvicornWorker --daemon
```

> 도커를 이용할 시
1. 도커 이미지 빌드
```
docker build -f DockerFile -t [이미지 이름] .
```
2. docker-compose의 환경변수 설정을 이용하여 실행.
* MARIADBHOST  : DB 호스트 주소
* MARIADBUSER  : DB 계정
* MARIADBPASS  : DB 비밀번호
* MARIADBPORT  : DB 접속 포트
* MARIADBNAME  : DB 이름
* MARIADBTABLE : DB 테이블 이름
* WEBAPIENDPOINT : 외부 API 주소
* APISERVERTEST : 서버 테스트 모드(API 요청 날리지 않음)