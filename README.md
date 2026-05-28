# Tech Debt Management — Hermes Agent Skill

> 系统化识别、评估、偿还技术债务。把隐性成本显性化，避免项目被债务拖垮。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Hermes Agent](https://img.shields.io/badge/Hermes%20Agent-skill-blue)](https://hermes-agent.nousresearch.com)

## 这个技能是做什么的？

技术债务就像信用卡欠款——快速交付时欠下的债，迟早要还。如果不主动管理，利息（维护成本）会越来越高，最终拖慢整个团队的开发速度。

这个技能是 Hermes Agent 的技能包，它能：

1. **自动扫描** — 用 pylint、radon、safety 等工具分析代码库，找出重复代码、高复杂度函数、安全漏洞
2. **评估优先级** — 通过影响 × 频率 × 风险的矩阵公式，量化每项债务的紧急程度
3. **制定偿还计划** — 按优先级排序，生成具体可执行的重构任务
4. **执行与验证** — 提供重构模式库、验证脚本、进度追踪模板

## 适用场景

- 代码库变得难以修改，加个小功能都要改半天
- 新功能开发速度越来越慢，测试越来越脆弱
- 线上问题频繁，但修复起来牵一发动全身
- 团队知道代码有问题，但不知道从何入手
- 定期技术债务回顾（每季度/每迭代）

---

## 版本要求

### Hermes Agent

| 要求 | 最低版本 | 说明 |
|------|----------|------|
| Hermes Agent | v1.0+ | 支持 `hermes skills install` 命令即可 |
| `hermes skills tap add` | v2.0+ | 方式二（tap 源安装）需要 v2.0+，方式一（URL 直装）无版本限制 |

如果你的 Hermes 版本低于 v2.0，建议先更新：
```bash
hermes update
```

检查当前版本：
```bash
hermes --version
```

### Python

| 要求 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Python | 3.6 | 3.8 ~ 3.12 |

本技能附带的脚本（`scan_script.py`、`verify_refactor.py`）使用标准库，不依赖第三方包。但用到了以下语法：
- `pathlib.Path` — Python 3.4+
- `subprocess.run` — Python 3.5+
- f-string — Python 3.6+

**Hermes 自带 Python 环境，无需额外安装。** 如果你要在 Hermes 之外手动运行脚本，确保你的系统 Python 版本 >= 3.6。

### 分析工具（手动运行时的依赖）

以下工具由 SKILL.md 中的分析命令调用，非脚本强制依赖。如果缺失，对应检查项会跳过并提示：

| 工具 | 用途 | 安装命令 | 兼容版本 | 已知问题 |
|------|------|----------|----------|----------|
| pylint | 代码规范、bug检测、重复代码 | `pip install pylint` | 全部版本 | 无 |
| radon | 圈复杂度分析 | `pip install radon` | 全部版本 | 无 |
| safety | 依赖安全漏洞检查 | `pip install safety` | 全部版本 | `safety check` 已于 2024年6月废弃，本技能已适配新旧命令（自动回退） |
| bandit | 代码安全漏洞扫描 | `pip install bandit` | 全部版本 | 无 |
| flake8 | 代码风格检查 | `pip install flake8` | 全部版本 | `--format=json` 在某些版本输出异常，本脚本使用默认文本格式手动解析 |

一键安装所有工具：
```bash
pip install pylint radon safety bandit flake8
```

---

## 安装说明

### 方式一：直接 URL 安装（推荐，一行搞定）

```bash
hermes skills install https://raw.githubusercontent.com/Vincent-crypto-coder/tech-debt-management-skill/main/SKILL.md
```

安装成功后会显示：
```
✅ Skill 'tech-debt-management' installed successfully
```

**适用版本：** Hermes v1.0+，无版本限制

### 方式二：添加为 tap 源（适合后续更新管理）

```bash
# 首次添加 tap 源
hermes skills tap add https://github.com/Vincent-crypto-coder/tech-debt-management-skill

# 安装技能
hermes skills install tech-debt-management

# 后续更新
hermes skills update
```

**适用版本：** Hermes v2.0+

### 方式三：手动 Git 下载（不需要 Hermes 也能用）

```bash
git clone git@github.com:Vincent-crypto-coder/tech-debt-management-skill.git

# 方式 A：复制到 Hermes skills 目录（推荐）
cp -r tech-debt-management-skill ~/.hermes/skills/software-development/tech-debt-management
# 然后进入 Hermes 会话，输入 /reload-skills 加载

# 方式 B：直接手动使用（Hermes 可选）
cd tech-debt-management-skill
pip install pylint radon safety bandit flake8
python references/scan_script.py /path/to/your/project/
```

### 安装后验证

```bash
# 检查技能是否安装成功
hermes skills list | grep tech-debt-management

# 如果已进入 Hermes 会话，重载技能列表
# 输入：/reload-skills
```

---

## 一句话启动

进入 Hermes 会话后，直接说：

```
帮我做一次技术债务分析，针对当前项目目录
```

Hermes 会自动加载本技能，执行扫描 → 分析 → 报告全流程。

### 手动触发

```bash
# 安装分析工具（一次性）
pip install pylint radon safety bandit flake8

# 运行一键扫描
python references/scan_script.py src/ --output debt_report.json

# 扫描多个目录
python references/scan_script.py qa_engine/ pdf_parser/ app/

# 创建债务登记表
# 参考 templates/debt_register.md 的格式
```

---

## 工作流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  债务识别    │ →  │  分类评估    │ →  │  制定计划    │ →  │  执行偿还    │
│  (静态分析)  │    │  (优先级)    │    │  (任务拆分)   │    │  (重构+验证)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### 阶段一：债务识别

使用行业标准工具自动扫描：

| 检查项 | 工具 | 目的 |
|--------|------|------|
| 代码规范 | pylint | 发现潜在 bug 和风格问题 |
| 复杂度 | radon | 圈复杂度 > 10 的函数需要重构 |
| 重复代码 | pylint duplicate-code | 消除重复，降低维护成本 |
| 安全漏洞 | bandit / safety | 发现已知的安全风险 |
| 依赖健康 | pip-audit | 过时或存在漏洞的依赖 |

### 阶段二：分类评估

每项债务按四个维度打分（1-5分）：

- **发生频率** — 遇到这个问题的频繁程度
- **影响范围** — 影响多少功能或模块
- **修复成本** — 需要多少工作量
- **风险程度** — 不修复的后果严重性

**优先级公式：** `(频率 × 范围 × 风险) / 成本`

### 阶段三：执行偿还

提供多种重构模式：

- **提取方法** — 拆分过长函数
- **提取类** — 拆分 God Class
- **引入参数对象** — 简化过长参数列表

每次重构后自动验证功能正常（`scripts/verify_refactor.py`）。

---

## 目录结构

```
tech-debt-management-skill/
├── SKILL.md                    # 主技能文件（Hermes 读取入口，包含完整工作流）
├── README.md                   # 本文件
├── references/
│   ├── practical_notes.md      # 实战经验笔记：工具坑点、评估技巧、重构陷阱
│   └── scan_script.py          # 增强版一键扫描脚本（多目录、自动汇总、JSON 报告）
├── scripts/
│   └── verify_refactor.py      # 重构验证脚本（模块导入 + 方法存在性检查）
└── templates/
    └── debt_register.md        # 债务登记表模板（Markdown 表格，可直接用）
```

---

## 实际效果

在本项目的实际测试中（一个约 5000 行 Python 的 RAG 系统），一次完整的扫描加偿还：

- 检测出 6 项技术债务（TD-001 ~ TD-006）
- 消除重复代码 3 处 → 重构为公共 util 方法
- 降低 4 个 E 级复杂函数为 C 级
- 清理遗留注释、硬编码版本号等低优先级债务

---

## 为什么选择这个技能？

- **是技能，不是独立工具** — 集成在 Hermes Agent 中，自然融入你的日常开发流程
- **实战验证** — 在真实项目（PDF 智能问答 RAG 系统）中反复打磨过
- **可扩展** — 你可以修改 SKILL.md 中的扫描命令或优先级公式，适配自己的团队
- **小而美** — 只做技术债务管理这一件事，做好

---

## 常见问题

### Q: 需要安装哪些工具？
Hermes 自动执行时，SKILL.md 中的命令会在你系统环境中运行，推荐安装 `pylint radon safety bandit flake8`。如果缺失，对应步骤会跳过，不影响整体流程。

### Q: 支持哪些语言？
本技能主要针对 Python 项目（pylint、radon 等工具），但评估框架和优先级公式适用于任何语言。你可以修改 SKILL.md 中的分析命令来适配其他语言。

### Q: 如何更新到最新版？
```bash
# 如果是 tap 源安装
hermes skills update

# 如果是 URL 直装
hermes skills install https://raw.githubusercontent.com/Vincent-crypto-coder/tech-debt-management-skill/main/SKILL.md --force
```

---

## 相关项目

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — 开源 AI Agent 框架
- [Hermes Skills 官方目录](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) — 更多可用技能

---

## License

MIT
