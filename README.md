# snapshot

Demo project to manage EC2 snapshots

# about
use boto3 to manage EC2 snapshots

# configuration

shotty use the configuration file created by the AWS calc_dist

'aws configuration --profile shotty'

#running

'pipenv run python shotty/shotty.py <command> <subcommand> <--project=PROJECT>'

*command* is instances, volumes and Snapshots
*subcommand* -depends on command
*project* is optional
*build package*
  pipenv run python setup.py bdist_wheel
  pip3 install dist/shotty-0.1-py3-none-any.whl

#usage
  i.e. shotty instances list
