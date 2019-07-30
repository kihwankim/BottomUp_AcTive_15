통신 네트워크 구성
===
규율
---
0. 로컬 <-> 파이 송수신 데이터는 [층번호(1byte), 파이번호(1byte), 메세지(1byte)]
1. 층 번호, 파이 번호는 1~255 사용
2. 메세지는 0~255 (253:상황발생 체크 시작, 254:상황종료(253으로 재시작 필요), 255:상황시작)

추가 작성 필요
---
1. 라즈베리파이 센서를 이용하여, 입력이 주어지면 방향을 표시
2. 예외처리
3. 상황종료 후에도 소켓 연결유지. 상황 재발생시 유용성
4. 모듈화, 코드정리
5. 메인컨트롤러 <-> 네트워크 컨트롤러 작업 조율(Queue)

고려사항
---
1. 작업의 조율
2. 필요없는 스레드, 소켓의 종료
3. 병렬화 : thread? pool? gevent? conccurrent.futures?
4. 예외 처리 : try / except / else / finally

기록
---

### 7/13(전승민)
사용모듈 : Queue, Thread  
큰 그림의 로직 작성. 세부 로직은 계속 다듬어야함  
사용모듈은 판단에 따라 더 좋은걸로 변경

### 7/14(전승민)
사용모듈 : Queue, Thread  
송수신 데이터 포맷은 (파이번호 : 1byte 숫자, 메세지 : 1byte 숫자).  
파이번호는 1번부터 사용하고, 메세지가 255라면, 재난상황 시작을 의미  
로컬<->파이2개 양방향 동시 통신완료

라즈베리파이에서 센서를 이용하여  
온도를 체크하고 안전여부 반환하는 함수와, 입력이 주어지면 방향을 표시하는 함수 필요

### 7/15(전승민)
사용모듈 : Queue, Thread  

기능추가  
1. 각종 예외처리
2. 로컬 : 연결 시도, 연결 성공+연결한 파이 정보, 연결 끊킴, 사용가능한 파이 번호 출력
3. 파이 : 연결 성공, 연결 실패, 사용가능한 파이 번호

### 7/16(전승민)
1. 층 정보도 이용하도록 수정

### 7/17(전승민)
1. 네트워크 컨트롤러 코드 정리 : 송신, 수신을 담당할 클래스 작성
 - 네트워크 컨트롤러에는 Sender들을 관리할 SendManager 싱글톤 객체 생성  
 - 송신은 SendManager 하나를 통해서, 수신은 각각의 Receiver 스레드를 통해서.
 - 새로운 연결을 받아 들일때마다 Sender 생성해서 SendManager에 추가, Recevier 생성해서 스레드로 수신시작

### 7/19(전승민)
메인컨트롤러의 유동성 있는 동작을 위해, 네트워크를 다룰 수 있도록 수정

### 7/16(배지훈)
GPIO를 이용한 온도센서 작동확인 및 LED전구 정상작동확인
1. 온도를 체크하고 안전여부 반환하는 함수 구현
- Emergency Situation에서는 False를 반환, Normal Situation에서는 True를 반환
2. 사용자의 입력값에 따른 LED Turn on
- 향후 데이터 값에 따른 센서 작동을 위한 코드 테스팅

### 7/17(전승민)
1. 네트워크 컨트롤러 코드 정리 : 송신, 수신을 담당할 클래스 작성
 - 네트워크 컨트롤러에는 Sender들을 관리할 SendManager 싱글톤 객체 생성  
 - 송신은 SendManager 하나를 통해서, 수신은 각각의 Receiver 스레드를 통해서.
 - 새로운 연결을 받아 들일때마다 Sender 생성해서 SendManager에 추가, Recevier 생성해서 스레드로 수신시작

### 7/19(배지훈)
1. 7/16일 작업내용 참고 사이트 https://m.blog.naver.com/chandong83/220902795488
2. 온습도센서 DHT11
- 측정가능 온도: 섭씨 0도 ~ 50도 (오차 범위 +,- 2도)
3. 온습도센서 DHT22
- 측정가능 온도: 섭씨 -40도 ~ 80도 (오차 범위, +,-0.5도)
- 측정 간격 : 0.1도
4. LCD I2C 작동 환경 구현 참고사이트
- https://moondals.wordpress.com/2016/05/01/raspberry-pi%EC%99%80-python%EC%9C%BC%EB%A1%9C-1602-lcd-%EB%AC%B8%EC%9E%90-%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/
- https://www.raspberrypi-spy.co.uk/2015/05/using-an-i2c-enabled-lcd-screen-with-the-raspberry-pi/
- https://torrms.tistory.com/42
5. LCD I2C 테스팅 완료(출력 디자인 완성)
- 참고: 6개의 LCD 중 4개 불량

### 7/22 (배지훈)
1. LCD I2C 모듈 Direction 표시 테스트 성공
2. GPIO 참고사이트 추가 https://m.blog.naver.com/audiendo/220771658560
3. DHT11 온습도 센서 추가 정보 사이트 http://blog.foobargem.com/blog/2016/03/27/how-to-read-dht-series-of-humidity-and-temperature-sensors-on-a-raspberry-pi/

### 7/24 (배지훈)
1. LCD I2C 모듈 Direction 표시 및 String 표시 테스트 완료
2. 온습도 센서(DHT11, DHT22) 조사자료 정리

### 7/25 (배지훈)
1. LED 모듈 연결 및 테스트(성공)
2. LED 모듈과 LCD 모듈 동시 테스트 완료(성공)

참고사항
---
코드중 #####는 에러 유망주

희망사항
---
1. range 대신 enumerate
2. 실행도중 정점(파이)을 더 추가할 수 있게?
