from setuptools import setup, find_packages

setup(
    name='linklinux-init',
    version='1.2.0',
    description='A tool to configure initial development environment on Linux',
    long_description=open('README.rst').read(),
    author='Vincnent Su',
    author_email='suyelu@hotmail.com',
    url='https://github.com/suyelu/LinkLinux_Init',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'linklinux-init=linklinux_init.main:main',  # 创建一个命令来执行 Python 入口
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)

