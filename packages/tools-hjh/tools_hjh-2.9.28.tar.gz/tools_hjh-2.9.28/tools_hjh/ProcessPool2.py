# coding:utf-8
import time
from multiprocessing import Process, Manager
import sys


def main():
    pass


class ProcessPool():
    """ 维护一个线程池 """
    
    def __init__(self, size, while_wait_time=0.1):
        self.size = size
        self.running_pids = Manager().list()
        self.running_pro = []
        self.while_wait_time = while_wait_time
        
    def run(self, func, args):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """
        if len(self.running_pids) < self.size:
            p = myProcess(func, args=args, running_pids=self.running_pids)
            self.running_pro.append(p)
            p.start()
            self.running_pids.append(p.pid)
            return p.pid
        else:
            while len(self.running_pids) >= self.size:
                time.sleep(self.while_wait_time)
            return self.run(func, args)
        
    def wait(self):
        """ 主线程等待，直到线程池不存在活动线程 """
        for pro in self.running_pro:
            if pro.is_alive():
                pro.join()
    
    def get_running_num(self):
        return len(self.running_pids)
    
    def get_running_process(self):
        return self.running_pids


class myProcess (Process):

    def __init__(self, func, args, running_pids):
        Process.__init__(self)
        # Process.daemon = True
        self.func = func
        self.args = args
        self.running_pids = running_pids

    def run(self):
        try:
            self.func(*self.args)
        except Exception as _:
            pass
        finally:
            if self.pid in self.running_pids:
                self.running_pids.remove(self.pid)
            sys.exit()


if __name__ == '__main__':
    main()
