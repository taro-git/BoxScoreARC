import time
import psycopg
from django.conf import settings

def wait_for_postgres(retries=100, delay=1):
    print("Waiting for PostgreSQL...")

    for attempt in range(1, retries + 1):
        try:
            with psycopg.connect(
                host=settings.DATABASES['default']['HOST'],
                port=int(settings.DATABASES['default']['PORT']),
                dbname=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                connect_timeout=1
            ):
                print("PostgreSQL is ready!")
                return
        except Exception as e:
            print(f"Attempt {attempt}/{retries}: PostgreSQL not available ({e})")
            time.sleep(delay)

    print("PostgreSQL not available after several attempts.")
    raise SystemExit(1)


if __name__ == "__main__":
    import django
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_box_score_arc.settings")
    django.setup()
    wait_for_postgres()
