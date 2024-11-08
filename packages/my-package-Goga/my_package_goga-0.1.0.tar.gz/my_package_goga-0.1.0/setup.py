from setuptools import setup, find_packages

setup(
    name='my_package_Goga',  # Replace with your package name
    version='0.1.0',
    author='Jaskaran Singh Goga',
    author_email='gogaismyname@example.com',
    description='Module_Personal',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my-package',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here (from requirements.txt)
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
