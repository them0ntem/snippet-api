import os

from pip.req import parse_requirements
from setuptools import find_packages, setup

install_reqs = parse_requirements("requirements.txt", session=False)

reqs = [str(ir.req) for ir in install_reqs]

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
	README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='snippet-snippet',
	version='0.1',
	packages=find_packages(),
	include_package_data=True,
	license='The MIT License (MIT)',
	description='A Django App to write code and display in pygments format ',
	long_description=README,
	url='https://github.com/manthansharma/snippet-snippet',
	author='Manthan Sharma',
	author_email='hitechmanthan@gmail.com',
	keyworsds='snippet-snippet',
	install_requires=reqs,
    zipsafe=False,
	classifiers=[
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: The MIT License (MIT)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
)
