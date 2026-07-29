import pymysql

DB_CONFIG = dict(
                host = 'localhost',
                user = 'root',
                password = '1q2w3e4r',
                database = 'inventory'
                charset = 'utf8'
                )

# 로그인, erp 관련 테이블과 그 DB 관리용 함수들을 정의한 클래스
class DB:
    def __init__(self, **config): 
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)

    # 로그인 검증
    def verify_user(self, username, password):
        sql = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s" 
        with self.connect() as conn: 
            with conn.cursor() as cur:
                cur.execute(sql, (username, password))
                count, = cur.fetchone()
                return count == 1

    # 재고 정보 란에 띄울 모든 erp 정보들
     def fetch_erp(self):
        sql = "SELECT 관리번호, 분류, 자재명, 재고수량, 수량단위, 재고단가, 단가단위, 업데이트, 등록자 FROM erp ORDER BY id"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    # 재고 조회 창 상단 메뉴 중 재고 추가
    def insert_member(self, 관리번호, 분류, 자재명, 재고수량, 수량단위, 재고단가, 단가단위, 업데이트, 등록자):
        sql = "INSERT INTO erp (관리번호, 분류, 자재명, 재고수량, 수량단위, 재고단가, 단가단위, 업데이트, 등록자) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cut.execute(sql, (관리번호, 분류, 자재명, 재고수량, 수량단위, 재고단가, 단가단위, 업데이트, 등록자))
                    conn.commit()
                    return True

            except Exception:
                conn.rollback()
                return False

    # 재고 조회 창 상단 메뉴 중 재고 조회


    # 재고 조회 창 재고 정보 란 내 칸 눌러서 재고 정보 수정

    
