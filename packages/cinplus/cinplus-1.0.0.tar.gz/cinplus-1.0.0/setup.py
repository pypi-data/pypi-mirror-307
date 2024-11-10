from setuptools import setup, find_packages

setup(
    name='cinplus',
    version='1.0.0',
    author='woskethebot',
    author_email='nushratakhter1999@gmail.com',
    description='A Python module that extends the basic input function with 16 different parameters and many combinations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/woskethebot/cinplus',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
