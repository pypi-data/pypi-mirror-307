from setuptools import setup

with open('README.md') as arq:
    readme = arq.read()

setup(name='auto-logout-pipy',
    version='0.0.2',
    author ='José Carlos Tenório',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='jcsilva.tenorio@gmail.com',
    keywords='django auto logout',
    description=u'Django auto logout não oficial para Django',
    packages=['my-auto-logout'],
    install_requires=['logging', 'typing'],
)