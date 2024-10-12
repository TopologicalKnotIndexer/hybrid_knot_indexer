# hybrid_knot_indexer
根据 Khovanov 同调以及 HOMFLY-PT 多项式，输入扭结空间信息，输出扭结类型名称。



## 前置条件

- 指令集架构为 `x86_64`，使用 `linux` （`tested under linux 6.10.4`）
- 终端中能够使用 `bash`, `java`, `g++` 以及 `python3` 命令



## 使用方法

在使用扭结类型推测功能前，请先完成程序自检，以检查基础设施是否完善。

### 程序自检

在项目根目录下执行一下代码可以测试功能完整性，测试需要大概十分钟时间：

```bash
bash ./test_all.sh
```

程序将会输出类似如下内容：

```bash
INFO: erasing original knot-pdcode binary.
INFO: testing sage                   ... [    PASSED]
INFO: testing python (basic)         ... [    PASSED]
INFO: testing python snappy          ... [    PASSED]
INFO: using python3.11 packed in sagemath.
INFO: building knot-pdcode with g++.
INFO: testing for knot type (K0a1  ) ... [    PASSED]
INFO: testing for knot type (K3a1  ) ... [    PASSED]
INFO: testing for knot type (K6a1  ) ... [    PASSED]
INFO: testing for knot type (K6a3  ) ... [    PASSED]
INFO: testing for knot type (K7a1  ) ... [    PASSED]
INFO: testing for knot type (K7a2  ) ... [    PASSED]
INFO: testing for knot type (K7a4  ) ... [    PASSED]
INFO: testing for knot type (K7a7  ) ... [    PASSED]
INFO: testing for knot type (K8a1  ) ... [    PASSED]
INFO: testing for knot type (K8a3  ) ... [    PASSED]
INFO: testing for knot type (K8a4  ) ... [    PASSED]
INFO: testing for knot type (K8a8  ) ... [    PASSED]
INFO: testing for knot type (K8a9  ) ... [    PASSED]
INFO: testing for knot type (mK6a2 ) ... [    PASSED]
INFO: testing for knot type (mK7a3 ) ... [    PASSED]
INFO: testing for knot type (mK7a5 ) ... [    PASSED]
INFO: testing for knot type (mK7a6 ) ... [    PASSED]
INFO: testing for knot type (mK8a10) ... [    PASSED]
INFO: testing for knot type (mK8a2 ) ... [    PASSED]
INFO: testing for knot type (mK8a5 ) ... [    PASSED]
INFO: testing for knot type (mK8a6 ) ... [    PASSED]
INFO: testing for knot type (mK8a7 ) ... [    PASSED]
```

如果除 testing python snappy 一项外，其余所有项目均为测试通过（即 “PASSED”），说明程序可以正常使用。否则请联系 `premierbob@qq.com` 获得支持。

### 扭结类型推测

在项目根目录下，执行以下代码以实现对扭结类型的预测：

```bash
bash python3.sh ./src/main.py --che <分子坐标信息文件名>
```

程序会将所有可能成为答案的扭结名称输出到标准输出流。例如你可以运行以下命令：

```bash
bash python3.sh ./src/main.py --che "./src/che_data/K6a1/data.closed_knot_6_1_L100_sample_1"
```

程序将会输出一行内容：

```
K6a1
```

即为预测出的所有可能扭结类型。

### 计时服务

有时当扭结结构比较复杂时，程序可能出现无法终止的情况，本项目并不默认提供超时终止机制。若想要使用超时终止机制请使用下述命令：

```bash
bash python3.sh ./src/timer_process.py <超时秒数> bash python3.sh ./src/main.py --che <分子坐标信息文件名>
```

例如你可以通过下述方式设置一个 20 分钟超时的扭结类型预测：

```bash
bash python3.sh ./src/timer_process.py 1200 bash python3.sh ./src/main.py --che "./src/che_data/K6a1/data.closed_knot_6_1_L100_sample_1"
```

如果程序按时结束，计时程序会向标准错误流输出类似如下的信息：

```bash
INFO: subprocess return 0, total_time_cost = 5.002s.
```

否则，计时程序会向标准错误流输出类似如下的信息：

```bash
WARN: subprocess killed after timeout, total_time_cost = 1200.031s.
```



## 项目结构

- che_data_to_pd_code：https://github.com/TopologicalKnotIndexer/che_data_to_pd_code
  - 解析分子信息文件，将其转化为 PD_CODE
- HOMFLY-PT-indexer：https://github.com/TopologicalKnotIndexer/HOMFLY-PT-indexer
  - 根据 HOMFLY-PT 多项式，分析可能的扭结类型
- khovanov-indexer：https://github.com/TopologicalKnotIndexer/khovanov-indexer
  - 根据 khovanov 同调，分析可能的扭结类型

- spatial_coord_to_pd_code：https://github.com/TopologicalKnotIndexer/spatial_coord_to_pd_code
  - 将三维空间数据转化为扭结 PD_CODE（目前版本没有调用这一子项目）

