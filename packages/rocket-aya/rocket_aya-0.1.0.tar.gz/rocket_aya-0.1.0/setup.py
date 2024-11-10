# setup.py
from setuptools import setup, find_packages

setup(
    name='rocket-aya',  # Update this to your new unique name
    version='0.1.0',
    packages=find_packages(),
    description='A simple rocket module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='aya',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/rocket-aya',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)

