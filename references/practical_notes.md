# 技术债务分析实操笔记

## 工具使用注意事项

### pylint
- 输出格式：`--output-format=json` 生成JSON数组
- 每个问题包含：type, module, obj, line, column, path, symbol, message, message-id
- 问题类型：convention(规范), warning(警告), refactor(重构建议), error(错误)
- 常见误报：unused-import (可能动态使用), too-many-arguments (复杂但必要)

### flake8
- **JSON格式问题**：某些版本的flake8 `--format=json` 输出不是有效JSON
- 推荐使用默认格式，手动解析：`file:line:col: code message`
- 常见问题：E501(行过长), W291(尾随空白), E302(缺少空行)

### radon (复杂度分析)
- 输出格式：`-json` 生成嵌套字典
- 复杂度等级：A(1-5), B(6-10), C(11-15), D(16-20), E(21-25), F(26+)
- 命令：`radon cc src/ -a -nc` 显示C级及以上
- 文本输出解析：查找包含 ` - [A-F]` 的行

### safety (安全检查)
- **已废弃命令**：`safety check` 将于2024年6月后不再支持
- **新命令**：`safety scan` (功能更强)
- 输出格式：`--json` 生成漏洞列表
- 注意：检查的是整个Python环境，不仅是项目依赖

### 重复代码检测
- pylint: `--enable=duplicate-code` 检测重复
- jscpd: 通用工具，支持多语言 `jscpd src/ --min-lines 5`

## 债务评估维度

### 频率 (1-5分)
1: 几乎不遇到
2: 偶尔遇到
3: 每周几次
4: 每天遇到
5: 频繁阻碍开发

### 范围 (1-5分)
1: 单个函数
2: 单个文件
3: 单个模块
4: 多个模块
5: 整个项目

### 成本 (1-5分)
1: 30分钟内
2: 2小时内
3: 半天
4: 1-2天
5: 超过2天

### 风险 (1-5分)
1: 仅代码风格
2: 可维护性下降
3: 功能扩展困难
4: 可能导致bug
5: 安全漏洞/数据丢失

## 优先级计算

```
优先级 = (频率 × 范围 × 风险) / 成本
```

阈值建议：
- 高优先级：>= 15
- 中优先级：8-14
- 低优先级：< 8

## 报告模板

### 债务登记表字段
- ID: TD-XXX (唯一标识)
- 描述: 具体问题描述
- 类别: 代码债务/架构债务/测试债务/文档债务/依赖债务/基础设施债务
- 频率: 1-5
- 范围: 1-5
- 成本: 1-5
- 风险: 1-5
- 优先级: 计算值
- 状态: 待处理/进行中/已完成

### 分析报告章节
1. 执行摘要
2. 发现的主要问题
3. 债务分类与评估
4. 偿还计划建议
5. 风险缓解
6. 成功指标
7. 工具配置建议

## CI集成示例

```yaml
# .github/workflows/tech-debt.yml
name: Technical Debt Check

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  analysis:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install tools
      run: pip install pylint radon safety bandit
    
    - name: Run analysis
      run: |
        pylint src/ --output-format=json > pylint.json || true
        radon cc src/ -a -nc -json > complexity.json
        safety scan --json > safety.json || true
    
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: tech-debt-report
        path: *.json
```

## 实战经验

### 工单7分析经验
- 项目：PDF问答RAG系统
- 主要模块：qa_engine, pdf_parser, app
- 发现：4个E级复杂度函数，2个F级复杂度函数
- 建议：优先重构核心业务逻辑（RAGSystem.ask等）

### 工单7执行经验（TD-004消除重复代码）
- 问题：`detect_language`函数在generator.py, retriever.py, query_understanding.py中重复
- 方案：创建`qa_engine/utils.py`，3个文件改为`from .utils import detect_language`
- 结果：重复代码从3份变1份，后续修改只需改一处
- 耗时：约10分钟（含测试验证）
- 注意：修改后需清理测试文件（test_utils.py），保持项目整洁

### 工单7执行经验（TD-002重构E级复杂度函数）
- 问题：4个E级复杂度函数，主要问题是嵌套过深、职责过多
- 重构策略：
  1. **RAGSystem.ask** (200行)：提取为6个辅助方法
     - `_resolve_question()` - 指代消解
     - `_retrieve_context()` - 文本检索
     - `_retrieve_images()` - 图像检索
     - `_try_multimodal()` - 多模态生成
     - `_fallback_text()` - 文字降级
     - `_build_response()` - 结果组装
  2. **_load_file_internal** (174行)：提取4个公共方法
     - `_try_load_from_cache()` - 缓存加载
     - `_process_images()` - 图像处理
     - `_vectorize_chunks()` - 向量化
     - `_build_fulltext_index()` - 全文索引
  3. **_load_pdf_internal** (171行)：使用相同公共方法
  4. **Retriever._detect_table_type** (25行)：重构为策略模式
- 结果：
  - ask函数从200行降为50行主函数
  - 消除了大量重复代码
  - 复杂度从E级降为C级以下
  - 代码可读性大幅提升
- 耗时：约30分钟（含测试验证）
- 验证：运行测试脚本确认功能不变
- 关键点：
  1. 保持函数签名和返回值不变
  2. 提取的方法要有明确的职责
  3. 使用策略模式简化条件判断
  4. 重构后立即验证功能

## 重构执行陷阱

### Python docstring patch陷阱
用patch工具修改Python文件时，如果old_string包含模块顶部的docstring（`"""..."""`），容易引入语法错误：
- 错误示例：patch后出现`""""""`（双docstring开头）
- 原因：old_string没有精确匹配docstring的开头`"""`
- 解决：patch时检查old_string是否完整包含第一行docstring的`"""`，避免重复

### 重构顺序建议
1. 先消除重复代码（成本最低，风险最小）
2. 再处理复杂度重构（需要更多时间，改动更大）
3. 最后处理代码规范问题（pylint警告等）

### utils.py模式
当多个模块有相同工具函数时：
1. 创建`module/utils.py`
2. 将公共函数移入
3. 各模块改为`from .utils import func_name`
4. 保持`__init__.py`不变（不需要导出utils）

### 常见模式
1. **God Class反模式**：单个类承担过多职责
   - 症状：文件>500行，方法>20个
   - 修复：按职责拆分为多个类

2. **长方法反模式**：函数过长
   - 症状：>50行，复杂度C级以上
   - 修复：提取子方法，单一职责

3. **重复代码**：相同逻辑多处出现
   - 症状：pylint R0801警告
   - 修复：提取公共函数/类

4. **魔法数字**：硬编码数字
   - 症状：代码中直接使用数字
   - 修复：定义常量，添加注释

---
*更新时间：2026-05-27*