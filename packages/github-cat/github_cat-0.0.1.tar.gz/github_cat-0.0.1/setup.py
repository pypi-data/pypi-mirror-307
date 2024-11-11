from distutils.core import setup
from setuptools import find_packages
with open("README.md", "r",encoding='utf-8') as f:
  long_description = f.read()
setup(name='github_cat',  # 包名
      version='0.0.1',  # 版本号
      description='github tools',
      long_description_content_type = 'text/markdown',
      long_description=long_description,
      author='chandler song',
      author_email='275737875@qq.com',
      url='https://www.linkedin.com/in/chandlersong/',
      keywords = "github api tool by token",
      license='MIT',
      packages = find_packages(),
      install_requires=[
          "requests",
      ],
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],

      )