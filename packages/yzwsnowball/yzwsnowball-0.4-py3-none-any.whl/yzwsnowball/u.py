import os

def get_u():
    if os.environ.get('XUEQIU_Cookie_U') is None:
        raise Exception('没有找到cookies中的U')
    else:
        return os.environ['XUEQIU_Cookie_U']

def set_u(u):
    os.environ['XUEQIU_Cookie_U'] = u
    return os.environ['XUEQIU_Cookie_U']
