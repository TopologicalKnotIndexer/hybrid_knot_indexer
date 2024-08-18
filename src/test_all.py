import re
import sys
import os
import che_file_to_knot_name
dirnow = os.path.dirname(os.path.abspath(__file__))

# 本文件仅用于测试
# 不同规则的扭结名称之间遵循着复杂的对应关系
# 以下函数并不能正确实现这一对应，但对于目前的测试集来说，是够用的
def link_knot_name(folder_name: str) -> str:
    assert re.match(r"((m|)K\d+(a|n)\d+(,|))+", folder_name) is not None
    return folder_name

def get_all_file_in_dir(dirpath: str) -> list: # 获取一个文件夹中的所有文件的绝对路径
    ans = []
    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)
        if os.path.isfile(filepath):
            ans.append(filepath)
    return ans

def get_knot_name_from_path(filepath: str) -> str: # 从路径中截取扭结名称
    return os.path.basename(os.path.dirname(filepath))

def list_all_test_file() -> list: # 获取所有测试文件的绝对路径
    che_data_folder = os.path.join(dirnow, "che_data")
    ans = []
    assert os.path.isdir(che_data_folder)
    for file in os.listdir(che_data_folder):
        filepath = os.path.join(che_data_folder, file)
        if os.path.isdir(filepath):
            ans += get_all_file_in_dir(filepath)
    return sorted(ans, key=get_knot_name_from_path)

def main(): # 进行了测试
    for file in list_all_test_file():
        knotname_ans = link_knot_name(get_knot_name_from_path(file))
        knotname_got = che_file_to_knot_name.che_file_to_knot_name(file)
        suc_test     = (knotname_ans in knotname_got) # 成功标志
        print("\033[1;34mINFO\033[0m: testing for knot type (\033[1;33m%-6s\033[0m) ... " % knotname_ans, end="") # 输出测试信息
        print(
            "\033[1;32m[    PASSED]\033[0m" if suc_test else # 输出成功标志
            "\033[1;31m[NOT PASSED]\033[0m"
        )

if __name__ == "__main__":
    main()