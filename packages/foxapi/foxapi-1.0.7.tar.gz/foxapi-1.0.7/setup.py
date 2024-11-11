from setuptools import setup, find_packages
# from BotAmino.__init__ import __version__

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name='foxapi',
    version="1.0.7",
    url='https://github.com/ThePhoenix78/FoxAPI',
    download_url='https://github.com/ThePhoenix78/FoxAPI/tarball/master',
    license='MIT',
    author='ThePhoenix78',
    author_email='thephoenix788@gmail.com',
    description='A wrapper for the foxhole API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'foxhole',
        'foxapi'
    ],
    install_requires=[
        'requests',
        'pillow',
    ],
    setup_requires=[
        'wheel'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages()
    # packages=["sdist", "bdist_wheel"]
    # python_requires='>=3.6',
)
