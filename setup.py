from setuptools import setup


setup(
    name='urlwait',
    version='1.0',
    description='A CLI utility for blocking until a service is listening',
    long_description=open('README.rst').read(),
    author='Paul McLanahan',
    author_email='paul@mclanahan.net',
    license='MIT',
    py_modules=['urlwait'],
    entry_points={
        'console_scripts': ['urlwait = urlwait:main'],
    },
    url='https://github.com/pmac/urlwait',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Systems Administration'
    ],
    keywords=['database_url', 'tcp', 'port', 'docker', 'service',
              'deploy', 'deployment'],
)
