from setuptools import setup, find_packages

setup(
    name='aya-linear-regression',
    version='0.1.0',
    packages=find_packages(),
    description='A simple linear regression model from scratch',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='aya',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/aya-linear-regression',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)