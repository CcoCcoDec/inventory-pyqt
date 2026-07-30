import pymysql
import json

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

        after_data = {
            "관리번호": 관리번호,
            "분류": 분류,
            "자재명": 자재명,
            "재고수량": 재고수량,
            "수량단위": 수량단위,
            "재고단가": 재고단가,
            "단가단위": 단가단위,
            "업데이트": 업데이트,
            "등록자": 등록자
        }

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

                    self.add_history(
                        cur,
                        "추가",
                        관리번호,
                        "",
                        json.dumps(after_data, ensure_ascii=False),
                        등록자
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
        columns = [
            "관리번호", "분류", "자재명", "재고수량", "수량단위",
            "재고단가", "단가단위", "업데이트", "등록자"
        ]

        select_sql = """
            SELECT 관리번호, 분류, 자재명, 재고수량, 수량단위,
                   재고단가, 단가단위, 업데이트, 등록자
            FROM erp
            WHERE 관리번호=%s
        """

        update_sql = """
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

        after_data = {
            "관리번호": 관리번호,
            "분류": 분류,
            "자재명": 자재명,
            "재고수량": 재고수량,
            "수량단위": 수량단위,
            "재고단가": 재고단가,
            "단가단위": 단가단위,
            "업데이트": 업데이트,
            "등록자": 등록자
        }

        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(select_sql, (관리번호,))
                    before_row = cur.fetchone()

                    if before_row is None:
                        return False

                    before_data = dict(zip(columns, before_row))

                    # 관리번호는 수정하지 않으므로 비교 대상에서 제외
                    before_changed = {}
                    after_changed = {}

                    for column in columns[1:]:
                        # DB 숫자형과 입력값 문자열을 같은 기준으로 비교
                        if str(before_data[column]) != str(after_data[column]):
                            before_changed[column] = before_data[column]
                            after_changed[column] = after_data[column]

                    # 실제 수정 사항이 없다면 DB 및 이력에 저장하지 않음
                    if not before_changed:
                        return True

                    cur.execute(
                        update_sql,
                        (
                            분류, 자재명, 재고수량, 수량단위,
                            재고단가, 단가단위, 업데이트, 등록자,
                            관리번호
                        )
                    )

                    # 변경된 컬럼만 이력에 기록
                    self.add_history(
                        cur,
                        "수정",
                        관리번호,
                        json.dumps(
                            before_changed,
                            ensure_ascii=False,
                            default=str
                        ),
                        json.dumps(
                            after_changed,
                            ensure_ascii=False,
                            default=str
                        ),
                        등록자
                    )

                conn.commit()
                return True

            except Exception as error:
                conn.rollback()
                print("재고 수정 오류:", error)
                return False
            
    # 선택한 재고 정보 삭제
    def delete_erp(self, 관리번호):
        select_sql = """
            SELECT 관리번호, 분류, 자재명, 재고수량, 수량단위,
                   재고단가, 단가단위, 업데이트, 등록자
            FROM erp
            WHERE 관리번호=%s
        """

        delete_sql = "DELETE FROM erp WHERE 관리번호=%s"

        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(select_sql, (관리번호,))
                    before_row = cur.fetchone()

                    if before_row is None:
                        return False

                    before_data = dict(zip(
                        [
                            "관리번호", "분류", "자재명", "재고수량", "수량단위",
                            "재고단가", "단가단위", "업데이트", "등록자"
                        ],
                        before_row
                    ))

                    cur.execute(delete_sql, (관리번호,))

                    self.add_history(
                        cur,
                        "삭제",
                        관리번호,
                        json.dumps(before_data, ensure_ascii=False, default=str),
                        "",
                        before_data["등록자"]
                    )

                conn.commit()
                return True

            except Exception as error:
                conn.rollback()
                print("재고 삭제 오류:", error)
                return False

    def add_history(self, cur, 작업구분, 관리번호, 변경전, 변경후, 등록자):
        sql = """
            INSERT INTO erp_history
            (작업구분, 관리번호, 변경전, 변경후, 처리일시, 등록자)
            VALUES (%s, %s, %s, %s, NOW(), %s)
        """

        cur.execute(
            sql,
            (작업구분, 관리번호, 변경전, 변경후, 등록자)
        )

    def get_history(self, 관리번호=None):
        sql = """
            SELECT 이력번호, 작업구분, 관리번호, 변경전, 변경후,
                   처리일시, 등록자
            FROM erp_history
        """

        params = []

        if 관리번호:
            sql += " WHERE 관리번호 LIKE %s"
            params.append(f"%{관리번호}%")

        sql += " ORDER BY 처리일시 DESC"

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()