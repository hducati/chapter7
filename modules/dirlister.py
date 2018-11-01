import os


def run():

    print('[*] In listdir modules: ')
    files = os.listdir()

    return str(files)


if __name__ == '__main__':
    print(run())