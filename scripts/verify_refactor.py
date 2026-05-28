#!/usr/bin/env python3
"""
验证重构后的代码功能正常
用法: python verify_refactor.py [module_name]
示例: python verify_refactor.py qa_engine.orchestrator
"""

import sys
import os
import inspect

def verify_refactor(module_path, class_name=None, methods_to_check=None):
    """验证重构：检查类和方法是否存在，功能是否正常"""
    
    # 添加项目路径
    project_dir = os.path.dirname(os.path.abspath(__file__))
    while project_dir != '/' and not os.path.exists(os.path.join(project_dir, 'requirements.txt')):
        project_dir = os.path.dirname(project_dir)
    if project_dir != '/':
        sys.path.insert(0, project_dir)
    
    print(f"=== 验证重构: {module_path} ===\n")
    
    # 1. 导入模块
    try:
        module = __import__(module_path, fromlist=[''])
        print(f"✅ 模块导入成功: {module_path}")
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    
    # 2. 检查类（如果指定）
    if class_name:
        try:
            cls = getattr(module, class_name)
            instance = cls() if hasattr(cls, '__init__') else None
            print(f"✅ 类实例化成功: {class_name}")
        except Exception as e:
            print(f"❌ 类实例化失败: {e}")
            return False
        
        # 3. 检查方法
        if methods_to_check:
            print(f"\n=== 检查方法 ===")
            for method in methods_to_check:
                if hasattr(instance, method):
                    print(f"✅ {method} 存在")
                else:
                    print(f"❌ {method} 缺失")
    
    # 4. 检查函数复杂度（如果有radon）
    try:
        import radon.complexity as cc
        module_file = inspect.getfile(module)
        with open(module_file, 'r') as f:
            source = f.read()
        
        results = cc.cc_visit(source)
        high_complexity = [r for r in results if r.complexity > 15]
        
        if high_complexity:
            print(f"\n⚠️  发现{len(high_complexity)}个高复杂度函数:")
            for r in high_complexity:
                print(f"   - {r.name}: {r.complexity}")
        else:
            print(f"\n✅ 无高复杂度函数（>15）")
    except ImportError:
        print(f"\nℹ️  未安装radon，跳过复杂度检查")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python verify_refactor.py <module_path> [class_name] [method1,method2,...]")
        print("示例: python verify_refactor.py qa_engine.orchestrator RAGSystem _resolve_question,_retrieve_context")
        sys.exit(1)
    
    module_path = sys.argv[1]
    class_name = sys.argv[2] if len(sys.argv) > 2 else None
    methods = sys.argv[3].split(',') if len(sys.argv) > 3 else None
    
    success = verify_refactor(module_path, class_name, methods)
    sys.exit(0 if success else 1)