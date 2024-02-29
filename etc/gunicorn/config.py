bind = "unix:/tmp/gunicorn.sock"
workers = 4
wsgi_app = "todomir.wsgi"
secure_scheme_headers = {
    "X-FORWARDED-PROTOCOL": "https",
    "X-FORWARDED-PROTO": "https",
    "X-FORWARDED-SSL": "on",
}
