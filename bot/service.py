from django.db import connection


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def get_facultet():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM bot_facultet
            
        """)
        data = dictfetchall(cursor)
    return data