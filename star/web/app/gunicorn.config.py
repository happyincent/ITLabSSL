# bind = '0.0.0.0:8000'
bind = 'unix:/www/star.sock'

workers = 4
worker_class = 'gevent'

accesslog = '-'