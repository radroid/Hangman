"""Settings to assist package installation"""

import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(name='hangman',
                 version='0.2',
                 author='Raj Dholakia',
                 author_email='raj9dholakia@gmail.com',
                 url='https://gtihub.com/radroid/Hangman',
                 license='MIT open-source licence',
                 description='hangman game package',
                 keywords=['hangman', 'simple hangman', 'hangman package',
                           'game', 'game package', 'play hangman'],
                 long_description=long_description,
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 install_requires=[],
                 classifiers=[
                     'Development Status :: 2 - Beta',
                     'Intended Audience :: End Users/Desktop',
                     'License :: MIT',
                     'Operating System :: Linux/MacOs',
                     'Programming Language :: Python',
                     'Topic :: Desktop Environment'
                 ],
                 include_package_data=True,
                 package_data={'': ['data/*.txt', 'examples/*.py']},
                 )
