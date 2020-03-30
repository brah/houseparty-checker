import requests
import time
import os
import sys
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread

THREADCOUNT = 10
queue = Queue()
notTaken = []


def Read(filename):
    return [line.strip() for line in open(filename)]


def DoWork(line):
    sesh = requests.Session()
    req = sesh.get('https://houseparty.com/add/%s' % line).text
    print('Checking username {0}'.format(line))
    soup = BeautifulSoup(req, 'html.parser')
    if soup.find(text="Oh no! How did you end up here?"):
        notTaken.append(line)


def Worker(q):
    while True:
        line = q.get()
        DoWork(line)
        time.sleep(0.1)
        q.task_done()


for i in range(THREADCOUNT):
    worker = Thread(target=Worker, args=(queue,))
    worker.setDaemon(True)
    worker.start()


def main():
    if len(sys.argv) < 2:
        try:
            Accounts = Read('Usernames.txt')
        except IOError:
            print('Please use the system args or make a file called Usernames.txt')
            input()
            sys.exit()
    else:
        Accounts = Read(sys.argv[1])

    for Account in Accounts:
        queue.put(Account)

    queue.join()

    for a in notTaken:
        print('The account %s is not taken!' % a)
        with open('Unclaimed.txt', 'w+') as File:
            for i in notTaken:
                File.write(i + '\n')

    print("Saved to Usernames.txt")


if __name__ == '__main__':
    main()
