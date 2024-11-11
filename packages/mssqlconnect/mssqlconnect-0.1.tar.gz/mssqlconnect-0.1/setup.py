from setuptools import setup, find_packages

setup(
    name='mssqlconnect',
    version='0.1',
    packages=find_packages(),
    description='mssqlconnect',
    long_description=open('README.md').read(),
    # python3，readme文件中文报错
    # long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    # url='http://github.com/yourusername/my_package',
    author='棽杓',
    author_email='1047366140@qq,com',
    license='MIT',
    install_requires=[
        "pymssql"
    ],
    classifiers=[
        # 分类信息
    ]
)