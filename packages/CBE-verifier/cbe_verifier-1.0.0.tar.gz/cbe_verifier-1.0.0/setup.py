from setuptools import setup, find_packages

setup(
    name='CBE_verifier',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'easyocr', 
        'opencv-python', 
        'pillow',           
        'pyzbar',           
        'numpy',
    ],
    author='Zahir Seid',
    author_email='Zahirseid101@gmail.com',
    description='A transaction verification library for CBE.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Zahir-Seid/CBE_verifier',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
