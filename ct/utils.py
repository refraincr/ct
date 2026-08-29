import bcrypt

def generate_password_hash(password: str) -> str:
    password_byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_byte_hash = bcrypt.hashpw(password_byte,salt)
    return password_byte_hash.decode('utf-8')

def check_password(password: str,saved_password: str) -> bool:
    """ 前面的输入的密码，后面的是保存的密码 """
    return bcrypt.checkpw(password.encode('utf-8'),saved_password.encode('utf-8'))

if __name__ == '__main__':
    s = generate_password_hash('zxc123234')
    p = 'zxc123234'
    print(f's == p[{s == p}]')
    print(f'valid: {check_password(p,s)}')
