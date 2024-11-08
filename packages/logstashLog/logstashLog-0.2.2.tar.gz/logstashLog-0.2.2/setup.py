from setuptools import setup, find_packages

setup(
    name="logstashLog",  # 项目名称
    author="chinaUnicomAi",  # 作者
    version="0.2.2",  # 版本号
    author_email="840215085@qq.com",  # 作者地址
    description="a print log ans search tools",  # 描述
    install_requires=[
        "python-logstash==0.4.8"
        # 指定python-logstash的具体版本，可根据实际情况调整
    ],
    packages=find_packages(),  # 打包地址
    include_package_data=True  # 导入数据

)