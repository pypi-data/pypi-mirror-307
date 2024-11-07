# coding:utf-8
import time
import threading
from uuid import uuid1
import eventlet

mylist = []


def main():
    pass


class ThreadPool():
    """ 维护一个线程池 """
    
    def __init__(self, size, save_result=False, while_wait_time=0.1, report=False):
        self.size = size
        self.running_thread = []
        self.result_map = {}
        self.exception_map = {}
        self.save_result = save_result
        self.while_wait_time = while_wait_time
        self.report = report

    def run(self, func, args, kwargs={}, time_out=None, thread_id=uuid1()):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """
        if len(self.running_thread) < self.size:
            self.running_thread.append(thread_id)
            t = myThread(func, args=args, kwargs=kwargs, thread_id=thread_id, running_thread=self.running_thread, result_map=self.result_map, save_result=self.save_result, time_out=time_out, exception_map=self.exception_map)
            t.start()
            return thread_id
        else:
            while len(self.running_thread) >= self.size:
                time.sleep(self.while_wait_time)
            return self.run(func, args, kwargs, time_out, thread_id=thread_id)

    def get_results(self):
        return self.result_map
    
    def get_result(self, thread_id):
        return self.result_map[thread_id]
    
    def get_exceptions(self):
        return self.exception_map
    
    def get_exception(self, thread_id):
        return self.exception_map[thread_id]
    
    def clear_result(self):
        self.result_map = {}

    def clear_exception(self):
        self.exception_map = {}

    def wait(self):
        """ 主线程等待，直到线程池不存在活动线程 """
        while len(self.running_thread) > 0:
            time.sleep(self.while_wait_time)
    
    def get_running_num(self):
        return len(self.running_thread)
    
    def get_running_thread(self):
        return self.running_thread


class myThread (threading.Thread):

    def __init__(self, func, args, kwargs, thread_id, running_thread, result_map, save_result, time_out, exception_map):
        threading.Thread.__init__(self)
        threading.Thread.daemon = True
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.thread_id = thread_id
        self.running_thread = running_thread
        self.result_map = result_map
        self.exception_map = exception_map
        self.save_result = save_result
        self.time_out = time_out

    def run(self):
        try:
            if self.time_out is None:
                result = self.func(*self.args, **self.kwargs)
                if self.save_result:
                    self.result_map[self.thread_id] = result
            else:
                # 实测效率很低
                eventlet.monkey_patch()
                with eventlet.Timeout(self.time_out, False):
                    result = self.func(*self.args, **self.kwargs)
                    if self.save_result:
                        self.result_map[self.thread_id] = result
        except Exception as e:
            self.exception_map[self.thread_id] = e
        finally:
            if self.thread_id in self.running_thread:
                self.running_thread.remove(self.thread_id)


if __name__ == '__main__':
    main()
