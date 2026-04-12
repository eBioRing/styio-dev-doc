# Runtime 手册

Runtime 层包括两块现实接口：

1. 当前已经实现并被 JIT 绑定的 C ABI
2. 运行时句柄与错误状态管理

不要把它和未来的 driver 插件设计文档混为一谈。

## 当前 C ABI

文件：`src/StyioExtern/ExternLib.hpp`

### 文件 I/O

| 函数 | 作用 |
| --- | --- |
| `styio_file_open` | 打开文件 |
| `styio_file_open_auto` | 自动模式打开 |
| `styio_file_open_write` | 以写模式打开 |
| `styio_file_close` | 关闭文件 |
| `styio_file_rewind` | 回卷 |
| `styio_file_read_line` | 逐行读取 |
| `styio_file_write_cstr` | 写字符串 |

### 字符串与数值桥接

| 函数 | 作用 |
| --- | --- |
| `styio_cstr_to_i64` | `cstr -> i64` |
| `styio_strcat_ab` | 拼接字符串 |
| `styio_free_cstr` | 释放 Styio 自有字符串 |
| `styio_i64_dec_cstr` | `i64 -> cstr` |
| `styio_f64_dec_cstr` | `f64 -> cstr` |

### 运行时错误

| 函数 | 作用 |
| --- | --- |
| `styio_runtime_has_error` | 是否存在 runtime error |
| `styio_runtime_last_error` | 错误消息 |
| `styio_runtime_last_error_subcode` | 错误子码 |
| `styio_runtime_clear_error` | 清空错误状态 |

### 标准流

| 函数 | 作用 |
| --- | --- |
| `styio_stderr_write_cstr` | 向 stderr 写一行并 flush |
| `styio_stdin_read_line` | 从 stdin 读一行 |

## 所有权与生命周期

`ExternLib.hpp` 和 `ExternLib.cpp` 里已经写死了几条重要规则：

- `styio_file_read_line` 返回 thread-local 借用指针，不能释放
- `styio_strcat_ab` 返回堆分配字符串，需要 `styio_free_cstr`
- `styio_i64_dec_cstr` / `styio_f64_dec_cstr` 返回借用缓冲，不能释放
- `styio_stdin_read_line` 返回 thread-local 借用指针，遇 EOF 返回 `nullptr`

这类规则如果和 codegen 侧不一致，就会直接产生错用或泄漏。

## 句柄表

文件：`src/StyioRuntime/HandleTable.hpp`

关键对象：`StyioHandleTable`

主要能力：

| 方法 | 作用 |
| --- | --- |
| `acquire(kind, ptr)` | 分配 handle |
| `lookup(id, kind)` | 查找 |
| `lookup_as<T>(...)` | 强类型查找 |
| `release(...)` | 释放单个句柄 |
| `release_all(...)` | 批量释放 |
| `reserve_stub(kind)` | 预留句柄 |
| `invalidate(id)` | 失效化 |

当前 `ExternLib.cpp` 内部就维护了 thread-local `g_handle_table`。

## runtime 内部实现细节

从 `ExternLib.cpp` 能直接确认：

- 句柄表是 thread-local
- 读取行缓冲采用 thread-local 交替 buffer
- runtime error 也是 thread-local 状态
- `styio_stderr_write_cstr` 会自动补换行并 flush
- `styio_stdin_read_line` 会剥离尾部 `\\n` / `\\r`

## JIT 绑定边界

文件：`src/StyioJIT/StyioJIT_ORC.hpp`

JIT 在构造时会把 runtime helper 显式注册到 `MainJD`。因此新增 helper 的最低同步范围是：

1. `ExternLib.hpp`
2. `ExternLib.cpp`
3. `StyioJIT_ORC.hpp`
4. analyzer / codegen 调用点

少一步，JIT 就找不到符号。

## 与设计文档的关系

`docs/design/Styio-Resource-Driver.md` 描述的是未来资源驱动接口目标，比如：

- `on_subscribe`
- `start_pump`
- `on_receive`
- `on_release`

当前主仓库真正已经实现并可依赖的 runtime 接口，仍以：

- `ExternLib.*`
- `HandleTable.hpp`
- `StyioJIT_ORC.hpp`

为准。
