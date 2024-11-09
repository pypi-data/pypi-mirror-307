from setuptools import setup, find_packages

setup(
    name='blackboxai-chat',
    version='0.1.1',
    author='BLACKBOXAI',
    author_email='robocoder-repo@blackboxai.tech',
    description='BlackboxAI is AI pair programming in your terminal',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)