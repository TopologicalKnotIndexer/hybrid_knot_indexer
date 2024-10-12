# 用于实现对子进程的计时
import subprocess
import sys
import signal
import time
import os

SRCDIR    = os.path.dirname(os.path.abspath(__file__))
ROOTDIR   = os.path.dirname(SRCDIR)
PYTHONDIR = os.path.join(ROOTDIR, "python3.sh")
assert os.path.isfile(PYTHONDIR)

SLEEP_STEP = 1 # 每 5 秒钟轮询一次进程状态

def kill_process_and_children(pid):
    # 获取所有进程
    try:
        # 获取所有子进程
        children = subprocess.check_output(['pgrep', '-P', str(pid)]).decode().strip().split('\n')
        for child_pid in children:
            kill_process_and_children(int(child_pid))  # 递归杀死子进程
        os.kill(pid, signal.SIGTERM)  # 终止父进程
    except subprocess.CalledProcessError:
        pass
    except Exception as e:
        sys.stderr.write(f"\033[1;33mWARN\033[0m:Error: {e}\n")

def run_subprocess_with_time_limit(cmd: list, time_limit_sec: int) -> int:
    assert isinstance(cmd, list)
    process     = subprocess.Popen(cmd)
    time_begin  = time.time()
    return_code = -1
    time_cost   = 0
    while True:
        time.sleep(SLEEP_STEP)
        if process.poll() is not None:       # 进程已经停止运行
            process.wait()                   # 回收
            return_code = process.returncode # 进程正常得到返回值
            break
        time_cost = time.time() - time_begin # 计算当前用时
        if time_cost > time_limit_sec:       # 超过了限制用时，把进程杀死
            kill_process_and_children(process.pid)
            break
    total_time_cost = time.time() - time_begin
    if return_code < 0:
        sys.stderr.write("\033[1;33mWARN\033[0m: subprocess killed after timeout, total_time_cost = \033[1;32m%.3fs\033[0m.\n" % (total_time_cost))
    else:
        sys.stderr.write("\033[1;34mINFO\033[0m: subprocess return \033[1;32m%d\033[0m, total_time_cost = \033[1;32m%.3fs\033[0m.\n" % (return_code, total_time_cost))
    return return_code

def main():
    time_limit = float(sys.argv[1]) # 获得秒数限制
    other_cmd  = sys.argv[2:]       # 获得命令本身
    assert len(other_cmd) > 0
    ret = run_subprocess_with_time_limit(other_cmd, time_limit)
    if ret < 0:
        exit(255) # -1 相当于是认为程序没有结束就被杀死了
    else:
        exit(ret)

if __name__ == "__main__":
    main()