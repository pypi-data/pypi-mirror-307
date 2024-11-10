from distutils.core import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'Flask_J2S',         # How you named your package folder (MyLib)
    packages = ['Flask_J2S'],   # Chose the same as "name"
    version = '1.9',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Set Flask From JSON',   # Give a short description about your library
    long_description=long_description,            # Give a long description about your library
    long_description_content_type='text/markdown',
    author = 'KIMIN',                   # Type in your name
    author_email = 'staykimin@gmail.com',      # Type in your E-Mail
    url = 'https://github.com/staykimin/Flask-J2S',   # Provide either the link to your github or to your website
    # download_url = 'https://github.com/staykimin/Modul-Wrapper/archive/Modul-Wrapper-0.1.tar.gz',    # I explain this later on
    project_urls={
        'Documentation': 'https://github.com/staykimin/Flask-J2S',
        'Funding': 'https://github.com/staykimin/Flask-J2S',
        'Say Thanks!': 'https://saweria.co/staykimin',
        'Source': 'https://github.com/staykimin/Flask-J2S',
        'Tracker': 'https://github.com/staykimin/Flask-J2S/issues',
    }, 
    keywords = ['Kimin', 'Flask', 'Flask-J2S', 'J2S'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'Flask',
		  'Flask-Cors',
          'colorama',
		  'requests',
		  'Modul-Wrapper'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ], 
)