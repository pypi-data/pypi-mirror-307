from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='connor_nlp',
    version='0.1.8',
    packages=find_packages(exclude=['connor/connor_nlp/data']),
    include_package_data=True,
    package_data={
        'connor': ['connor_nlp/data/*'],
    },
    install_requires=[
        "docx==0.2.4",
        "python_pptx==1.0.2",
        "python_docx==0.8.11",
        "nltk==3.9.1",
        "numpy==2.1.2",
        "odfpy==1.4.1",
        "openpyxl==3.1.5",
        "PyPDF2==3.0.1",
        "PyQt6==6.7.1",
        "scikit_learn==1.5.2",
        "sentence_transformers==3.2.0",
    ],
    entry_points={
        'console_scripts': [
            'connor=connor.main:main',
        ],
    },
    author='Ycatsh',
    description='Fast and fully local NLP file organizer that organizes files based on their content.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ycatsh/connor',
    license='MIT',
    license_file='LICENSE',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10'
)