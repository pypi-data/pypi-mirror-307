from setuptools import setup, find_packages
import io

with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cli2webui",
    version="0.1.0",
    author="skyfire",
    author_email="skyfireitdiy@hotmail.com",
    description="将命令行工具转换为 Web 界面的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skyfireitdiy/cli2web",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.0",
        "Flask-SocketIO>=5.0.0",
        "eventlet>=0.33.0",
        "python-socketio>=5.0.0",
        "python-engineio>=4.0.0",
        "urllib3>=1.26.0,<2.0.0",  # 限制 urllib3 版本
        "pygments>=2.13.0,<3.0.0",  # 限制 pygments 版本
        "tqdm>=4.64.1",  # 添加缺失的依赖
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "cli2web=cli2web.__main__:main",
        ],
    },
    package_data={
        "cli2web": [
            "templates/*.html",
            "static/css/*.css",
            "static/js/*.js",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
    ],
    keywords=[
        "cli",
        "web",
        "interface",
        "command-line",
        "gui",
        "web-interface",
        "terminal",
        "shell",
        "command",
        "flask",
        "websocket",
    ],
    project_urls={
        "Bug Reports": "https://github.com/skyfireitdiy/cli2web/issues",
        "Source": "https://github.com/skyfireitdiy/cli2web",
        "Documentation": "https://github.com/skyfireitdiy/cli2web#readme",
    },
) 