from setuptools import setup, find_packages
import os

# Safely load the README file
def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, encoding="utf-8") as f:
            return f.read()
    return ""

setup(
    name='TableHockeyTools',               
    version='0.1.2',                    
    packages=find_packages(),           
    description='A collection of tools for working with TableHockey data.',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    author='Benjamin Nygard',           
    author_email='Benjamin.nygard13@gmail.com',
    url='https://github.com/Benginy-lab/TableHockeyTools.git',
    package_data={
        '': ['TableHockeyTools.1'],  # Add the man page file here
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
    install_requires=[
        'beautifulsoup4',
        'require'
    ],

)
