import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    if project:
        filters = [{'Name': 'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """Shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
        """Command for snapshots"""

@snapshots.command('snapshot'
    help="Create snapshots of all volumes")
@click.option('--project', default = None,
        help="Only Snapshots for project (tag Project:<name>)")
def create_snapshots(project):

    instances = filter_instances(project)

    for i in instances:
        for v in i.volunmes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Descripton = "Created by shotty")

    return
    
@snapshots.command('list')
@click.option('--project', default = None,
        help="Only Snapshots for project (tag Project:<name>)")

def list_volumes(project):
    "List EC2 snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", " .join((
                s.id,
                v.id,
                i.id,
                s.state,
                s.progress,
                s.start_time.strftime("%c")
                )))
    return

@cli.group('volumes')
def volumes():
    """Command for volumes"""

@volumes.command('list')
@click.option('--project', default = None,
    help="Only Volumes for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", " .join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return

@cli.group('instances')
def instances():
    """Command for instances"""

@instances.command('list')
@click.option('--project', default = None,
    help="Only instance for project (tag Project:<name>)")
def list_instance(project):
    "List EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        print(', ' .join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name,
        tags.get('Project', '<no project>')
        )))

    return
@instances.command('stop')
@click.option('--project', default = None,
    help="Only instance for project (tag Project:<name>)")
def stop_instance(project):
    "Stop EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default = None,
    help="Only instance for project (tag Project:<name>)")
def start_instance(project):
    "Start EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return

if __name__ == '__main__':
        cli()
