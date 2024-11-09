from setuptools import setup, find_packages

setup(
    name='firebase-main',
    version='1.2.3',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'trackdir',
    ],
    entry_points={
        'console_scripts': [
            'firebase-main=firebase_main.cli:main',
        ],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    author='MrFidal',
    author_email='mrfidal@proton.me',
    url='https://github.com/ByteBreach/firebase-main',
)
