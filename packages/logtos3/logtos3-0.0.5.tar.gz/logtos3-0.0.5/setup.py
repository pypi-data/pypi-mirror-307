from setuptools import setup, find_packages

setup(
    name='logtos3',
    version='0.0.5',
    description='PYPI creation written by Terry',
    author='taeung28',
    author_email='taeung28@gmail.com',
    url='https://www.linkedin.com/in/tae-ung-hwang-790014221/',
    install_requires=['boto3', 'pandas',],
    packages=find_packages(exclude=[]),
    keywords=['terry', 'log', 's3', 'log2s3', 'logtos3', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)