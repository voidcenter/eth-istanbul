# coding:utf-8
"""
@author: github.com/chuwt
@time: 2023/11/18
"""

from off_chain.listener import Listener


def run():
    lis = Listener()
    lis.listen()


if __name__ == '__main__':
    run()
