import os


def run():
    print('[*] Environment variables: ')
    environ = os.environ()
    return str(environ)