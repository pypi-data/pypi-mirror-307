from setuptools import setup, find_packages

setup(
    name='interact-ms',
    version='0.2',
    description='Interactive GUI for mass spectrometry identification and analysis.',
    author='John Cormican, Sahil Khan, Juliane Liepe, Manuel S. Pereira',
    author_email='juliane.liepe@mpinat.mpg.de',
    include_package_data=True,
    long_description=open('README.md', mode='r', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    py_modules=[
        'interact_ms',
    ],
    entry_points={
        'console_scripts': [
            'interact-ms=interact_ms.api:main',
        ]
    },
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'inspirems==2.0rc8',
        'blinker==1.6.2',
        'click==8.1.3',
        'flask==2.3.2',
        'flask_cors==3.0.10',
        'itsdangerous==2.1.2',
        'psutil==5.9.6',
        'Werkzeug==3.0.1',
    ],
    project_urls={
        'Homepage': 'https://github.com/QuantSysBio/interact-ms',
        'Tracker': 'https://github.com/QuantSysBio/interact-ms/issues',
    },
    zip_safe=False,
)
