from psutil import process_iter
from signal import SIGTERM

for proc in process_iter():
    if proc.name() == 'gunicorn' or proc.name() == 'python' :
        proc.send_signal(SIGTERM)