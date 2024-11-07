#!/usr/bin/env python
# -*- coding: utf-8 -*-

import questionary
from .core.users import get_system_users

def main():
    choices = [
        "1. 查看系统用户列表",
        "2. 安装 Docker (未实现)",
        "3. 添加用户 (未实现)"
    ]
    
    answer = questionary.select(
        "请选择操作:",
        choices=choices
    ).ask()
    
    if answer.startswith("1"):
        users = get_system_users()
        print("\n当前系统用户列表:")
        print("-" * 40)
        for user in users:
            print("用户: {:<15} UID: {:<8} 主目录: {}".format(
                user['name'], 
                user['uid'], 
                user['home']
            ))
        print("-" * 40)

if __name__ == "__main__":
    main()