import sys
import hom_inter
import kho_inter

def hybrid_indexer(pd_code: list) -> list: # 给出 pd_code 根据两种不变量推测扭结类型
    namelist_kho = kho_inter.to_knotname(pd_code)
    namelist_hom = hom_inter.to_knotname(pd_code)
    if namelist_kho == [] or namelist_hom == []: # 至少有一方出错了
        err_pos = []
        if namelist_kho == []: # 检查 khovanov 计算是否出错
            err_pos.append("khovanov homology")
        if namelist_hom == []: # 检查 homflypt 计算是否出错
            err_pos.append("homflypt polynomial")
        sys.stderr.write("\033[1;33mWARNING\033[0m: hybrid_indexer: error happend when solving %s" % (" and ".join(err_pos)))
        return namelist_kho + namelist_hom
    return sorted([name for name in namelist_kho if name in namelist_hom])

if __name__ == "__main__":
    print(hybrid_indexer([[1,11,2,10],[2,9,3,10],[3,9,4,8],[4,29,5,30],[5,22,6,23],[7,1,8,30],[15,29,16,28],[16,11,17,12],
                           [18,18,19,17],[20,14,21,13],[21,14,22,15],[23,6,24,7],[24,20,25,19],[25,27,26,26],[27,13,28,12]]))