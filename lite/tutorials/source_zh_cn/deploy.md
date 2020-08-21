# 部署

本文档介绍如何在Ubuntu系统上快速安装MindSpore Lite。

<!-- TOC -->

- [部署](#部署)
    - [环境要求](#环境要求)
    - [编译选项](#编译选项)
    - [输出件说明](#输出件说明)
    - [编译示例](#编译示例)

<!-- /TOC -->

<a href="https://gitee.com/mindspore/docs/blob/master/lite/tutorials/source_zh_cn/deploy.md" target="_blank"><img src="../_static/logo_source.png"></a>

## 环境要求

- 编译环境仅支持x86_64版本的Linux：推荐使用Ubuntu 18.04.02LTS

- 编译依赖（基本项）
  - [CMake](https://cmake.org/download/) >= 3.14.1
  - [GCC](https://gcc.gnu.org/releases.html) >= 7.3.0
  - [Python](https://www.python.org/) >= 3.7
  - [Android_NDK r20b](https://dl.google.com/android/repository/android-ndk-r20b-linux-x86_64.zip)
  
  > - 仅在编译ARM版本时需要安装`Android_NDK`，编译x86_64版本可跳过此项。
  > - 如果安装并使用`Android_NDK`，需配置环境变量，命令参考：`export ANDROID_NDK={$NDK_PATH}/android-ndk-r20b`。
                                                                              
- 编译依赖（MindSpore Lite模型转换工具所需附加项，仅编译x86_64版本时需要）
  - [Autoconf](http://ftp.gnu.org/gnu/autoconf/) >= 2.69
  - [Libtool](https://www.gnu.org/software/libtool/) >= 2.4.6
  - [LibreSSL](http://www.libressl.org/) >= 3.1.3
  - [Automake](https://www.gnu.org/software/automake/) >= 1.11.6
  - [Libevent](https://libevent.org) >= 2.0
  - [M4](https://www.gnu.org/software/m4/m4.html) >= 1.4.18
  - [OpenSSL](https://www.openssl.org/) >= 1.1.1 
  
  
## 编译选项

MindSpore Lite提供多种编译方式，用户可根据需要选择不同的编译选项。

| 参数  |  参数说明  | 取值范围 | 是否必选 |
| -------- | ----- | ---- | ---- |
| -d | 设置该参数，则编译Debug版本，否则编译Release版本 | - | 否 |
| -i | 设置该参数，则进行增量编译，否则进行全量编译 | - | 否 |
| -j[n] | 设定编译时所用的线程数，否则默认设定为8线程 | - | 否 |
| -I | 选择适用架构 | arm64、arm32、x86_64 | 是 |
| -e | 在ARM架构下，选择后端算子，设置`gpu`参数，会同时编译框架内置的GPU算子 | gpu | 否 |
| -h | 设置该参数，显示编译帮助信息 | - | 否 |

> 在`-I`参数变动时，即切换适用架构时，无法使用`-i`参数进行增量编译。

## 输出件说明

编译完成后，进入源码的`mindspore/output`目录，可查看编译后生成的文件，命名为`MSLite-{version}-{platform}.tar.gz`。解压后，即可获得编译后的工具包。
   
```bash
tar -xvf MSLite-{version}-{platform}.tar.gz
```

编译后的输出件一般包含以下几种，架构的选择会影响输出件的种类。

| 目录 | 说明 | x86_64 | arm64 | arm32 |
| --- | --- | --- | --- | --- |
| include | 推理框架头文件 | 有 | 有 | 有 |
| lib | 推理框架动态库 | 有 | 有 | 有 |
| benchmark | 基准测试工具 | 有 | 有 | 有 |
| time_profiler | 模型网络层耗时分析工具 | 有 | 有 | 有 |
| converter | 模型转换工具 | 有 | 无 | 无 |
| third_party | 第三方库头文件和库 | 有 | 有 | 有 |

在x86_64、ARM两种架构下，`third party`的内容不同。其中：  
- x86_64：包含`flatbuffers`（FlatBuffers头文件）和`protobuf`（Protobuf头文件与动态库）。
- ARM：包含`flatbuffers`（FlatBuffers头文件）。

> 运行converter、benchmark或time_profiler目录下的工具前，都需配置环境变量，将MindSpore Lite和Protobuf的动态库所在的路径配置到系统搜索动态库的路径中。以0.6.0-beta版本为例：`export LD_LIBRARY_PATH=./MSLite-0.6.0-linux_x86_64/lib:./MSLite-0.6.0-linux_x86_64/third_party/protobuf/lib:${LD_LIBRARY_PATH}`。

## 编译示例

首先，从MindSpore代码仓下载源码。

```bash
git clone https://gitee.com/mindspore/mindspore.git
```

然后，在源码根目录下，执行如下命令，可编译不同版本的MindSpore Lite。

- 编译x86_64架构Debug版本。
    ```bash
    bash build.sh -I x86_64 -d
    ```
   
- 编译x86_64架构Release版本，同时设定线程数。
    ```bash
    bash build.sh -I x86_64 -j32
    ```
      
- 增量编译ARM64架构Release版本，同时设定线程数。
    ```bash
    bash build.sh -I arm64 -i -j32 
    ```
   
- 编译ARM64架构Release版本，同时编译内置的GPU算子。
    ```bash
    bash build.sh -I arm64 -e gpu 
    ```
    
> `build.sh`中会执行`git clone`获取第三方依赖库的代码，请提前确保git的网络设置正确可用。
   
以0.6.0-beta版本为例，x86_64架构Release版本编译完成之后，进入`mindspore/output`目录，执行如下解压缩命令，即可获取输出件`include`、`lib`、`benchmark`、`time_profiler`、`converter`和`third_party`。
   
```bash
tar -xvf MSLite-0.6.0-linux_x86_64.tar.gz
```