#!/usr/bin/env python3
"""技术债务自动扫描脚本 - 增强版"""

import subprocess
import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime


def run_pylint(src_dirs):
    """运行pylint并解析结果"""
    if isinstance(src_dirs, str):
        src_dirs = [src_dirs]
    
    all_issues = []
    for src_dir in src_dirs:
        result = subprocess.run(
            ['pylint', '--output-format=json', src_dir],
            capture_output=True, text=True
        )
        if result.stdout:
            try:
                issues = json.loads(result.stdout)
                all_issues.extend(issues)
            except json.JSONDecodeError:
                pass
    return all_issues


def run_flake8(src_dirs):
    """运行flake8（注意：json格式可能有问题，使用默认格式）"""
    if isinstance(src_dirs, str):
        src_dirs = [src_dirs]
    
    all_issues = []
    for src_dir in src_dirs:
        result = subprocess.run(
            ['flake8', src_dir, '--max-line-length=120'],
            capture_output=True, text=True
        )
        # 解析默认格式: file:line:col: code message
        for line in result.stdout.strip().split('\n'):
            if ':' in line:
                parts = line.split(':', 3)
                if len(parts) >= 4:
                    all_issues.append({
                        'file': parts[0],
                        'line': int(parts[1]),
                        'col': int(parts[2]),
                        'message': parts[3].strip()
                    })
    return all_issues


def analyze_complexity(src_dirs):
    """分析代码复杂度"""
    if isinstance(src_dirs, str):
        src_dirs = [src_dirs]
    
    results = {}
    for src_dir in src_dirs:
        result = subprocess.run(
            ['radon', 'cc', src_dir, '-a', '-nc', '-json'],
            capture_output=True, text=True
        )
        if result.stdout:
            try:
                results[src_dir] = json.loads(result.stdout)
            except json.JSONDecodeError:
                # 解析文本输出
                results[src_dir] = parse_radon_text(result.stdout)
    return results


def parse_radon_text(output):
    """解析radon文本输出"""
    issues = []
    for line in output.strip().split('\n'):
        if ' - ' in line and any(grade in line for grade in ['A', 'B', 'C', 'D', 'E', 'F']):
            issues.append(line.strip())
    return issues


def check_dependencies():
    """检查依赖安全（使用scan替代已废弃的check）"""
    # 尝试使用新命令
    result = subprocess.run(
        ['safety', 'scan', '--json'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        # 回退到旧命令
        result = subprocess.run(
            ['safety', 'check', '--json'],
            capture_output=True, text=True
        )
    
    if result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {'raw_output': result.stdout[:1000]}
    return []


def find_duplicate_code(src_dirs):
    """检测重复代码"""
    if isinstance(src_dirs, str):
        src_dirs = [src_dirs]
    
    duplicates = []
    for src_dir in src_dirs:
        result = subprocess.run(
            ['pylint', '--disable=all', '--enable=duplicate-code', src_dir],
            capture_output=True, text=True
        )
        # 解析重复代码报告
        if 'R0801' in result.stdout:
            duplicates.append(result.stdout)
    return duplicates


def generate_summary(pylint_issues, flake8_issues, complexity, security, duplicates):
    """生成摘要统计"""
    # pylint统计
    pylint_by_type = Counter(issue.get('type', 'unknown') for issue in pylint_issues)
    pylint_by_file = Counter(issue.get('path', 'unknown') for issue in pylint_issues)
    
    # 复杂度统计
    complexity_grades = Counter()
    high_complexity_functions = []
    for file_path, file_complexity in complexity.items():
        if isinstance(file_complexity, dict):
            for func, info in file_complexity.items():
                if isinstance(info, dict) and 'complexity' in info:
                    grade = info.get('rank', 'N/A')
                    complexity_grades[grade] += 1
                    if grade in ('D', 'E', 'F'):
                        high_complexity_functions.append({
                            'file': file_path,
                            'function': func,
                            'complexity': info['complexity'],
                            'grade': grade
                        })
    
    return {
        'timestamp': datetime.now().isoformat(),
        'pylint': {
            'total': len(pylint_issues),
            'by_type': dict(pylint_by_type),
            'top_files': dict(pylint_by_file.most_common(10))
        },
        'flake8': {
            'total': len(flake8_issues)
        },
        'complexity': {
            'grades': dict(complexity_grades),
            'high_complexity': high_complexity_functions[:20]
        },
        'security': {
            'vulnerabilities': len(security) if isinstance(security, list) else 'unknown'
        },
        'duplicates': {
            'found': len(duplicates) > 0,
            'count': len(duplicates)
        }
    }


def generate_report(src_dirs, output_file='tech_debt_report.json'):
    """生成完整债务报告"""
    print(f"开始分析: {src_dirs}")
    
    # 1. Pylint分析
    print("  运行pylint...")
    pylint_issues = run_pylint(src_dirs)
    print(f"    发现 {len(pylint_issues)} 个问题")
    
    # 2. Flake8分析
    print("  运行flake8...")
    flake8_issues = run_flake8(src_dirs)
    print(f"    发现 {len(flake8_issues)} 个问题")
    
    # 3. 复杂度分析
    print("  分析复杂度...")
    complexity = analyze_complexity(src_dirs)
    
    # 4. 安全检查
    print("  检查依赖安全...")
    security = check_dependencies()
    
    # 5. 重复代码检测
    print("  检测重复代码...")
    duplicates = find_duplicate_code(src_dirs)
    
    # 6. 生成摘要
    summary = generate_summary(pylint_issues, flake8_issues, complexity, security, duplicates)
    
    # 7. 保存报告
    report = {
        'summary': summary,
        'details': {
            'pylint': pylint_issues[:100],  # 限制数量
            'flake8': flake8_issues[:100],
            'complexity': complexity,
            'security': security if isinstance(security, list) else [],
            'duplicates': duplicates
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n报告已生成: {output_file}")
    print_summary(summary)
    
    return report


def print_summary(summary):
    """打印摘要"""
    print("\n" + "="*60)
    print("技术债务分析摘要")
    print("="*60)
    
    print(f"\nPylint问题: {summary['pylint']['total']}个")
    for issue_type, count in summary['pylint']['by_type'].items():
        print(f"  - {issue_type}: {count}")
    
    print(f"\nFlake8问题: {summary['flake8']['total']}个")
    
    print(f"\n复杂度分析:")
    for grade, count in summary['complexity']['grades'].items():
        print(f"  - {grade}级: {count}个函数")
    
    if summary['complexity']['high_complexity']:
        print(f"\n高复杂度函数 (D/E/F级):")
        for func in summary['complexity']['high_complexity'][:5]:
            print(f"  - {func['file']}:{func['function']} ({func['grade']}级)")
    
    print(f"\n安全漏洞: {summary['security']['vulnerabilities']}个")
    print(f"重复代码: {'发现' if summary['duplicates']['found'] else '未发现'}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python tech_debt_scan.py <目录1> [目录2] ...")
        print("示例: python tech_debt_scan.py src/ app/ lib/")
        sys.exit(1)
    
    src_dirs = sys.argv[1:]
    output_file = 'tech_debt_report.json'
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    generate_report(src_dirs, output_file)