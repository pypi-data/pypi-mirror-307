from setuptools import setup, find_packages

setup(
    name='dharun',
    version='1.3',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dharun',
    author_email='leodas@gmail.com',
    description='Some Optimization Problems for Machine Learning',
    url='https://github.com/KeerthiVasan-ai/optimization-techniques', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
)
