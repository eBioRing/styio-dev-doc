# styio-dev-env 用途说明

这页简单说明 `styio-dev-env` 仓库的作用。

`styio-dev-env` 是一个专门用于存放标准开发环境配置文件的静态仓库，不包含复杂的业务逻辑或独立的开发治理规则。

## 仓库用途

它的核心目的是消灭开发环境的不一致性，提供：

- **Toolchain Bootstrap**：用于一键安装编译器（如 LLVM、CMake）及必要依赖的脚本。
- **标准化容器配置**：官方的 `Dockerfile` 和 VS Code `devcontainer.json` 配置文件。
- **CI/CD 环境基座**：为 GitHub Actions 或自建 Runner 提供统一的构建环境镜像配置。

## 使用方式

- 开发者在克隆主代码仓（如 `styio`、`Spio`）时，可以通过运行本仓库提供的初始化脚本来配置本地环境。
- CI 流水线会拉取本仓库中定义的 Docker 镜像作为编译容器。
- 只要环境配置（如 Clang 版本、系统库版本）需要升级，直接修改此仓库的配置文件即可。

## 继续阅读

- [构建工具链](../toolchain/build-toolchain.md)
- [仓库矩阵与来源优先级](repository-matrix.md)
