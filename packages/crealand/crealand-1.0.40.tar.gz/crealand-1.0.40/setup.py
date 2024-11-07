from setuptools import setup, find_packages

name = 'crealand'
# 正式版本号
version = '1.0.40'
# 测试版本号
# version = '1.0.9'
description = 'Python SDK for Crealand'
author = 'UBTECH Robotics'
author_email = 'swenggroup@ubtrobot.com'

package_dir = {
    'crealand': 'crealand'
}

package_data = {
}

install_requires = [
    'websockets'
]

# require_data_files = ['requirements.txt']
require_data_files = []
example_data_files = [
]
doc_data_files = [
]

data_files = []
try:
    data_files.extend(require_data_files)
    data_files.extend(example_data_files)
    data_files.extend(doc_data_files)
except:
    pass

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    packages=find_packages(),
    package_dir=package_dir,
    package_data=package_data,
    data_files=data_files,
    install_requires=install_requires
)
