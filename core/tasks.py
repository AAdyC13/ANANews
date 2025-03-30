from celery import shared_task


@shared_task
def test(word):
    import time
    import channels.layers
    from asgiref.sync import async_to_sync
    channel_layer = channels.layers.get_channel_layer()
    
    for i in range(5):
        message = f'{word}進行中：{i}'
        async_to_sync(channel_layer.group_send)(
            "celery_logs", {"type": "log_message", "message": message}
        )
        time.sleep(1)
    return f"test_task complete"
