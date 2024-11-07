import pwd

def get_system_users():
    """获取系统用户列表"""
    users = []
    for p in pwd.getpwall():
        users.append({
            'name': p.pw_name,
            'uid': p.pw_uid,
            'home': p.pw_dir
        })
    return users