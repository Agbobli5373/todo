## Todomir
Personal project with todo and scheduling tasks.
Mostly to get productive with house chores and play around with django + htmx.

Uses [uv](https://github.com/astral-sh/uv) for package management and `ruff` in pre-commit.


### Install and run locally.
```shell
$ uv venv
$ source .venv/bin/activate
$ uv pip install -r requirements.txt
$ cd todomir 
$ python manage.py runserver
```

### Compile requirements file
```shell
$ uv pip compile requirements.in -o requirements.txt
```

### Docker
You can run it with docker, please see `docker-compose.yml` file.
