import time

def timestamp_processor(request):
    return {
        'timestamp': int(time.time())
    }