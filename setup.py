import setuptools

setuptools.setup(
    name='anycmd-jupyter-magic',
    version = '0.1.4',
    packages = setuptools.find_packages(),
    author = 'Justin Douty',
    author_email = "jdouty03@icloud.com",
    description = "A versatile Jupyter cell magic that allows running a cell with any command line utility.",
    keywords = ['ipython', 'jupyter', 'magic', 'cell magic', 'command'],
    classifiers = ['Framework :: IPython', 'Framework :: Jupyter', 'Framework :: Jupyter :: JupyterLab', 'Framework :: Jupyter :: JupyterLab :: Extensions', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Programming Language :: Python', 'Programming Language :: Python :: 3.7'],
    url='https://github.com/zenarcher007/AnyCmd',
    license = "MIT",
    platforms='any',
    long_description=open('README.md').read(),
    long_description_content_type = "text/markdown",
    install_requires = [
      "argparse",
      "uuid"
    ],
    
)
