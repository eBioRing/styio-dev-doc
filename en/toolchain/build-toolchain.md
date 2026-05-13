# 构建工具链

这页只记录维护 `styio` 本体真正需要的工具链契约。

如果你在维护 `Spio` 或 `Vityo`，先跳到它们各自的开发指引，不要把本页当成通用生态工具链说明。

## 核心依赖

根据 `CMakeLists.txt` 和 `THIRD-PARTY.md`，当前主依赖如下：

| 依赖 | 版本 / 形式 | 用途 |
| --- | --- | --- |
| CMake | `>= 3.14` | 构建系统 |
| C++ 编译器 | `C++20` | 编译主工程 |
| LLVM | `18.1.0+` | IR、ORC JIT、本机目标 |
| Python 3 | `find_package(Python3)` | `styio-nano` profile 生成 |
| ICU | 可选 | Unicode 与 CLI Unicode 支持 |
| GoogleTest | `FetchContent` | C++ 测试 |
| cxxopts | vendored 单头文件 | CLI 解析 |

## 关键 CMake 开关

当前远端 `main` 已公开这些高频开关：

| 开关 | 默认值 | 作用 |
| --- | --- | --- |
| `STYIO_USE_ICU` | `OFF` | 打开 ICU-backed Unicode |
| `STYIO_BUILD_NANO` | `ON` | 同时构建 `styio-nano` |
| `STYIO_NANO_OPTIMIZE_FOR_SIZE` | `ON` | 对 `styio-nano` 使用 size-oriented 优化 |
| `STYIO_NANO_PROFILE` | `configs/styio-nano-default.toml` | 指定 `styio-nano` profile |

## 构建命令

标准构建：

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j
```

启用 ICU：

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DSTYIO_USE_ICU=ON
cmake --build build -j
```

关闭 `styio-nano`：

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DSTYIO_BUILD_NANO=OFF
cmake --build build -j
```

自定义 `styio-nano` profile：

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug \
  -DSTYIO_NANO_PROFILE=$PWD/configs/styio-nano-default.toml
cmake --build build -j
```

## 主要产物

- `build/bin/styio`
- `build/bin/styio-nano`
- `build/bin/styio_test`
- `build/bin/styio_security_test`
- `build/bin/styio_soak_test`

## 当前工具链注意事项

`AGENT-SPEC.md` 明确提到过几类风险：

- 源文件列表不是自动发现的
- 新增 `.cpp` 要手动进 `CMakeLists.txt`
- `styio-nano` profile 是 configure 阶段生成物，缺 Python 3 会直接卡住
- 某些机器上 GoogleTest 构建可能受 LLVM / 标准库头冲突影响
- `tests/CMakeLists.txt` 现在还包含 `docs_audit`，文档树也算正式测试面的一部分

因此维护优先级通常是：

1. 确保 `styio` 本体能构建
2. 确保关键 `ctest` 标签能跑
3. 再处理平台特定的额外测试问题

## 依赖变更的正确顺序

如果你要改外部依赖：

1. 先改 `CMakeLists.txt` 或 `tests/CMakeLists.txt`
2. 同步 `docs/specs/THIRD-PARTY.md`
3. 再把本手册的对应页面同步过来
