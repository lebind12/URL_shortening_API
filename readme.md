# 백엔드 코딩 과제

## URL 단축 서비스 개발하기

- Framework: fastapi
- Database: sqlite
- Library: alembic, venv

### 데이터베이스 사용

- sqlite 사용.
- 이유:
  1. 제출의 용이함.
     - DB 서버를 열어둘 필요가 없다.
     - 외부 종속이 거의 필요하지않다.
  2. 테스트의 간편함
     - 언제든지 사용가능하고 테스트 값을 입력하기도 편리하다.
     - 채점 시 테스트 데이터를 입력 및 삭제 후 확인이 간편하다.

## API 명세

### POST /api/shorten

- 요청 본문: `{"url" : "<original_url>"}`

  아래와 같이 expire_date를 추가할 수 있습니다.

  ```
  {
    "url" : "<original_url>",
    "expire_date": "YYYY-MM-DD HH:MM:SS"
  }
  ```

- 응답 본문: `{"short_url": "<shortened_url>"}`

  - 정상응답: 201 created

  - 오류 발생시

    - 422 Unprocessable Content : 날짜 포맷이 맞지 않거나 url이 입력되지 않은경우

### GET /<shorten_key>

- 요청 본문: 없음
- 응답 본문:
  - 정상응답: 301 Moved Permanently
  - 오류 발생시
    - 404 Not Found: 만료된 링크거나 없는 링크인 경우.

### GET /api/stats/<short_key>

- 요청 본문: 없음
- 응답 본문:
  - 정상응답:
  ```
  {
      key: <short_key>,
      views: int
  }
  ```
  - 오류 발생시
    - 404 Not Found: 만료된 링크거나 없는 링크인 경우.
