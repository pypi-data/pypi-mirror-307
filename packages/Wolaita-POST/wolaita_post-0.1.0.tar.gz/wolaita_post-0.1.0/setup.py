# setup.py
from setuptools import setup, find_packages

setup(
    name='Wolaita_POST',  # Unique name on PyPI
    version='0.1.0',
    author='Sisagegn Samuel',
    author_email='samuelsisagegn@gmail.com',
    description='A POS tagger for the Wolaita language using deep learning',
    long_description=open('/content/drive/MyDrive/Wolaita_POST/README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Sisagegn/Wolaita_POST',  # GitHub link
    project_urls={  # Additional URLs for project details
        "Documentation": "https://github.com/Sisagegn/Wolaita_POST/wiki",
        "Source": "https://github.com/Sisagegn/Wolaita_POST",
        "Tracker": "https://github.com/Sisagegn/Wolaita_POST/issues",
    },
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0.0',  # Specify minimum versions to ensure compatibility
        'numpy>=1.18.0',
        'nltk>=3.5',
        'fasttext>=0.9.2'
    ],
    extras_require={  # Optional dependencies for specific use cases
        'dev': ['pytest', 'sphinx'],  # Dependencies for development and testing
        'gpu': ['tensorflow-gpu>=2.0.0'],  # For users with GPU support
    },
    classifiers=[
        'Development Status :: 4 - Beta',  # Specify project maturity level
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Linguistic',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='Wolaita POS tagging NLP deep learning',  # Keywords for discoverability
    python_requires='>=3.6',
    include_package_data=True,  # To include non-code files specified in MANIFEST.in
    package_data={  # Include additional files within the package
        '': ['*.txt', '*.md'],  # For example, README or configuration files
    },
    entry_points={  # Command-line interface entry points if applicable
        'console_scripts': [
            'wolaita-pos=Wolaita_POST.wolaita_pos_tagger:main',  # Example CLI entry point
        ],
    },
)
