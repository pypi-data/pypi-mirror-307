import setuptools #导入setuptools打包工具

setuptools.setup(
    name="jcw_utils-yingyingguai", # 用自己的名替换其中的YOUR_USERNAME_
    version="0.10.0",    #包版本号，便于维护版本
    author="yingyingguai",    #作者，可以写自己的姓名
    author_email="402117226@qq.com",    #作者联系方式，可写自己的邮箱地址
    description="A small example package",#包的简述
    # long_description=long_description,    #包的详细介绍，一般在README.md文件内
    # long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    package_data={
        # If you have multiple packages, specify each one here
        "jcw_utils": ["*.json", "*.txt","*.jar","*.md5"],
    },
    # classifiers=[
    #     "Programming Language :: Python :: 3.10",
    #     "Programming Language :: Python :: 3.12",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    #     "Development Status :: 5 - Production/Stable",
    #     "Intended Audience :: Developers",
    #     "Topic :: Software Development :: Libraries",
    # ],
    # python_requires='>=3.10',    #对python的最低版本要求
)