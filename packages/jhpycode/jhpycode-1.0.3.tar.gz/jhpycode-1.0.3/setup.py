import setuptools  # 导入setuptools打包工具

requirements = []
with open('requirements.txt', 'r', encoding="utf-8") as fhr:
    for line in fhr:
        requirements.append(line.strip())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jhpycode",  # 用自己的名替换其中的YOUR_USERNAME_
    version="1.0.3",  # 包版本号，便于维护版本,保证每次发布都是版本都是唯一的
    author="PJH",  # 作者，可以写自己的姓名
    author_email="ppsq7777@163.com",  # 作者联系方式，可写自己的邮箱地址
    description="自用分析银行卡",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="",  # 自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires = requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)