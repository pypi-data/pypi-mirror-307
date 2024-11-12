from setuptools import setup, find_packages
import os

# Read version from __init__.py
with open(os.path.join('cli2web', '__init__.py'), 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'").strip('"')
            break

# Read long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cli2webui',
    version=version,
    description='A tool to convert CLI tools to web interfaces',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Wang Maobin',
    author_email='wangmaobin@iscas.ac.cn',
    url='https://github.com/wangmaobin/cli2webui',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'cli2web': [
            'templates/*.html',
            'templates/*',
            'static/*',
            'static/**/*',
        ],
    },
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SocketIO',
        'eventlet',
        'pygments',
        'tqdm',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.6',
) 