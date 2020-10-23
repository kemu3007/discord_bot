cd bot_backend
gunicorn bot_backend.wsgi -b :8080 -D

cd ..
nohup python3 bot.py &