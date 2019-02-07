from multiprocessing import Queue, Process
#import communication.CommMod
from communication.CommMod import Commstart, msgValue
def main():
    print("start")
    qout = Queue()
    qin = Queue()
    p = Process(target=Commstart, args=(qin,qout,0))
    p.start()
    print("start 2")
    while True:
        msg = qin.get()
        msgSolver(msg)


def msgSolver(msg):
    if msg.type == 1:
        print('Sensor {} value: {}'.format(msg.name,msg.value))
    elif msg.type == 2:
        print('New device: {}'.format(msg.name))

main()