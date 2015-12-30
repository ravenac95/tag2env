import os
import re
import requests
import boto3
import click


AWS_INSTANCE_DOC_URL = 'http://169.254.169.254/latest/dynamic/instance-identity/document'


class TagLoader(object):
    def __init__(self, override_instance_doc=None, override_instance_id=None):
        self._override_instance_doc = override_instance_doc
        self._override_instance_id = override_instance_id

    def load_tags(self):
        instance_id = None
        if self._override_instance_id:
            instance_id = self._override_instance_id
        else:
            local_instance_document = self.local_instance_document
            instance_id = local_instance_document['instanceId']
        tags = {}

        for orig_tag_key, tag_value in self.load_tags_for_instance(instance_id):
            orig_tag_key = re.sub(r'[^\w\s]', '_', orig_tag_key)
            orig_tag_key = re.sub(r'\s+', '_', orig_tag_key)
            tag_key = "EC2_TAG_%s" % orig_tag_key.upper()
            tags[tag_key] = tag_value
        return tags

    def load_tags_for_instance(self, instance_id):
        next_token = None
        while True:
            kwargs = dict(
                Filters=[
                    {
                        'Name': 'resource-id',
                        'Values': [
                            instance_id
                        ]
                    }
                ]
            )
            if next_token:
                kwargs['NextToken'] = next_token

            response = self.client.describe_tags(**kwargs)
            for tag in response['Tags']:
                yield (tag['Key'], tag['Value'])
            next_token = response.get('NextToken')
            if not next_token:
                break

    @property
    def client(self):
        return boto3.client('ec2')

    @property
    def local_instance_document(self):
        if self._override_instance_doc:
            return self._override_instance_doc
        return requests.get(AWS_INSTANCE_DOC_URL)


def load_instances_tags(instance_id=None):
    """Loads all of the tags for an instance"""
    loader = TagLoader(override_instance_id=instance_id)
    return loader.load_tags()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--instance-id', help='Override the instance id')
def script(instance_id):
    tags = load_instances_tags(instance_id=instance_id)
    for env_var, value in tags.iteritems():
        print "export %s='%s'" % (env_var, value)


@cli.command(name='exec')
@click.argument('command')
@click.option('--instance-id', help='Override the instance id')
def exec_in_env(command, instance_id):
    import subprocess
    import shlex

    command_env = {}
    command_env.update(os.environ)
    command_env.update(load_instances_tags(instance_id=instance_id))

    # Execute the passed in command
    subprocess.check_call(shlex.split(command), env=command_env)


if __name__ == "__main__":
    cli()
