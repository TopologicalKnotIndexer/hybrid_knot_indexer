import sys
import hom_inter
import kho_inter
import time

# 如果计算 khovanov 同调的时间超过了 TIME_THRESH，则跳过对 homflypt 的计算
# 以防止出现 homflypt 计算时程序崩溃的情况
TIME_THRESH = 40

def merge_name_list(namelist_kho: list, namelist_hom:list) -> list: # 合并名字序列
    if namelist_kho == [] or namelist_hom == []: # 至少有一方出错了
        err_pos = []
        if namelist_kho == []: # 检查 khovanov 计算是否出错
            err_pos.append("khovanov homology")
        if namelist_hom == []: # 检查 homflypt 计算是否出错
            err_pos.append("homflypt polynomial")
        sys.stderr.write("\033[1;33mWARNING\033[0m: hybrid_indexer: error happend when solving %s" % (" and ".join(err_pos)))
        return namelist_kho + namelist_hom
    return sorted([name for name in namelist_kho if name in namelist_hom])

def hybrid_indexer(pd_code: list) -> list: # 给出 pd_code 根据两种不变量推测扭结类型
    time_begin   = time.time()
    namelist_kho = kho_inter.to_knotname(pd_code)
    time_end     = time.time()
    if len(namelist_kho) == 1: # 如果 khovanov 已经能确定具体的扭结类型，就不要再算 HOMFLY-PT 了
        return namelist_kho
    if time_end - time_begin <= TIME_THRESH: # 如果 khovanov 没有超时，则可以计算 homflypt 多项式
        namelist_hom = hom_inter.to_knotname(pd_code)
        return merge_name_list(namelist_kho, namelist_hom)
    else:
        sys.stderr.write("\033[1;33mWARNING\033[0m: hybrid_indexer: homflypt polynomial ignored.")
        return sorted(namelist_kho)

if __name__ == "__main__":
    print(hybrid_indexer([[1,11,2,10],[2,9,3,10],[3,9,4,8],[4,29,5,30],[5,22,6,23],[7,1,8,30],[15,29,16,28],[16,11,17,12],
                           [18,18,19,17],[20,14,21,13],[21,14,22,15],[23,6,24,7],[24,20,25,19],[25,27,26,26],[27,13,28,12]]))