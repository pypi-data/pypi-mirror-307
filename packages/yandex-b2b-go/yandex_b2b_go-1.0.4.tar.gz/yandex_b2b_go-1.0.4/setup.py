from setuptools import find_packages, setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


def get_version():
    version = {}
    with open('yandex_b2b_go/version.py') as file:
        exec(file.read(), version)
    return version['__version__']


with open('requirements.txt') as r:
    requirements = []
    for line in r.readlines():
        line = line.strip()
        if line != '':
            requirements.append(line)


setup(
    name='yandex_b2b_go',
    version=get_version(),
    author='Yandex LLC',
    author_email='b2b-go@yandex-team.ru',
    description='Yandex GO for Business SDK',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords=['yandex', 'go', 'b2b', 'sdk', 'library', 'api'],
    install_requires=requirements,  # requirements.txt
    license='MIT',
    python_requires='>=3.8',
    packages=find_packages(".", include=["yandex_b2b_go*"]),
    tests_require=['pytest'],
)
