from setuptools import setup, find_packages

setup(
   name='meu_investimento',
   version='0.1',
   packages=find_packages(),
   install_requires=[],
   author='Enio Lacerda',
   author_email='enioras@hotmail.com',
   description='Uma biblioteca para cálculos de investimentos.',
   url='https://github.com/tadrianonet/meu_investimento',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)