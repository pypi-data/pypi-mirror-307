from configparser import ConfigParser
import json
from collections import OrderedDict

config_file = "config.ini"

SERVER_IP = None
SERVER_PORT = None
ITS_NUM = None
DATA_DIR = None
certfile = None

def print_config_message(server_ip, server_port, its_num, data_dir, certfile):
    # 각 줄의 최대 길이를 설정합니다.
    width = 45
    separator = '*' * (width + 4)
    empty_line = f"*{' ' * (width + 2)}*"
    
    def format_line(label, value):
        return f"*  {label} = {value}{' ' * (width - len(label) - len(value) - 3)}*"

    message = f"""
{separator}
*{' ' * ((width + 2 - len('[ Config ]')) // 2)}[ Config ]{' ' * ((width + 2 - len('[ Config ]') + 1) // 2)}*
{empty_line}
{format_line('Server info', f'{server_ip}:{server_port}')}
{format_line('ITS_NUM', its_num)}
{format_line('DATA_DIR', data_dir)}
{format_line('certfile', certfile)}
{empty_line}
{separator}
    """
    print(message)

def config_load():
    global SERVER_IP, SERVER_PORT, ITS_NUM, DATA_DIR, certfile

    conf = ConfigParser()
    conf.read(config_file)

    SERVER_IP = conf.get('SERVER', 'IP')
    SERVER_PORT = conf.getint('SERVER', 'PORT')

    certfile = conf.get('CERT', 'certfile')

    ITS_NUM = conf.get('ITS_USER', 'ITS_NUM')
    DATA_DIR = conf.get('ITS_USER', 'DATA_DIR')

    print_config_message(SERVER_IP, SERVER_PORT, ITS_NUM, DATA_DIR, certfile)

if __name__ == '__main__':
    config_load()