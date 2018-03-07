import json
import os

from testapiclient import command
from testapiclient import http_client
from testapiclient import identity

PODS_URL = os.environ.get('testapi_url') + "/pods"


class PodGet(command.Lister):
    "Handle get request for pods"

    def get_parser(self, prog_name):
        parser = super(PodGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Search pods using name')
        return parser

    def take_action(self, parsed_args):
        url = PODS_URL
        if(parsed_args.name):
            url = PODS_URL + "?name=" + parsed_args.name
        pods = http_client.get(url)
        print pods


class PodGetOne(command.ShowOne):
    "Handle get request for pod by name"

    def get_parser(self, prog_name):
        parser = super(PodGetOne, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Find pod using name',
                            required=True)
        return parser

    def take_action(self, parsed_args):
        pods = http_client.get(PODS_URL + "/" + parsed_args.name)
        print pods


class PodCreate(command.Command):
    "Handle post request for pods"

    def get_parser(self, prog_name):
        parser = super(PodCreate, self).get_parser(prog_name)
        parser.add_argument('pod',
                            type=json.loads,
                            help='Pod create request format :\n'
                                 '\'{"role": "", "name": "", "details": "", '
                                 '"mode": ""}\',\n role should be either '
                                 '"community-ci" or "production-ci", and '
                                 'mode should be either "metal" or "virtual.')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        response = http_client.post(PODS_URL,
                                    parsed_args.pod)
        if response.status_code == 200:
            print "Pod has been successfully created!"
        else:
            print response.text


class PodDelete(command.Command):
    "Handle delete request for pods"

    def get_parser(self, prog_name):
        parser = super(PodDelete, self).get_parser(prog_name)
        parser.add_argument('-name',
                            type=str,
                            required=True,
                            help='Delete pods using name')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        print http_client.delete(PODS_URL + "/" + parsed_args.name)
