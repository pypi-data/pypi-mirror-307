from setuptools import setup, find_packages

setup(
    name='vector_nest',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'sentence-transformers',
    ],
    test_requires=[
        'pytest',
    ],
    description='A package for text similarity and embeddings',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Penjarla Sai Ram',
    author_email='psairam9301@gmail.com',
    url='https://github.com/sairam-penjarla/vector_nest.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
