#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess, shlex, threading, json
import requests
import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession


from teleinput.parser import Parser
from teleinput.hw_vendor import RpiDom

TTY_COMMAND='stty -F /dev/ttyAMA0 1200 sane evenp parenb cs7 -crtscts'


def main():

    # Lecture de la conf
    config = ConfigParser.RawConfigParser()
    config.read('/etc/teleinfo/teleinfo.cfg')
    url = config.get('teleinfo_reader', 'notify_url')


    # Configuration du port
    fd=subprocess.Popen(shlex.split(TTY_COMMAND))
    stdout, stderr = fd.communicate()

    with FuturesSession(executor=ThreadPoolExecutor()) as s:

        # Boucle lecture / post
        for frame in Parser(RpiDom()):

            s.post(url, json=frame, timeout=(3.05, 3))


if __name__ == '__main__':
    main()