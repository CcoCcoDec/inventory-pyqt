import pymysql


DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="1q2w3e4r",
    database="inventory",
    charset="utf8"
)


class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)

    # 로그인 검증
    def verify_user(self, username, password):
        sql = """
            SELECT COUNT(*)
            FROM users
            WHERE username=%s AND password=%s
        """

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username, password))
                count, = cur.fetchone()
                return count == 1

    # 전체 재고 조회
    def fetch_erp(self):
        sql = """
            SELECT 관리번호, 분류, 자재명, 재고수량, 수량단위,
                   재고단가, 단가단위, 업데이트, 등록자
            FROM erp
            ORDER BY 업데이트 DESC
        """

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    # 재고 추가
    def insert_erp(
        self, 관리번호, 분류, 자재명, 재고수량, 수량단위,
        재고단가, 단가단위, 업데이트, 등록자
    ):
        sql = """
            INSERT INTO erp (
                관리번호, 분류, 자재명, 재고수량, 수량단위,
                재고단가, 단가단위, 업데이트, 등록자
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        sql,
                        (
                            관리번호, 분류, 자재명, 재고수량, 수량단위,
                            재고단가, 단가단위, 업데이트, 등록자
                        )
                    )
                conn.commit()
                return True

            except Exception as error:
                conn.rollback()
                print("재고 추가 오류:", error)
                return False

    # 관리번호, 분류, 자재명으로 재고 검색
    def search_erp(self, keyword):
        sql = """
            SELECT 관리번호, 분류, 자재명, 재고수량, 수량단위,
                   재고단가, 단가단위, 업데이트, 등록자
            FROM erp
            WHERE 관리번호 LIKE %s
               OR 분류 LIKE %s
               OR 자재명 LIKE %s
            ORDER BY 업데이트 DESC
        """

        value = f"%{keyword}%"

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (value, value, value))
                return cur.fetchall()

    # 선택한 재고 정보 수정
    def update_erp(
        self, 관리번호, 분류, 자재명, 재고수량, 수량단위,
        재고단가, 단가단위, 업데이트, 등록자
    ):
        sql = """
            UPDATE erp
            SET 분류=%s,
                자재명=%s,
                재고수량=%s,
                수량단위=%s,
                재고단가=%s,
                단가단위=%s,
                업데이트=%s,
                등록자=%s
            WHERE 관리번호=%s
        """

        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        sql,
                        (
                            분류, 자재명, 재고수량, 수량단위,
                            재고단가, 단가단위, 업데이트, 등록자,
                            관리번호
                        )
                    )
                conn.commit()
                return True

            except Exception as error:
                conn.rollback()
                print("재고 수정 오류:", error)
                return False