from setuptools import setup, find_packages

setup(
    name='Fsys',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    description="Fsys is a lightweight, efficient filesystem with dynamic partitioning, caching, and data integrity checks. It's ideal for embedded systems, servers, and cloud environments, with cross-platform compatibility and simple APIs.",
    url='https://github.com/DevByEagle/Fsys',
)
