from setuptools import setup
from pip.req import parse_requirements

import gsm_modem_asyncio as package


install_reqs = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_reqs]

setup(
    name=package.__name__,
    version=package.__version__,
    packages=[package.__name__],
    url='https://github.com/insolite/{}'.format(package.__name__),
    author='Oleg Krasnikov',
    author_email='a.insolite@gmail.com',
    description='GSM modem control library',
    include_package_data=True,
    install_requires=requirements,
    # entry_points={
    #     'console_scripts': [
    #         '{0} = {0}.scripts.cli:main'.format(package.__name__),
    #     ],
    # },
)
