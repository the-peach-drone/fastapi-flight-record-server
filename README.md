# 비행 기록 FastAPI 서버
## HTTP POST로 전송 된 비행기록을 DB Cache 및 저장하는 FastAPI 서버
> Python 3.8.10 이상에서 실행 권장

1. 도커 이미지 빌드
```
docker build --no-cache -f DockerFile -t [이미지 이름] .
```

2. docker-compose의 환경변수 설정을 이용하여 실행
* MARIADBHOST  : DB 호스트 주소
* MARIADBUSER  : DB 계정
* MARIADBPASS  : DB 비밀번호
* MARIADBPORT  : DB 접속 포트
* WEBAPIENDPOINT : 외부 API 주소