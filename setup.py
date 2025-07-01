from setuptools import setup, find_packages

setup(
    name="odoo-extractor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # 目前没有外部依赖
    
    # 命令行工具配置
    entry_points={
        'console_scripts': [
            'odoo-extract=odoo_extractor.extractor:main',
        ],
    },
    
    # 元数据
    author="Jesse Chang",
    author_email="lcf.zhangxing@hotmail.com",
    description="A tool to extract Odoo module code for AI analysis",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="odoo, development, AI, code extraction",
    url="https://github.com/yourusername/odoo-extractor",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
