from setuptools import setup, find_packages


def requirements():
    required = []
    try:
        with open('requirements.txt', encoding='utf-8') as f:
            required = f.read().splitlines()
    except:
        print(f'ERROR: open `requirements.txt` failed')
    return required


def readme():
    with open("README.md", "r", encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# ------------------------------------------------------------------------------

VERSION = "1.0.1"
PACKAGE_NAME = "baotool"


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Nisus Liu",  # 作者名称
    author_email="609069481@qq.com", # 作者邮箱
    description="BaoTool (宝图), 个人积累的 python 工具库", # 库描述
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # 自动找包 __init__.py
    install_requires=requirements(),
    keywords=['python', 'tool', 'util', 'baotool', 'bao tool', 'log'],
    # data_files=[('cut_video', ['cut_video/clip_to_erase.json'])], # yourtools库依赖的其他库
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT",
    url="https://pypi.org/project/bao-tool/", # 库的官方地址
    include_package_data=True,
    # package_data={
    #     "": ['requirements.txt', "README.md", 'VERSION'],  # 指定哪些文件应该被包含
    # },
)



# def split_version(version):
#     # 从版本号字符串中提取三个数字并将它们转换为整数类型
#     match = re.search(r"(\d+)\.(\d+)\.(\d+)", version)
#     major = int(match.group(1))
#     minor = int(match.group(2))
#     patch = int(match.group(3))
#
#     # 对三个数字进行加一操作
#     patch += 1
#     if patch > 9:
#         patch = 0
#         minor += 1
#         if minor > 9:
#             minor = 0
#             major += 1
#     new_version_str = f"{major}.{minor}.{patch}"
#     return new_version_str
#
#
# def upload():
#     long_description = readme()
#     required = requirements()
#
#     setuptools.setup(
#         name=PACKAGE_NAME,
#         version=curr_version(),
#         author="Nisus Liu",  # 作者名称
#         author_email="609069481@qq.com", # 作者邮箱
#         description="BaoTool (宝兔), 个人积累的 python 工具库", # 库描述
#         long_description=long_description,
#         long_description_content_type="text/markdown",
#         url="https://pypi.org/project/bao-tool/", # 库的官方地址
#         packages=setuptools.find_packages(),
#         data_files=["requirements.txt"], # yourtools库依赖的其他库
#         classifiers=[
#             "Programming Language :: Python :: 3",
#             "License :: OSI Approved :: MIT License",
#             "Operating System :: OS Independent",
#         ],
#         python_requires='>=3.6',
#         install_requires=required,
#         include_package_data=True,
#         # package_data={
#         #     "": ['requirements.txt', "README.md", 'VERSION'],  # 指定哪些文件应该被包含
#         # },
#     )
#
#
# def write_now_version():
#     print("Current VERSION:", split_version())
#     with open("VERSION", "w", encoding='utf-8') as version_f:
#         version_f.write(split_version())
#
#
# def main():
#     try:
#         upload()
#         print("Upload success , Current VERSION:", curr_version())
#     except Exception as e:
#         raise Exception("Upload package error", e)
#
#
# if __name__ == '__main__':
#     main()
