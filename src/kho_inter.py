# 桥接：https://github.com/TopologicalKnotIndexer/khovanov-indexer
import os
DIRNOW = os.path.dirname(os.path.abspath(__file__))
SUBDIR = os.path.join(DIRNOW, "khovanov-indexer", "src") # 子包路径


# ======================================== BEGIN IMPORT FROM PATH ======================================== #
import importlib
import json
import sys
def load_module_from_path(path: str, mod_name: str): # 从指定路径导入一个包
    assert os.path.isdir(path)                       # 路径必须存在
    path         = os.path.abspath(path)             # 获得绝对路径
    old_sys_path = json.loads(json.dumps(sys.path))  # 存档旧的 sys.path
    sys.path     = [path] + sys.path                 # 将新的路径加入 sys.path
    mod          = importlib.import_module(mod_name) # 加载指定的包
    sys.path     = old_sys_path                      # 恢复旧的 sys.path
    return mod
# ======================================== END IMPORT FROM PATH ======================================== #

def to_knotname(pd_code: list) -> list:
    return load_module_from_path(SUBDIR, "khovanov_indexer").khovanov_indexer(pd_code)

if __name__ == "__main__": # 测试 K11a1
    print(to_knotname([[4, 2, 5, 1], [10, 6, 11, 5], [8, 3, 9, 4], [2, 9, 3, 10], [16, 12, 17, 11], [14, 7, 15, 8], 
                       [6, 15, 7, 16], [20, 14, 21, 13], [22, 18, 1, 17], [18, 22, 19, 21], [12, 20, 13, 19]]))