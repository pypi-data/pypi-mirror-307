from setuptools import setup, find_packages

setup(
    name='kind-quasar',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kind-quasar=kind_quasar.cli:main',
        ],
    },
    description='A simple package to calculate net profit and ROI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Semyon Drozdov',
    author_email='s.drozdov@edu.centraluniversity.ru',
    url='https://github.com/yourusername/finance_calculator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
