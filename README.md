# Tech Debt Management - Hermes Agent Skill

系统化识别、评估、偿还技术债务。把隐性成本显性化，避免项目被债务拖垮。

## 安装

```bash
# 方式一：直接安装（推荐）
hermes skills install https://raw.githubusercontent.com/Vincent-crypto-coder/tech-debt-management-skill/main/SKILL.md

# 方式二：添加为 tap 源
hermes skills tap add https://github.com/Vincent-crypto-coder/tech-debt-management-skill
hermes skills install tech-debt-management

# 方式三：手动下载
# git clone git@github.com:Vincent-crypto-coder/tech-debt-management-skill.git
# cp -r tech-debt-management-skill ~/.hermes/skills/software-development/tech-debt-management
```

## 用法

技能会自动在以下场景触发：
- 代码库难以修改或扩展
- 新功能开发速度明显下降
- 线上问题频繁但修复困难
- 团队抱怨代码质量但不知从何入手
- 定期维护周期（如每个季度）

## 目录结构

```
tech-debt-management-skill/
├── SKILL.md              # 主技能文件
├── references/
│   ├── practical_notes.md   # 实战经验笔记
│   └── scan_script.py       # 增强版扫描脚本
├── scripts/
│   └── verify_refactor.py   # 重构验证脚本
└── templates/
    └── debt_register.md     # 债务登记表模板
```
