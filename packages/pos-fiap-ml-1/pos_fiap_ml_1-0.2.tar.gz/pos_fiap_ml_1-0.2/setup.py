from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
   name='pos_fiap_ml_1',
   version='0.2',
   packages=find_packages(),
   install_requires=[],
   author='XXXXXX',
   author_email='leandro.lhbb@gmail.com',
   description='Uma biblioteca para cálculos de investimentos.',
   url='https://github.com/Leandro-barreto/fiap_mleng.git',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
   license='MIT',
   long_description=long_description,
   long_description_content_type='text/markdown' 
)