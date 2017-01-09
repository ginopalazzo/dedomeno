# -*- coding: utf-8 -*-
import random
import os


def loadUserAgents():
    """
    uafile : string
        path to text file of user agents, one per line
    """
    module_dir = os.path.dirname(__file__)  # get current directory
    uafile = os.path.join(module_dir, 'user_agents.txt')
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1: - 1 - 1])
    random.shuffle(uas)
    return uas


def getUserAgent(uas):
    ua = random.choice(uas)  # select a random user agent
    headers = {
        "Connection": "close",  # another way to cover tracks
        "User-Agent": ua
    }
    return headers
