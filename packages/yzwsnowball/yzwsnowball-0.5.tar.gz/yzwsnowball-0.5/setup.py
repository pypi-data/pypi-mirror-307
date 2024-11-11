from setuptools import setup, find_packages

setup(
    name='yzwsnowball',  # 你的包的名称
    version='0.5',  # 版本号
    packages=find_packages(),  # 自动找到包内所有模块
    install_requires=[
        # 你的包依赖的其他库
    ],
    author='JY Yu Chi Wai',
    author_email='13715416@qq.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yzw2010/jysnowball/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 指定兼容的Python版本
)
