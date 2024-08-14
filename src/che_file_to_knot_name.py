import os
import che_inter
import hybrid_indexer

def che_file_to_knot_name(che_file_path: str) -> list[str]:
    assert os.path.isfile(che_file_path)
    pd_code = che_inter.che_data_to_pd_code(che_file_path)
    return hybrid_indexer.hybrid_indexer(pd_code)

if __name__ == "__main__": # 测试
    dirnow    = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(dirnow, "che_data", "8_10", "data.closed_knot_8_10_L200_sample_1")
    assert os.path.isfile(test_file)
    print(che_file_to_knot_name(test_file))