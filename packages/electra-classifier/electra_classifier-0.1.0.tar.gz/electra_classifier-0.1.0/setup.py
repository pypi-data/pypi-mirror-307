from setuptools import setup, find_packages

setup(
    name='electra-classifier',
    version='0.1.0',
    description='Electra Classifier for Sentiment Analysis',
    author='Jim Beno',
    author_email='jim@jimbeno.net',
    url='https://github.com/jbeno/electra-classifier',
    packages=find_packages(),
    install_requires=[
        'torch>=1.8.0',
        'transformers>=4.5.0'
    ],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
