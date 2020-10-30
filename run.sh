cd bot_backend
pkill gunicorn
python3 manage.py migrate
gunicorn bot_backend.wsgi -b :8080 -D

cd ..
pkill python3
nohup python3 bot.py &