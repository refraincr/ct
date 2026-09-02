from functools import wraps
from typing import Callable

# 测试数据
request = {
    'headers': {
        'Authorization': 'Bearer tooooooken'
    }
}

def login_required():
    def decorator(fn):
        headers = request['headers']
        if not headers:
            raise ValueError('请求没有headers')
        bearer_token = headers['Authorization']
        if not bearer_token:
            raise ValueError('未携带 Bearer <token>')
        if bearer_token.split(' ',1)[-1] != 'ooooooken':
            raise ValueError('无效的 token')
        @wraps(fn)
        def wrapper():
            return fn()
        return wrapper
    return decorator

@login_required()
def posts():
    return {'code':0,'data':{'title': '1','content': '1-99'},'message':'请求成功'},200


def main():
    print(posts())


if __name__ == '__main__':
    main()