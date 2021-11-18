import setuptools


VERSION = '0.1.0'


setuptools.setup(
    name='toniback',
    packages=setuptools.find_packages(),
    version=VERSION,
    description='-/-',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Euromance/toniback',
    author='Euromancer',
    author_email='euromancer@icloud.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Repository': 'https://github.com/Euromance/toniback',
    },
    python_requires='>=3.9,<4.0',
    install_requires=[
        'SQLAlchemy-Utils==0.37.9',
        'SQLAlchemy==1.4.27',
        'alembic==1.7.5',
        'databases[postgresql]==0.5.3',
        'psycopg2-binary==2.9.2',
        'pydantic==1.8.2',
    ],
    extras_require={
        'dev': [
            'flake8-commas==2.1.0',
            'flake8-import-order==0.18.1',
            'flake8-quotes==3.3.1',
            'flake8==4.0.1',
            'pep8-naming==0.12.1',
        ],
        'test': [
            'pytest-asyncio==0.16.0',
            'pytest-cov==3.0.0',
            'pytest-freezegun==0.4.2',
            'pytest-mock==3.6.1',
            'pytest==6.2.5',
        ],
        'vim': [
            'pyls-flake8==0.4.0',
            'pynvim==0.4.3',
            'python-lsp-server==1.2.4',
        ],
    },
)
