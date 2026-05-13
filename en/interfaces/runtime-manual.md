# Runtime Manual

The Runtime layer has two concrete interface surfaces:

1. the C ABI currently implemented and bound by the JIT
2. runtime handle and error-state management

Do not confuse this with future driver plugin design documents.

## Current C ABI

File: `src/StyioExtern/ExternLib.hpp`

### File I/O

| Function | Purpose |
| --- | --- |
| `styio_file_open` | Opens a file |
| `styio_file_open_auto` | Opens using automatic mode |
| `styio_file_open_write` | Opens in write mode |
| `styio_file_close` | Closes a file |
| `styio_file_rewind` | Rewinds |
| `styio_file_read_line` | Reads line by line |
| `styio_file_write_cstr` | Writes a string |

### String and numeric bridge

| Function | Purpose |
| --- | --- |
| `styio_cstr_to_i64` | `cstr -> i64` |
| `styio_strcat_ab` | Concatenates strings |
| `styio_free_cstr` | Frees Styio-owned strings |
| `styio_i64_dec_cstr` | `i64 -> cstr` |
| `styio_f64_dec_cstr` | `f64 -> cstr` |

### Runtime errors

| Function | Purpose |
| --- | --- |
| `styio_runtime_has_error` | Checks for runtime error |
| `styio_runtime_last_error` | Error message |
| `styio_runtime_last_error_subcode` | Error subcode |
| `styio_runtime_clear_error` | Clears error state |

### Standard streams

| Function | Purpose |
| --- | --- |
| `styio_stderr_write_cstr` | Writes one line to stderr and flushes |
| `styio_stdin_read_line` | Reads one line from stdin |

## Ownership and Lifecycle

`ExternLib.hpp` and `ExternLib.cpp` encode several important rules:

- `styio_file_read_line` returns a thread-local borrowed pointer; do not free it.
- `styio_strcat_ab` returns a heap-allocated string; free it with `styio_free_cstr`.
- `styio_i64_dec_cstr` / `styio_f64_dec_cstr` return borrowed buffers; do not free them.
- `styio_stdin_read_line` returns a thread-local borrowed pointer and returns `nullptr` at EOF.

If codegen disagrees with these rules, the result will be misuse or leaks.

## Handle Table

File: `src/StyioRuntime/HandleTable.hpp`

Key object: `StyioHandleTable`

Main capabilities:

| Method | Purpose |
| --- | --- |
| `acquire(kind, ptr)` | Allocates a handle |
| `lookup(id, kind)` | Looks up a handle |
| `lookup_as<T>(...)` | Strongly typed lookup |
| `release(...)` | Releases one handle |
| `release_all(...)` | Releases handles in bulk |
| `reserve_stub(kind)` | Reserves a handle |
| `invalidate(id)` | Invalidates a handle |

`ExternLib.cpp` currently maintains a thread-local `g_handle_table`.

## Runtime Implementation Details

From `ExternLib.cpp`:

- the handle table is thread-local
- line-read buffers use thread-local alternating buffers
- runtime error state is thread-local
- `styio_stderr_write_cstr` automatically appends a newline and flushes
- `styio_stdin_read_line` strips trailing `\n` / `\r`

## JIT Binding Boundary

File: `src/StyioJIT/StyioJIT_ORC.hpp`

The JIT explicitly registers runtime helpers into `MainJD` during construction. The minimum synchronization scope for a new helper is:

1. `ExternLib.hpp`
2. `ExternLib.cpp`
3. `StyioJIT_ORC.hpp`
4. analyzer / codegen call sites

Miss any step and the JIT will not find the symbol.

## Relationship to Design Documents

`docs/design/Styio-Resource-Driver.md` describes future resource driver interface goals such as:

- `on_subscribe`
- `start_pump`
- `on_receive`
- `on_release`

The runtime interfaces that actually exist and can be depended on today are still:

- `ExternLib.*`
- `HandleTable.hpp`
- `StyioJIT_ORC.hpp`
