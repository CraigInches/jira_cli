from setuptools import setup

setup(name='jira_cli',
      version='0.1',
      description='dont like GUIs',
      url='https://github.com/CraigInches/jira_cli',
      author='Craig Inches',
      author_email='craig@craiginches.com',
      license='AGPLv3',
      packages=['jira_cli'],
      install_requires=[
          'oauth2',
          'tlslite_ng'],
      entry_points ={
          'console_scripts': [
              'jira_cli = jira_cli.__main__:main'
          ]
      })
