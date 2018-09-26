from setuptools import setup

setup(
    name = 'shotty',
    version = '0.1',
    author = "Nick Yu",
    author_email = "nick.xi.yu@gmail.com",
    description = "shotty is a tool to manage AWS EC2 snapshots",
    license = "GPLv3+",
    packages = ['shotty'],
    url = "https://github.com/nickgityu/snapshot",
    install_requires = [
        'click',
        'boto3'
    ],
    entry_points = '''
        [console_scripts]
        shotty= shotty.shotty:cli
    ''',
)
