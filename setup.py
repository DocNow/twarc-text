import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name='twarc-text',
    version='0.0.1',
    url='https://github.com/docnow/twarc-text',
    author='Ed Summers',
    author_email='ehs@pobox.com',
    py_modules=['twarc_text'],
    description='A twarc plugin to print tweets to the terminal',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.3',
    install_requires=['twarc>=2.7.0', 'maya', 'wcwidth'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points='''
        [twarc.plugins]
        text=twarc_text:text
    '''
)
