from setuptools import setup, find_packages

setup(
    name='verify-project-demo-181e3a37',
    version='0.1.1',
    author='doc',
    author_email='nikoduck@gmail.com',
    description='A sample Python package that generates test code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/verify-project-demo-181e3a37',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
