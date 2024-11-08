from setuptools import setup, find_packages

setup(
    name='RapidHost',
    version='4.0.1',
    description='A simple Flask Based library for serving HTML pages with customizable host IP, port, and template path.',
    author='Leonardo',
    author_email='Leonardonery616@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0.0'
    ],
    entry_points={
        'console_scripts': [
            'rapidhost=rapid_host.__init__:main'
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
