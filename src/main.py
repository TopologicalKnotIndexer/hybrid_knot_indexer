import sys
import os
import json
import test_all
import che_file_to_knot_name

def output_usage_list(): # 输出帮助信息
    sys.stderr.write("\033[1;33mUsage\033[0m:\n")
    sys.stderr.write("    python3 main.py --test\n")
    sys.stderr.write("    python3 main.py --che <che_coord_file>\n")

def main(argv_list: list):
    if argv_list == [] or len(argv_list) >= 3 or argv_list == ["--help"]:
        output_usage_list()
        exit(1)
    if argv_list == ["--test"]: # 执行测试程序
        test_all.main()
        exit()
    if len(argv_list) != 2 or argv_list[0] != "--che":
        output_usage_list()
        exit(1)
    # 指定一个文件，分析文件内容扭结类型
    filename = argv_list[1]
    if not os.path.isfile(filename): # 文件不存在
        sys.stderr.write("\033[1;31mERROR\033[0m: %s is not an available file.\n")
        exit(1)
    for knotname in che_file_to_knot_name.che_file_to_knot_name(filename):
        print(knotname)

if __name__ == "__main__":
    argv_list = json.loads(json.dumps(sys.argv[1:]))
    main(argv_list)
