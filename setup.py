from setuptools import setup, find_packages

setup(
    name='cryptosignalbot',
    version='1.0.0',
    author='ShiroNamakoto',
    author_email='dmitriyklyatva@gmail.com',
    description='AI Trading Signal Generator',
    packages=find_packages(),  # <-- ВАЖНО: убрали where='src'
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'matplotlib',
    ],
)