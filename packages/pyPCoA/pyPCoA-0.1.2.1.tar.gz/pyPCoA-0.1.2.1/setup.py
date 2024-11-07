from setuptools import setup, find_packages

setup(
    name='pyPCoA',
    version='0.1.2.1',
    description='A package for Principal Coordinates Analysis (PCoA) with Jaccard and Bray-Curtis distances.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yuki Hamaguchi',
    author_email='Yuki_Hamaguchi@suntory.co.jp',
    url='https://github.com/YukiHSun/pyPCoA',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'pyPCoA=pyPCoA.core:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
