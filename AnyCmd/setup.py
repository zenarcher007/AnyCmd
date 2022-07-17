from distutils.core import setup

setup(
    name='AnyCmd',
    version='0.1.0',
    author='Justin Douty',
    author_email='jdouty03@icloud.com',
    py_modules=['anycmd'],
    #url='',
    license='LICENSE',
    description='IPython cell magic to run a custom command',
    long_description=open('README.md').read(),
)
