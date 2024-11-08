from setuptools import setup

with open('README.md') as arq:
    readme = arq.read()

setup(name='auto-logout-django',
    version='0.0.3',
    author ='José Carlos Tenório',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='jcsilva.tenorio@gmail.com',
    keywords='django auto logout',
    description=u'Django auto logout não oficial para Django',
    packages=['auto-logout-django'],
    install_requires=['logging', 'typing'],
)