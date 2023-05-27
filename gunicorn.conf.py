proc_name = 'ApiRest'
daemon = True
loglevel = 'info'
workers = 5
worker_class = 'uvicorn.workers.UvicornWorker'
bind = '0.0.0.0'
port = 8000
