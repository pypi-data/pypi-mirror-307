from setuptools import setup, find_packages

setup(
    name='robotic_arm_package',
    version='4.3.6',
    # url='https://github.com/your_username/your_package_name',
    license='MIT',
    author='Realman-Aisha',
    author_email='aisha@realman-robot.com',
    # description='',
    # 假设你有一个README.md文件
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        # 你的包所依赖的其他Python包列表
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    packages=find_packages(),
    # package_data={
    #     'libs': ['linux_arm/*', 'linux_x86/*.so', 'win_32/*.dll', 'win_64/*.dll'],
    # },
    # ... 其他参数 ...
)
