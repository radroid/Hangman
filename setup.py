from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='hangman',
      version='0.1.4',
      author='Raj Dholakia',
      author_email='raj9dholakia@gmail.com',
      url='https://gtihub.com/radroid',
      license='MIT open-source licence',
      description='hangman game package',
      keywords=['hangman', 'simple hangman', 'hangman package', 'game', 'game package', 'play hangman'],
      long_description=long_description,
      packages=['Hangman'],
      zip_safe=False,
      classifiers=[
          'Development Status :: 2 - Beta',
          'Intended Audience :: End Users/Desktop',
          'License :: MIT',
          'Operating System :: Linux/MacOs',
          'Programming Language :: Python',
          'Topic :: Desktop Environment'
      ]
      )
