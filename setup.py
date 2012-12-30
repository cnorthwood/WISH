from distutils.core import setup

setup(name='WISH',
      version='1.0',
      description='WorldIRC Services Host',
      author='Chris Northwood',
      author_email='laser@worldirc.org',
      packages=['wish', 'wish.irc', 'wish.p10', 'wish.p10.commands'],
     )
