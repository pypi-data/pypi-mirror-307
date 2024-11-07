from setuptools import setup, find_packages

setup(
    name='pyscratchauth',
    version='1.0.0-beta',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyperclip',
        'colorama',
    ],
    author='G1ad0s',
    author_email="on67703@gmail.com",
    description='PyAuthScratch is a scratch auth program',
    url='https://github.com/G1ad0s/pyauthscratch',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
