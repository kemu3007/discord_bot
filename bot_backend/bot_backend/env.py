import pathlib

import environ

root = environ.Path(__file__) - 2  # リポジトリルートPATH
env = environ.Env()

if pathlib.Path(root(".env")).is_file():
    env.read_env(root(".env"))
else:
    pass