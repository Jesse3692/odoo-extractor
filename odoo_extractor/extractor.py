#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Odoo Module Code Extractor for AI
用于提取Odoo模块代码并格式化输出，便于AI理解和处理
"""

import argparse
import ast
import hashlib
import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


class OdooModuleExtractor:
    """Odoo模块代码提取器"""

    # 需要提取的文件类型
    INCLUDE_EXTENSIONS = {
        ".py",
        ".xml",
        ".csv",
        ".yml",
        ".yaml",
        ".js",
        ".scss",
        ".css",
        ".html",
        ".txt",
    }

    # 需要排除的目录和文件
    EXCLUDE_PATTERNS = {
        "__pycache__",
        ".git",
        ".idea",
        ".vscode",
        "*.pyc",
        "*.pyo",
        ".DS_Store",
        "node_modules",
        "venv",
        ".venv",
    }

    # 重要文件优先级
    PRIORITY_FILES = {
        "__manifest__.py": 1,
        "__init__.py": 2,
        "models/*.py": 3,
        "views/*.xml": 4,
        "security/*.csv": 5,
        "data/*.xml": 6,
        "wizard/*.py": 7,
        "controllers/*.py": 8,
        "static/src/*.js": 9,
        "reports/*.xml": 10,
    }

    def __init__(self, module_path, output_dir="output"):
        self.module_path = Path(module_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.module_name = self.module_path.name
        self.module_info = {}
        self.file_index = []
        self.total_size = 0

    def extract(self):
        """执行提取流程"""
        print(f"开始提取模块: {self.module_name}")

        # 1. 读取模块元信息
        self._extract_manifest()

        # 2. 生成目录结构
        self._generate_tree_structure()

        # 3. 提取文件内容
        self._extract_files()

        # 4. 生成摘要信息
        self._generate_summary()

        # 5. 创建索引文件
        self._create_index()

        print(f"提取完成！输出目录: {self.output_dir}")

    def _extract_manifest(self):
        """提取__manifest__.py信息"""
        manifest_path = self.module_path / "__manifest__.py"
        if manifest_path.exists():
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # 安全地评估manifest字典
                    self.module_info = ast.literal_eval(content)
            except Exception as e:
                print(f"警告: 无法解析__manifest__.py - {e}")
                self.module_info = {}

    def _generate_tree_structure(self):
        """生成目录树结构"""
        tree_file = self.output_dir / f"{self.module_name}_structure.txt"

        with open(tree_file, "w", encoding="utf-8") as f:
            f.write(f"# {self.module_name} 目录结构\\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

            for item in self._walk_directory(self.module_path):
                level = len(item["path"].relative_to(self.module_path).parts) - 1
                indent = "  " * level

                if item["type"] == "dir":
                    f.write(f"{indent}{item['name']}/\\n")
                else:
                    size_kb = item["size"] / 1024
                    f.write(f"{indent}{item['name']} ({size_kb:.1f}KB)\\n")

    def _walk_directory(self, path, parent_path=None):
        """遍历目录"""
        items = []

        try:
            for item in sorted(path.iterdir()):
                # 检查是否应该排除
                if self._should_exclude(item):
                    continue

                if item.is_dir():
                    items.append({"type": "dir", "name": item.name, "path": item})
                    # 递归处理子目录
                    items.extend(self._walk_directory(item, path))
                else:
                    items.append(
                        {
                            "type": "file",
                            "name": item.name,
                            "path": item,
                            "size": item.stat().st_size,
                        }
                    )

        except PermissionError:
            print(f"警告: 无权限访问 {path}")

        return items

    def _should_exclude(self, path):
        """检查是否应该排除该路径"""
        name = path.name

        # 检查排除模式
        for pattern in self.EXCLUDE_PATTERNS:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True

        # 检查文件扩展名
        if path.is_file():
            if path.suffix not in self.INCLUDE_EXTENSIONS:
                return True

        return False

    def _extract_files(self):
        """提取文件内容"""
        content_file = self.output_dir / f"{self.module_name}_content.txt"

        # 收集所有文件
        all_files = []
        for item in self._walk_directory(self.module_path):
            if item["type"] == "file":
                all_files.append(item)

        # 按优先级排序
        all_files.sort(key=lambda x: self._get_file_priority(x["path"]))

        # 写入内容
        with open(content_file, "w", encoding="utf-8") as f:
            f.write(f"# {self.module_name} 模块代码内容\\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write(f"# 文件总数: {len(all_files)}\\n\\n")

            for file_item in all_files:
                self._write_file_content(f, file_item)

    def _get_file_priority(self, file_path):
        """获取文件优先级"""
        rel_path = file_path.relative_to(self.module_path)
        rel_str = str(rel_path).replace("\\\\", "/")

        # 检查精确匹配
        for pattern, priority in self.PRIORITY_FILES.items():
            if pattern == rel_str:
                return priority

        # 检查模式匹配
        for pattern, priority in self.PRIORITY_FILES.items():
            if "*" in pattern:
                import fnmatch

                if fnmatch.fnmatch(rel_str, pattern):
                    return priority

        return 999  # 默认优先级

    def _write_file_content(self, output_file, file_item):
        """写入单个文件内容"""
        file_path = file_item["path"]
        rel_path = file_path.relative_to(self.module_path)

        # 文件头部信息
        output_file.write("\\n" + "=" * 80 + "\\n")
        output_file.write(f"FILE: {rel_path}\\n")
        output_file.write(f"SIZE: {file_item['size']} bytes\\n")
        output_file.write(f"TYPE: {file_path.suffix}\\n")

        # 特殊处理不同类型的文件
        if file_path.suffix == ".py":
            self._write_python_file(output_file, file_path)
        elif file_path.suffix == ".xml":
            self._write_xml_file(output_file, file_path)
        else:
            self._write_generic_file(output_file, file_path)

        output_file.write("\\n" + "=" * 80 + "\\n")

        # 更新索引
        self.file_index.append(
            {
                "path": str(rel_path),
                "size": file_item["size"],
                "type": file_path.suffix,
                "checksum": self._calculate_checksum(file_path),
            }
        )

        self.total_size += file_item["size"]

    def _write_python_file(self, output_file, file_path):
        """写入Python文件内容（带解析）"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 尝试解析Python文件
            try:
                tree = ast.parse(content)
                classes = [
                    node.name
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ClassDef)
                ]
                functions = [
                    node.name
                    for node in ast.walk(tree)
                    if isinstance(node, ast.FunctionDef)
                ]

                if classes or functions:
                    output_file.write("PARSED_INFO:\\n")
                    if classes:
                        output_file.write(f"  Classes: {', '.join(classes)}\\n")
                    if functions:
                        output_file.write(
                            f"  Functions: {', '.join(functions[:10])}{'...' if len(functions) > 10 else ''}\\n"
                        )
            except Exception:
                pass

            output_file.write("CONTENT:\\n")
            output_file.write(content)

        except Exception as e:
            output_file.write(f"ERROR: 无法读取文件 - {e}\\n")

    def _write_xml_file(self, output_file, file_path):
        """写入XML文件内容（带解析）"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 尝试解析XML结构
            try:
                root = ET.fromstring(content)
                # 提取一些关键信息
                if root.tag == "odoo" or root.tag == "openerp":
                    records = root.findall(".//record")
                    templates = root.findall(".//template")

                    output_file.write("PARSED_INFO:\\n")
                    if records:
                        output_file.write(f"  Records: {len(records)}\\n")
                        # 列出前5个record的id
                        record_ids = [r.get("id", "no-id") for r in records[:5]]
                        output_file.write(
                            f"  Record IDs: {', '.join(record_ids)}{'...' if len(records) > 5 else ''}\\n"
                        )
                    if templates:
                        output_file.write(f"  Templates: {len(templates)}\\n")
            except Exception:
                pass

            output_file.write("CONTENT:\\n")
            output_file.write(content)

        except Exception as e:
            output_file.write(f"ERROR: 无法读取文件 - {e}\\n")

    def _write_generic_file(self, output_file, file_path):
        """写入通用文件内容"""
        try:
            # 尝试以文本方式读取
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            output_file.write("CONTENT:\\n")
            output_file.write(content)
        except Exception:
            # 如果失败，可能是二进制文件
            output_file.write("CONTENT: [Binary file - skipped]\\n")

    def _calculate_checksum(self, file_path):
        """计算文件校验和"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()[:8]
        except Exception:
            return "error"

    def _generate_summary(self):
        """生成摘要信息"""
        summary_file = self.output_dir / f"{self.module_name}_summary.json"

        summary = {
            "module_name": self.module_name,
            "extraction_date": datetime.now().isoformat(),
            "module_info": self.module_info,
            "statistics": {
                "total_files": len(self.file_index),
                "total_size_bytes": self.total_size,
                "total_size_mb": round(self.total_size / 1024 / 1024, 2),
                "file_types": self._count_file_types(),
            },
            "dependencies": self.module_info.get("depends", []),
            "version": self.module_info.get("version", "unknown"),
            "author": self.module_info.get("author", "unknown"),
            "category": self.module_info.get("category", "unknown"),
        }

        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

    def _count_file_types(self):
        """统计文件类型"""
        type_count = {}
        for file in self.file_index:
            ext = file["type"]
            type_count[ext] = type_count.get(ext, 0) + 1
        return type_count

    def _create_index(self):
        """创建文件索引"""
        index_file = self.output_dir / f"{self.module_name}_index.json"

        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "module": self.module_name,
                    "files": self.file_index,
                    "total_files": len(self.file_index),
                    "total_size": self.total_size,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )


def main():
    parser = argparse.ArgumentParser(description="Odoo模块代码提取工具")
    parser.add_argument("module_path", help="Odoo模块路径")
    parser.add_argument("-o", "--output", default="output", help="输出目录")
    parser.add_argument("--split-size", type=int, default=10, help="分割文件大小(MB)")

    args = parser.parse_args()

    # 检查模块路径
    if not os.path.exists(args.module_path):
        print(f"错误: 模块路径不存在 - {args.module_path}")
        sys.exit(1)

    # 执行提取
    extractor = OdooModuleExtractor(args.module_path, args.output)
    extractor.extract()


if __name__ == "__main__":
    main()
