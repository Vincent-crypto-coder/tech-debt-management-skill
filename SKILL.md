---
name: tech-debt-management
description: 系统化识别、评估、偿还技术债务。把隐性成本显性化，避免项目被债务拖垮。
version: 1.0
author: hermes
tags: [refactoring, code-quality, maintenance, best-practices]
trigger:
  - 代码库难以修改或扩展
  - 新功能开发速度明显下降
  - 线上问题频繁但修复困难
  - 团队抱怨代码质量但不知从何入手
  - 定期维护周期（如每个季度）
---

# 技术债务管理技能

## 概述

技术债务是代码中为了快速交付而做的妥协，需要在未来"偿还"。这个技能提供系统化的方法来识别、评估、优先排序和偿还技术债务，避免债务累积拖垮项目。

## 阶段一：债务识别（发现阶段）

### 1.1 代码静态分析

使用工具自动扫描代码质量问题：

```bash
# Python项目
pip install pylint flake8 mypy bandit
pylint --output-format=json src/ > pylint_report.json
flake8 --format=json src/ > flake8_report.json
mypy --ignore-missing-imports src/ > mypy_report.txt
bandit -r src/ -f json -o bandit_report.json

# JavaScript/TypeScript项目
npm install -g eslint jshint
eslint src/ --format json > eslint_report.json
```

### 1.2 复杂度分析

识别高复杂度函数（圈复杂度>10）：

```bash
# Python
pip install radon
radon cc src/ -a -nc  # 显示C级及以上的复杂函数

# 或使用lizard（支持多语言）
pip install lizard
lizard src/ -l python > complexity_report.txt
```

### 1.3 重复代码检测

```bash
# Python
pip install pylint
pylint --disable=all --enable=duplicate-code src/

# 通用工具
npm install -g jscpd
jscpd src/ --min-lines 5 --min-tokens 50
```

### 1.4 依赖健康检查

```bash
# Python
pip install safety pip-audit
safety check  # 检查安全漏洞
pip-audit     # 更全面的审计

# JavaScript
npm audit
npm outdated

# License检查
pip install pip-licenses
pip-licenses --format=csv --with-urls
```

### 1.5 测试覆盖率

```bash
# Python
pip install coverage pytest-cov
pytest --cov=src --cov-report=html

# JavaScript
npm test -- --coverage
```

### 1.6 架构债务识别

手动检查清单：
- [ ] 模块间是否有循环依赖？
- [ ] 是否有God Class（承担过多职责的类）？
- [ ] 数据库查询是否在循环中执行（N+1问题）？
- [ ] 是否有硬编码的配置值？
- [ ] 错误处理是否一致？
- [ ] 日志记录是否充分且有用？

## 债务分类与评估

### 2.1 债务分类表

| 类别 | 示例 | 典型症状 |
|------|------|----------|
| **代码债务** | 重复代码、过长函数、命名不佳 | 难以理解、修改易出错 |
| **架构债务** | 模块耦合、分层混乱 | 牵一发而动全身 |
| **测试债务** | 覆盖率低、测试脆弱 | 不敢重构、回归bug多 |
| **文档债务** | 文档过时、缺失 | 新人上手慢、知识流失 |
| **依赖债务** | 版本过时、安全漏洞 | 安全风险、兼容性问题 |
| **基础设施债务** | 手动部署、监控缺失 | 部署慢、问题发现晚 |

### 2.2 影响评估矩阵

对每个债务项评估四个维度（1-5分）：

1. **发生频率**：遇到这个问题的频繁程度
2. **影响范围**：影响多少功能或模块
3. **修复成本**：需要多少工作量来修复
4. **风险程度**：不修复可能导致的后果严重性

计算优先级分数：`优先级 = (发生频率 × 影响范围 × 风险程度) / 修复成本`

- 高优先级：>= 15
- 中优先级：8-14
- 低优先级：< 8

### 2.3 创建债务登记表

参考 `templates/debt_register.md` 获取标准模板，包含：
- 按优先级分类的债务表格
- 债务类别说明
- 优先级计算公式
- 更新记录格式

```markdown
# 技术债务登记表

## 高优先级（立即处理）
| ID | 描述 | 类别 | 频率 | 范围 | 成本 | 风险 | 优先级 | 状态 |
|----|------|------|------|------|------|------|--------|------|
| TD-001 | 用户认证模块有重复代码 | 代码债务 | 4 | 3 | 2 | 4 | 24 | 待处理 |

## 中优先级（计划处理）
| ID | 描述 | 类别 | 频率 | 范围 | 成本 | 风险 | 优先级 | 状态 |
|----|------|------|------|------|------|------|--------|------|
| TD-002 | 数据库连接池配置硬编码 | 架构债务 | 2 | 4 | 1 | 3 | 24 | 待处理 |

## 低优先级（有机会时处理）
| ID | 描述 | 类别 | 频率 | 范围 | 成本 | 风险 | 优先级 | 状态 |
|----|------|------|------|------|------|------|--------|------|
| TD-003 | 日志格式不统一 | 基础设施债务 | 1 | 2 | 1 | 1 | 2 | 待处理 |
```

## 阶段三：制定偿还计划

### 3.1 偿还策略选择

**策略A：定期偿还（推荐）**
- 每个迭代预留20%时间用于偿还债务
- 优点：持续改进，不影响新功能
- 适用：大多数团队

**策略B：基于风险偿还**
- 优先处理高风险债务（安全漏洞、数据丢失风险）
- 优点：风险可控
- 适用：对稳定性要求高的系统

**策略C：机会主义偿还**
- 修改相关代码时顺便修复附近债务
- 优点：成本低，自然融合
- 适用：债务分散且不紧急

### 3.2 创建偿还任务

```bash
# 将债务项转换为具体的开发任务
# 示例：TD-001 用户认证模块重复代码

## 任务：重构用户认证模块
**关联债务**：TD-001
**预估时间**：4小时
**验收标准**：
1. 提取公共方法到`auth_utils.py`
2. 所有认证相关代码使用公共方法
3. 现有测试全部通过
4. 新增单元测试覆盖公共方法
**步骤**：
1. [ ] 分析现有重复代码的位置和模式
2. [ ] 设计公共接口
3. [ ] 提取公共方法
4. [ ] 逐步替换原有代码
5. [ ] 运行测试验证
6. [ ] 更新相关文档
```

### 3.3 风险评估与缓解

重构前必须考虑：
- **回滚计划**：如果重构出问题，如何快速回滚？
- **测试覆盖**：是否有足够测试保护重构？
- **影响范围**：修改会影响哪些功能？
- **部署策略**：是否需要灰度发布？

## 执行工作流

### 快速开始（行动导向）

用户偏好直接行动，减少理论讲解。按以下步骤快速执行：

```bash
# 1. 安装工具（一次性）
pip install pylint radon safety bandit flake8

# 2. 运行扫描
python scripts/verify_refactor.py src/  # 验证当前状态
radon cc src/ -a -nc                    # 查看高复杂度函数
pylint src/ --output-format=json > pylint_report.json

# 3. 分析结果，创建债务登记表（参考 templates/debt_register.md）

# 4. 按优先级偿还：先重复代码，再复杂度，最后规范问题

# 5. 验证重构
python scripts/verify_refactor.py qa_engine.orchestrator RAGSystem
```

### 执行原则

1. **行动优先**：用户说"行动吧"时，直接开始执行，不需要过多解释
2. **按序执行**：用户说"按顺序处理"时，严格按照优先级顺序偿还债务
3. **小步验证**：每完成一个债务项，立即验证功能正常
4. **保持整洁**：重构后删除临时测试文件，保持项目整洁

## 阶段四：执行与跟踪

### 4.1 重构模式库

**模式1：提取方法（Extract Method）**
```
适用：过长函数、重复代码片段
步骤：
1. 识别可独立的代码块
2. 提取为新方法
3. 用有意义的名称命名
4. 替换原位置调用
验证：原有测试通过，新方法有测试
```

**模式2：提取类（Extract Class）**
```
适用：God Class、职责过多
步骤：
1. 识别类中相关的职责组
2. 创建新类封装这些职责
3. 原类持有新类引用
4. 逐步迁移方法
验证：功能不变，耦合度降低
```

**模式3：引入参数对象（Introduce Parameter Object）**
```
适用：过长参数列表、相关参数组
步骤：
1. 识别相关参数组
2. 创建数据类/结构体
3. 修改方法签名
4. 更新所有调用点
验证：类型安全，调用简化
```

### 4.2 进度跟踪

```markdown
# 技术债务偿还进度

## 本周目标
- [ ] TD-001: 用户认证模块重构（4小时）
- [ ] TD-003: 统一日志格式（2小时）

## 完成情况
| 日期 | 债务ID | 工作内容 | 耗时 | 状态 | 备注 |
|------|--------|----------|------|------|------|
| 2026-05-27 | TD-001 | 提取公共认证方法 | 2h | 进行中 | 已完成分析 |

## 度量指标
- **债务余额**：高优先级3项，中优先级5项，低优先级8项
- **本周偿还**：0项
- **新增债务**：0项
- **偿还速度**：平均每周1.2项
```

### 4.3 预防新债务

**代码审查检查清单**：
- [ ] 是否引入重复代码？
- [ ] 函数是否过长（>30行）？
- [ ] 是否有硬编码值？
- [ ] 错误处理是否完整？
- [ ] 是否有足够测试？
- [ ] 文档是否需要更新？

**设计审查检查清单**：
- [ ] 模块职责是否单一？
- [ ] 依赖方向是否合理？
- [ ] 接口是否稳定？
- [ ] 是否考虑未来扩展？

## 工具集成

### 重构验证脚本

使用 `scripts/verify_refactor.py` 验证重构后功能正常：

```bash
# 验证模块导入和类实例化
python scripts/verify_refactor.py qa_engine.orchestrator RAGSystem

# 验证特定方法存在
python scripts/verify_refactor.py qa_engine.orchestrator RAGSystem _resolve_question,_retrieve_context,_build_response
```

### 自动化扫描脚本

参考 `references/scan_script.py` 获取增强版扫描脚本，支持：
- 多目录并行分析
- 自动解析各种工具输出
- 生成综合摘要报告
- 处理工具版本差异（如flake8 JSON格式问题）

### 快速开始

```bash
# 1. 安装依赖
pip install pylint radon safety bandit flake8

# 2. 运行扫描（单目录）
python references/scan_script.py src/

# 3. 运行扫描（多目录）
python references/scan_script.py qa_engine/ pdf_parser/ app/

# 4. 指定输出文件
python references/scan_script.py src/ --output my_report.json
```

### 实操注意事项

参考 `references/practical_notes.md` 获取：
- 各工具的使用技巧和坑点
- 债务评估维度详解
- 报告模板和CI集成示例
- 实战经验总结

### CI集成示例

```yaml
# .github/workflows/tech-debt-check.yml
name: Technical Debt Check

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  debt-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install pylint radon safety bandit
    
    - name: Run static analysis
      run: |
        pylint src/ --output-format=json > pylint.json || true
        radon cc src/ -a -nc -json > complexity.json
        safety check --json > safety.json || true
        bandit -r src/ -f json -o security.json || true
    
    - name: Generate debt report
      run: |
        python scripts/tech_debt_scan.py src/
    
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: tech-debt-report
        path: tech_debt_report.json
```

## 最佳实践

1. **小步快跑**：每次只处理一个债务项，避免大规模重构
2. **测试先行**：重构前确保有测试保护
3. **持续监控**：定期运行扫描，跟踪债务趋势
4. **团队共识**：定期评审债务优先级，保持团队对齐
5. **记录决策**：为什么选择某个优先级，有什么权衡
6. **立即验证**：重构后立即运行 `scripts/verify_refactor.py` 验证功能
7. **清理临时文件**：测试脚本验证后删除，保持项目整洁

## 常见陷阱

1. **分析瘫痪**：过度分析而不行动
2. **完美主义**：试图一次性解决所有债务
3. **忽视预防**：只偿还旧债，不预防新债
4. **缺乏度量**：没有量化指标，不知道改进效果
5. **孤立行动**：不与业务目标对齐，得不到支持

## 重构执行指南

### 重复代码消除步骤
1. 用pylint检测重复：`pylint --enable=duplicate-code src/`
2. 创建公共utils模块：`module/utils.py`
3. 移入公共函数，各文件改为`from .utils import func`
4. 验证导入无误：写临时测试脚本，运行后删除
5. 更新债务登记表状态

### patch工具使用注意
修改Python文件时，确保old_string精确匹配（包括docstring的三引号），避免引入语法错误。详见`references/practical_notes.md`。

## 验证成功

技术债务管理成功的标志：
- 新功能开发速度稳定或提升
- 生产环境问题减少
- 代码审查时间缩短
- 新人上手时间减少
- 团队满意度提升