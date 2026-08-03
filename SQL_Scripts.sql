-- mySQL 내 inventory DB 생성
CREATE DATABASE IF NOT EXISTS inventory DEFAULT CHARACTER SET utf8mb4

-- inventory DB 내 users 테이블 생성
CREATE Table IF NOT EXISTS users (
									id int PRIMARY KEY AUTO_INCREMENT,
                                    username VARCHAR(20) UNIQUE NOT NULL,
                                    password VARCHAR(50) NOT NULL
                                    )
-- users 테이블 내 값 입력                      
INSERT INTO users (username, password)
VALUES ('admin', 'admin')

-- 메인 창 재고 정보란에서 출력할 erp 데이터 테이블 생성
CREATE TABLE erp (
										id INT PRIMARY KEY AUTO_INCREMENT,
                    관리번호 VARCHAR(30) UNIQUE NOT NULL,
                    분류 VARCHAR(30) NOT NULL,
                    자재명 VARCHAR(100) NOT NULL,
                    재고수량 INT NOT NULL,
                    수량단위 VARCHAR(10) NOT NULL,
                    재고단가 INT NOT NULL,
                    단가단위 VARCHAR(10) NOT NULL,
                    업데이트 Date NOT NULL,
                    등록자 VARCHAR(20) NOT NULL
                    )

-- erp 테이블 내 값 입력
INSERT INTO erp (관리번호, 분류, 자재명, 재고수량, 수량단위, 재고단가, 단가단위, 업데이트, 등록자)
VALUES  ('mod_000001', '모듈', '80Ah_V사_3P8S', 20, 'ea', 9700000, 'KRW', '2026.07.01', '김진태')
				('cel_000001', '셀', '80Ah_V사_360*20*15', 300, 'ea', 33000, 'KRW', '2026.05.15', '김진태'),
				('exp_000001', '소모품', '가압지그_370*25*20', 500, 'set', 150000, 'KRW', '2026.04.02', '김진태'),
	      ('exp_000002', '소모품', '볼트_M6_60', 500, 'ea', 500, 'KRW', '2026.04.02', '김진태'),
	      ('too_000001', '공구', '육각렌치', 2, 'ea', 89000, 'KRW', '2025.10.11', '김진태'),
	      ('too_000002', '공구', '드라이버', 2, 'ea', 23000, 'KRW', '2025.10.11', '김진태')

-- erp 변경 이력 관리 위한 erp_history 테이블 생성
CREATE TABLE erp_history (
    이력번호 INT AUTO_INCREMENT PRIMARY KEY,
    작업구분 VARCHAR(10) NOT NULL,
    관리번호 VARCHAR(50) NOT NULL,
    변경전 TEXT,
    변경후 TEXT,
    처리일시 DATETIME NOT NULL,
    등록자 VARCHAR(50) NOT NULL
);
