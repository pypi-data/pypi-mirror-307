from setuptools import setup, find_packages

setup(
    name='country_population',
    version='0.1.0',
    author='Maharshi Choudhury',
    author_email='maharshi.choudhury@gmail.com',
    description='A package to fetch and sort countries by population',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/country_population',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'country_population=country_population:main',
        ],
    },
)
