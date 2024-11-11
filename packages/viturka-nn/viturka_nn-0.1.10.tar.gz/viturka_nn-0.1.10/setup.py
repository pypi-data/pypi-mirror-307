from setuptools import setup, find_packages

setup(
    name='viturka_nn',
    version='0.1.10',
    description='A client library for deep federated learning platform.',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'torch',
        'torchvision',
        'pycocotools',
        'scikit-learn'
    ],
    python_requires='>=3.6'
)