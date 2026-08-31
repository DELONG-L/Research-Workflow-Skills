# Research Workflow Skills

本仓库提供两个用于可复现研究工作的开源 Codex Skill：

- `experiment-design-management`：从实验设计到关闭，形式化并管理完整实验生命周期。
- `research-workspace-governance`：治理本地研究仓库，以及可选的论文仓库和 HPC 扩展。

两个 Skill 可以配合使用，也可以独立安装。工作区治理负责路径与仓库边界；实验管理负责科学记录与生命周期状态。任何一个 Skill 都不会自动授予外部提交、远程修改、受监管研究或破坏性清理的权限。

[English](README.md)

## 使用 Codex 安装

在能够访问 GitHub 的 Codex 对话中粘贴以下请求：

```text
请从下面的 GitHub 仓库安装两个 Codex Skills：

https://github.com/DELONG-L/Research-Workflow-Skills

请从 main 分支安装以下仓库路径：
- experiment-design-management
- research-workspace-governance

不要覆盖已有安装。安装后验证两个 Skill，并告诉我它们将从下一轮对话开始可用。
```

仅提供仓库地址并不代表授权安装；请求中应明确要求 agent 安装指定的 Skill 路径。Codex 的 Skill 安装器在目标目录已存在时会停止，成功下载后会把 Skill 安装到当前配置的 Codex Skill 目录。

## 手动安装

请使用保留规范大小写的仓库地址：

```sh
git clone https://github.com/DELONG-L/Research-Workflow-Skills.git
cd Research-Workflow-Skills
```

将一个或两个 Skill 目录复制到 Codex Skill 目录。请先确认目标不存在，不要覆盖或合并已有安装。

```sh
skill_root="${CODEX_HOME:-$HOME/.codex}/skills"
test ! -e "$skill_root/experiment-design-management"
test ! -e "$skill_root/research-workspace-governance"
mkdir -p "$skill_root"
cp -R experiment-design-management "$skill_root/"
cp -R research-workspace-governance "$skill_root/"
```

只安装一个 Skill 时，只需执行对应的检查和复制命令。如果 Codex 没有立即发现新 Skill，请刷新或重启 Codex。

## 调用

两个 Skill 都支持正常的自动发现，也可以显式调用：

```text
Use $experiment-design-management to turn this approved research question
into a reproducible protocol and analysis plan.

Use $research-workspace-governance to initialize a local-only research
workspace in this repository.
```

开放式研究构想不会自动进入受管理的实验生命周期。普通目录也不会自动变成受管理研究工作区；只有存在有效合约，或用户明确要求初始化或修复时才会进入治理模式。

## 工作区模式

基础合约仅管理本地仓库：

```text
project/
├── PROJECT-WORKSPACE.md
├── experiments/EXP-.../
├── src/
├── configs/
└── scripts/
```

论文仓库是可选的独立 Git 仓库，通过显式链接指向父合约；Overleaf Git 只是受支持的一种选择，并非必需。HPC 同样可选：启用后，本地仓库仍是规范来源，远程目录只是执行镜像。条件字段和示例见 [`project-workspace-contract.md`](research-workspace-governance/references/project-workspace-contract.md)。

## 验证

验证器使用 Python 3 和 PyYAML，检查两个 Skill 包、工作区合约、UI 元数据、内部链接、评测语料、私有路径与密钥形态、单元测试以及 Git 空白问题。如果环境中存在 Codex 自带的 `quick_validate.py`，也会一并运行。

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate_all.py
```

CI 运行同一条仓库级验证命令。

## 版本

- Git 标签表示仓库发布版本，从 `v0.1.0` 开始。
- `contract_version` 表示 `PROJECT-WORKSPACE.md` 合约模式，只在兼容性要求变化时更新。
- 后续如创建托管的不可变 Skill 版本，它属于另一种交付机制，不替代 Git 发布历史。
- `SOURCE_SNAPSHOT.sha256` 记录最初导入时的源文件基线，用于溯源，并不是当前发布树的校验和。

## 卸载

确认准确的安装根目录后，只删除相应的 `experiment-design-management` 和/或 `research-workspace-governance` 目录。卸载 Skill 不会删除它在研究项目中创建的实验或工作区记录。

## 许可证

[MIT](LICENSE)
