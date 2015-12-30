tag2env - Turn EC2 tags into environment variables
==================================================

This is a fairly simple app that turns ec2 tags into environment variables

## How it works

It turns your tags like:

    Name: my name
    some_tag: this is a tag

Into:

    EC2_TAG_NAME="my name"
    EC2_SOME_TAG="this is a tag"

## Usage

### Execute another command with the correct environment

    $ tag2env exec 'env' # This will execute the `env` command with the ec2 tags injected in the environment

### Export a sourceable bash script 

    $ tag2env script > ec2_tags.sh

### Export directory

    $ eval "$(tag2env script)"
