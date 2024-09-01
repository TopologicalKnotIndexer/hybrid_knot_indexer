import time
import sys
GLOBAL_TIMER_ON_DEFAULT = False # 计时器回显开关

class MyTimer:
    def __init__(self, timer_name: str) -> None:
        self.timer_name = timer_name
        self.begin_time = time.time()
        self.timer_on   = GLOBAL_TIMER_ON_DEFAULT

    def toggle(self):
        self.timer_on = not self.timer_on

    def timer_show(self) -> float: # 输出已用时间到 stderr
        time_cost = time.time() - self.begin_time
        if self.timer_on:
            sys.stderr.write("\033[1;32mTIMER\033[0m: timer \033[1;33m%15s\033[0m time_cost: %14.3fs.\n" % (self.timer_name, time_cost))
        return time_cost
    
def timer_wrap(function, function_name): # 修饰器
    def wraped_function(*args, **kargs):
        timer = MyTimer(str(function_name))
        ans = function(*args, **kargs)
        timer.timer_show()
        return ans
    return wraped_function

def timer_wrap_gen(function_name): # 柯里化
    def wrap(function):
        return timer_wrap(function, function_name)
    return wrap