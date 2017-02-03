import re
import os
from setuptools import setup
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_reqs]
package_name = 'gsm_modem_asyncio'
hyphen_package_name = package_name.replace('_', '-')


def read_version():
    regexp = re.compile(r"^__version__\s*=\s*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), package_name, '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in {}'.format(init_py))


setup(
    name=hyphen_package_name,
    version=read_version(),
    packages=[package_name],
    url='https://github.com/insolite/{}'.format(hyphen_package_name),
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
