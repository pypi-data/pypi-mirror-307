from setuptools import setup, find_packages

setup(
    name='BuildDeck',
    version="2.0.8",
    packages=find_packages(),  # Automatically finds the `builddeck` package
    install_requires=[
        'Click~=8.1.3',         # CLI library
        'PyYAML~=6.0.2',        # Dependency for YAML configuration
        'requests~=2.32.3',     # Dependency for HTTP requests
        'colorlog~=6.8.2',      # For colored logging
        'docker~=7.1.0',        # For Docker interaction
    ],
    entry_points='''
        [console_scripts]
        builddeck=builddeck.cli:cli
    ''',
    author='Leul Tewolde',
    author_email='leul@mereb.app',
    description='A CLI tool for managing services and deployments.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rmhy-tech/builddeck',  # Replace with your GitHub repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
