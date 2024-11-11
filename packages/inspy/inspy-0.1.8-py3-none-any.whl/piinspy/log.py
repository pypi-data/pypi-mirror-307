# -*- encoding: utf-8 -*-
"""
    @File : log.py \n
    @Contact : yafei.wang@pisemi.com \n
    @License: (C)Copyright {} \n
    @Modify Time: 2023/5/24 10:18 \n
    @Author : Pisemi Yafei Wang \n
    @Version: 1.0 \n
    @Description : None \n
    @Create Time: 2023/5/24 10:18 \n
"""

from colorama import Fore, init

init()


def log_print(pLogClass, pLogContent):
    if pLogClass == "DEBUG":
        print(Fore.BLUE + pLogClass + ":", end="")
        print(Fore.RESET + str(pLogContent))
    elif pLogClass == "INFO":
        print(Fore.GREEN + pLogClass + ":", end="")
        print(Fore.RESET + str(pLogContent))
    elif pLogClass == "WARN":
        print(Fore.YELLOW + pLogClass + ":", end="")
        print(Fore.RESET + str(pLogContent))
    elif pLogClass == "ERROR":
        print(Fore.RED + pLogClass + ":", end="")
        print(Fore.RESET + str(pLogContent))
