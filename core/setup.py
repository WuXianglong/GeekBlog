from setuptools import setup, find_packages

setup(
    name='blog-core',
    version='1.3.4',
    packages=find_packages(),
    license='',
    long_description=open('README.txt').read(),
    author='WuXianglong',
    author_email='wuxianglong098@gmail.com',
    maintainer='WuXianglong',
    url='http://www.xianglong.me/',
    package_data = {
        "blogcore": ['locale/zh_CN/LC_MESSAGES/*.mo'],
        "blogcore.utils": ['verify_code/*.ttf', 'verify_code/*.list'],
    }
)
