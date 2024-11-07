# coding:utf-8
from multiprocessing import Pool


def main():
    pass


class ProcessPool():
    """ 维护一个线程池 """
    
    def __init__(self, size):
        self.pool = Pool(processes=size)
        
    def run(self, func, args):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """
        self.pool.map_async(func, args)
        
    def wait(self):
        """ 主线程等待，直到线程池不存在活动线程 """
        self.pool.close()
        self.pool.join()


if __name__ == '__main__':
    main()
