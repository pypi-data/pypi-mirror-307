from setuptools import setup, find_packages

setup(
    name='football_manager_scouting',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'soccerplots',
        'sqlalchemy',
        'tqdm',
        'psycopg2-binary'  
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hannes Lindbäck',
    author_email='hanneskarllindback@gmail.com',
    description='A football manager scouting tool',
    url='https://github.com/HannesLindback/football-manager-scouting',
)
