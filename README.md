# hybrid_knot_indexer
根据 Khovanov 同调以及 HOMFLY-PT 多项式，输入扭结空间信息，输出扭结类型名称。



## 前置条件

- 指令集架构为 `x86_64`，使用 `linux` （`tested under linux 6.10.4`）
- 终端中能够使用 `bash`, `java` 以及 `python3` 命令



## 使用方法

在使用扭结类型推测功能前，请先完成程序自检，以检查基础设施是否完善。

### 程序自检

在项目根目录下执行一下代码可以测试功能完整性，测试需要大概十分钟时间：

```bash
bash ./test_all.sh
```

程序将会输出类似如下内容：

```bash
INFO: testing sage                  ... [    PASSED]
INFO: testing python (basic)        ... [    PASSED]
INFO: testing python snappy         ... [NOT PASSED]
INFO: testing for knot type (K6a1 ) ... [    PASSED]
INFO: testing for knot type (K6a2 ) ... [    PASSED]
INFO: testing for knot type (K6a3 ) ... [    PASSED]
INFO: testing for knot type (K7a1 ) ... [    PASSED]
INFO: testing for knot type (K7a2 ) ... [    PASSED]
INFO: testing for knot type (K7a3 ) ... [    PASSED]
INFO: testing for knot type (K7a4 ) ... [    PASSED]
INFO: testing for knot type (K7a5 ) ... [    PASSED]
INFO: testing for knot type (K7a6 ) ... [    PASSED]
INFO: testing for knot type (K7a7 ) ... [    PASSED]
INFO: testing for knot type (K8a1 ) ... [    PASSED]
INFO: testing for knot type (K8a10) ... [    PASSED]
INFO: testing for knot type (K8a2 ) ... [    PASSED]
INFO: testing for knot type (K8a3 ) ... [    PASSED]
INFO: testing for knot type (K8a4 ) ... [    PASSED]
INFO: testing for knot type (K8a5 ) ... [    PASSED]
INFO: testing for knot type (K8a6 ) ... [    PASSED]
INFO: testing for knot type (K8a7 ) ... [    PASSED]
INFO: testing for knot type (K8a8 ) ... [    PASSED]
INFO: testing for knot type (K8a9 ) ... [    PASSED]
```

如果除 testing python snappy 一项外，其余所有项目均为测试通过（即 “PASSED”），说明程序可以正常使用。否则请联系 `premierbob@qq.com` 获得支持。

### 扭结类型推测

在项目根目录下，执行以下代码以实现对扭结类型的预测：

```bash
bash python3.sh ./src/main.py --che <分子坐标信息文件名>
```

程序会将所有可能成为答案的扭结名称输出到标准输出流。例如你可以运行以下命令：

```bash
bash python3.sh ./src/main.py --che "./src/che_data/6_1/data.closed_knot_6_1_L100_sample_1"
```

程序将会输出一行内容：

```
K6a1
```

即为预测出的所有可能扭结类型。



### 项目结构

- che_data_to_pd_code：https://github.com/TopologicalKnotIndexer/che_data_to_pd_code
  - 解析分子信息文件，将其转化为 PD_CODE
- HOMFLY-PT-indexer：https://github.com/TopologicalKnotIndexer/HOMFLY-PT-indexer
  - 根据 HOMFLY-PT 多项式，分析可能的扭结类型
- khovanov-indexer：https://github.com/TopologicalKnotIndexer/khovanov-indexer
  - 根据 khovanov 同调，分析可能的扭结类型

- spatial_coord_to_pd_code：https://github.com/TopologicalKnotIndexer/spatial_coord_to_pd_code
  - 将三维空间数据转化为扭结 PD_CODE（目前版本没有调用这一子项目）

