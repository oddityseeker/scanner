import socket
import subprocess
import sys
from datetime import datetime
import colorama
import time
import os
from ping3 import ping, verbose_ping

#initializing color output
from colorama import init

init(autoreset=True)
from colorama import Fore, Back, Style

#blank the screen
os.system('cls||clear')

#long strings are stored here
title = "▗▄▄▖  ▗▄▖ ▗▄▄▖▗▄▄▄▖     ▗▄▄▖ ▗▄▄▖ ▗▄▖ ▗▖  ▗▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖ \n▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌ █      ▐▌   ▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▛▚▖▐▌▐▌   ▐▌ ▐▌\n▐▛▀▘ ▐▌ ▐▌▐▛▀▚▖ █       ▝▀▚▖▐▌   ▐▛▀▜▌▐▌ ▝▜▌▐▌ ▝▜▌▐▛▀▀▘▐▛▀▚▖\n▐▌   ▝▚▄▞▘▐▌ ▐▌ █      ▗▄▄▞▘▝▚▄▄▖▐▌ ▐▌▐▌  ▐▌▐▌  ▐▌▐▙▄▄▖▐▌ ▐▌"
TYPESscan = "\n1 all existing ports\n2 common ports\n3 special port\n4 FULL (all existing ports and services)\n5 ping\n99 change target\n00 Exit"

print(Fore.GREEN + title)


def checkport(port):
        """
        Проверяет наличие службы на указанном порту.
        Возвращает имя службы или 0, если служба не обнаружена.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((targetIP, port))

                # Отправка HTTP-запроса
                try:
                    request = "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(targetIP)
                    s.send(request.encode())
                    response = s.recv(1024)
                    if b"HTTP" in response:
                        return "HTTP"
                except:
                    pass

                # Попытка получить SSH баннер
                try:
                    s.send(b"\x00")
                    response = s.recv(1024)
                    if b"SSH" in response:
                        return "SSH"
                except:
                    pass

                # Попытка получить FTP баннер
                try:
                    response = s.recv(1024)
                    if b"FTP" in response:
                        return "FTP"
                except:
                    pass

                # Попытка получить SMTP ответ (220 код)
                try:
                    response = s.recv(1024)
                    if b"220" in response:
                        return "SMTP"
                except:
                    pass

        except Exception:
            return 0  # Нет ответа или порт закрыт

        return 0  # Если ни одна служба не обнаружена


def scanALL():
    for port in range(1, 65535):
        r = checkport(port)
        if r == 0:
            f = 0
            print(port)
        else:
            print(port + " " + r)

def taketype():
    #function for selecting scan type
    while True:
        print(TYPESscan)
        scanTYPE = input("\nEnter scan type: ")
        if scanTYPE == "00":
            sys.exit()
        if scanTYPE == "99":
            taketarget()
        if scanTYPE == "1":
            scanALL()
        if scanTYPE == "3":
            print(checkport(int(input("\nEnter port: "))))
            break
        else:
            print(Fore.RED + "option does not exist")


def taketarget():
    #getting a target
    global targetIP
    targetNAME = input("\nEnter a remote host to scan: ")
    targetIP = socket.gethostbyname(targetNAME)
    print(f"IP: {targetIP}")
    taketype()


taketarget()

startTIME = datetime.now()
