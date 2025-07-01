# Odoo Module Extractor

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)

Odoo Module Extractor 是一个用于提取和分析 Odoo 模块代码的工具。它可以帮助开发者和 AI 研究人员更好地理解和分析 Odoo 模块的结构和内容。

## 特性

- 📁 自动提取模块结构和文件内容
- 🔍 智能解析 Python 和 XML 文件
- 📊 生成详细的模块摘要和统计信息
- 🗂 创建文件索引和校验和
- 🎯 支持自定义输出目录
- 🔄 按优先级排序文件处理
- 📝 生成标准化的输出格式

## 安装

### 使用 pip 安装

```bash
pip install odoo-extractor
```

### 从源码安装

```bash
git clone https://github.com/yourusername/odoo-extractor.git
cd odoo-extractor
pip install -e .
```

## 使用方法

### 命令行使用

基本用法：
```bash
odoo-extract /path/to/odoo/module -o output_directory
```

参数说明：
- `module_path`: Odoo 模块的路径（必需）
- `-o, --output`: 输出目录（可选，默认为 'output'）
- `--split-size`: 大文件分割大小（MB）（可选，默认为 10MB）

### Python API 使用

```python
from odoo_extractor import OdooModuleExtractor

# 创建提取器实例
extractor = OdooModuleExtractor(
    module_path='/path/to/odoo/module',
    output_dir='output'
)

# 执行提取
extractor.extract()
```

## 输出文件说明

工具会在输出目录生成以下文件：

1. `{module_name}_structure.txt`: 模块目录结构
   ```
   # example_module 目录结构
   # 生成时间: 2025-07-01 10:21:33
   
   __init__.py (0.1KB)
   __manifest__.py (2.3KB)
   models/
     __init__.py (0.1KB)
     example.py (15.2KB)
   views/
     example_views.xml (8.4KB)
   ```

2. `{module_name}_content.txt`: 文件内容
   - 包含所有源代码文件的内容
   - 智能解析 Python 类和函数
   - XML 文件的结构分析

3. `{module_name}_summary.json`: 模块摘要
   ```json
   {
     "module_name": "example_module",
     "extraction_date": "2025-07-01T10:21:33",
     "statistics": {
       "total_files": 5,
       "total_size_bytes": 26214,
       "total_size_mb": 0.25,
       "file_types": {
         ".py": 3,
         ".xml": 1,
         ".csv": 1
       }
     }
   }
   ```

4. `{module_name}_index.json`: 文件索引
   - 包含所有文件的路径和校验和
   - 文件大小和类型统计

## 支持的文件类型

- Python (`.py`)
- XML (`.xml`)
- CSV (`.csv`)
- YAML (`.yml`, `.yaml`)
- JavaScript (`.js`)
- SCSS/CSS (`.scss`, `.css`)
- HTML (`.html`)
- 文本文件 (`.txt`)

## 开发指南

### 环境设置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"
```

### 构建包

```bash
# 安装构建工具
pip install build wheel

# 构建包
python -m build
```

### 运行测试

```bash
python -m pytest tests/
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 作者

您的名字 - [@yourusername](https://github.com/yourusername)

## 致谢

- 感谢所有贡献者的支持
- Odoo 社区的启发
- 使用本工具的开发者反馈

## 更新日志

### [0.1.0] - 2025-07-01
- 初始发布
- 基本功能实现
- 支持主要文件类型的解析
