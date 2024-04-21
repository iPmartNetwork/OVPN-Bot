import os, sqlite3, datetime, pytz

if not os.path.isdir('configs'):
    os.mkdir('configs')

users = [str(i) for i in range(42)]


def init_db():
    exec_db('''CREATE TABLE IF NOT EXISTS users(
            name text PRIMARY KEY NOT NULL,
            register_date text NOT NULL,
            days INT, telegram_id INT)''', commit=True)

def exec_db(cmd, args=None, fetch=False, commit=False):
    db = sqlite3.connect('db.sqlite3')
    c = db.cursor()
    if args:
        data = c.execute(cmd, args)
    else:
        data = c.execute(cmd)
    if commit:
        db.commit()
    if fetch:
        return list(data)
    db.close()
    return True


def get_users() -> list:
    users = exec_db('SELECT name FROM users', fetch=True)
    return [str(user[0]) for user in users]

def add_user(name: str, days=None) -> bool:
    if name in get_users():
        return False
    exec_db('INSERT INTO users(name, register_date, days) VALUES(?, ?, ?)', (name, datetime.datetime.now().astimezone(tz=pytz.timezone('Asia/Tehran')).strftime('%Y/%m/%d %H:%M'), days), commit=True)
    create_config(name)
    users.append(name)
    return True

def revoke(name) -> str:
    if name in get_users():
        exec_db("DELETE FROM users WHERE(name=?)", (name,), commit=True)
        return True
    return False

def create_config(name):
    with open(f'configs/{name}.ovpn', 'w') as f:
        f.write('test openvpn')

def get_config(name):
    if name in get_users():
        if not os.path.exists(f'configs/{name}.ovpn'):
            create_config(name)
        return f'{name}.ovpn'
    return False
