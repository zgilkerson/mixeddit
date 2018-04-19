bind = 'unix:gunicorn.socket'
reload = True
accesslog = 'gunicorn.access.log'
errorlog = 'gunicorn.error.log'
capture_output = False
loglevel = 'info'
