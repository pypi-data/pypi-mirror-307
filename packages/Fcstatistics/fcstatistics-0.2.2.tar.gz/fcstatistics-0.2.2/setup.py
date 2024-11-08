import setuptools

setuptools.setup(
    name='Fcstatistics',
    version='0.2.2',
    description='Fc statistics algorithm',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='fourchains_R&D',
    author_email='fourchainsrd@gmail.com',
    url='https://github.com/leechaeeyoung/Fc',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
