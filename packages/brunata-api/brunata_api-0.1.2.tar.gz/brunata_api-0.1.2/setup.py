from setuptools import setup, find_packages

setup(
    name='brunata-api',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'httpx>=0.27.2',
    ],
    author='Yuki Electronics',
    author_email='yuki@yukie.dev',
    description='A short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://codeberg.org/YukiElectronics/brunata-api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

