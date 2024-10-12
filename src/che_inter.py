# 桥接：https://github.com/TopologicalKnotIndexer/che_data_to_pd_code
import os
DIRNOW = os.path.dirname(os.path.abspath(__file__))
SUBDIR = os.path.join(DIRNOW, "che_data_to_pd_code", "src") # 子包路径

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

from mytimer import timer_wrap_gen

@timer_wrap_gen("che_inter")
def che_data_to_pd_code(che_data_file_path: str) -> list:
    assert os.path.isfile(che_data_file_path)
    ans = load_module_from_path(SUBDIR, "che_data_to_pd_code").che_data_to_pd_code(che_data_file_path)
    return ans

if __name__ == "__main__":
    test_file = os.path.join(DIRNOW, "che_data", "6_1", "data.closed_knot_6_1_L100_sample_1")
    assert os.path.isfile(test_file)
    print(che_data_to_pd_code(test_file))