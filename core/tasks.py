from celery import shared_task
import time
@shared_task
def do_thing(word):
    for i in range(5):
        print(f'{word}進行中：{i}')
        time.sleep(1)
    return f"{word}ok"