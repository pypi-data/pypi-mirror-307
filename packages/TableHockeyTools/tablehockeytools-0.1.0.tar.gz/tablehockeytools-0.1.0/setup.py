from setuptools import setup, find_packages

setup(
    name='TableHockeyTools',               # Your package name (must be unique on PyPI)
    version='0.1.0',                    # Initial version
    packages=find_packages(),           # Automatically finds the package
    description='A collection of tools for working with TableHockey data.',  # Give a short description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Make sure README is in markdown
    author='Benjamin Nygard',           # Your name
    author_email='Benjamin.nygard13@gmail.com',  # Your email
    url='https://github.com/Benginy-lab/TableHockeyTools.git', # Link to your repository
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',            # Minimum Python version
    license='MIT',
    install_requires=[
        'beautifulsoup4',  # The actual name for `bs4` on PyPI
        'require'
    ],
)