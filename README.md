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

## 快速开始

### 安装

```bash
# 方式一：直接 URL 安装（推荐）
hermes skills install https://raw.githubusercontent.com/Vincent-crypto-coder/tech-debt-management-skill/main/SKILL.md

# 方式二：添加为 tap 源
hermes skills tap add https://github.com/Vincent-crypto-coder/tech-debt-management-skill
hermes skills install tech-debt-management
```

安装后，在 Hermes 会话中输入 `/reload-skills` 即可加载。

### 一句话启动

```
帮我做一次技术债务分析，针对当前项目目录
```

Hermes 会自动加载本技能，执行扫描 → 分析 → 报告全流程。

### 手动触发

```bash
# 安装分析工具（一次性）
pip install pylint radon safety bandit flake8

# 运行扫描
python references/scan_script.py src/ --output debt_report.json

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
├── SKILL.md                    # 主技能文件（Hermes 读取入口）
├── README.md                   # 本文件
├── references/
│   ├── practical_notes.md      # 实战经验笔记：工具坑点、评估技巧
│   └── scan_script.py          # 增强版一键扫描脚本（多目录、汇总报告）
├── scripts/
│   └── verify_refactor.py      # 重构验证脚本（模块导入+方法存在性检查）
└── templates/
    └── debt_register.md        # 债务登记表模板（Markdown 表格）
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

## 相关项目

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — 开源 AI Agent 框架
- [Hermes Skills 官方目录](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) — 更多可用技能

---

## License

MIT
