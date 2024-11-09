from setuptools import setup, find_packages

setup(
    name='BinhoPulsar',
    version='0.3.0',
    packages=find_packages(),
    description='Basic SDK for Binho Pulsar',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Binho LLC',
    author_email='support@binho.io',
    url='https://github.com/binhollc/PulsarSDK',
    license='Private',
    install_requires=[
        "pyserial",
        "hidapi",
        "psutil",
    ],
    package_data= {
        'BinhoPulsar': ['SupernovaSDK/BinhoSupernova/*',
                        'SupernovaSDK/BinhoSupernova/**/*'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)