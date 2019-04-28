''' Main functions for jira_cli app '''
import os
import argparse
import json
from configparser import ConfigParser
from pathlib import Path
import oauth2 as oauth
from .jira import JiraInstance
from .auth import authorize, SignatureMethod_RSA_SHA1


CONFIG_FILE = str(Path.home()) + '/.config/jira_cli'
JIRA = JiraInstance("jira")

def gen_config():
    '''Generate a template config for User'''
    config = ConfigParser()
    config['JIRA'] = {
        'BaseUrl': 'https://jira.example.com',
        'ConsumerKey': '',
        'ConsumerSecret': '',
        'RequestTokenUrl': '/plugins/servlet/oauth/request-token',
        'AccessTokenUrl':  '/plugins/servlet/oauth/access-token',
        'AuthorizeUrl': '/plugins/servlet/oauth/authorize',
        'CACertFile': '',
        'OAuthToken': '',
        'OAuthSecret': '',
    }
    with open(CONFIG_FILE, 'x') as file:
        config.write(file)

def read_config():
    '''Read Config and parse into the Jira Instance Object'''
    config = ConfigParser()
    config.read(CONFIG_FILE)
    JIRA.base_url = config['JIRA']['baseurl']
    JIRA.consumer_key = config['JIRA']['ConsumerKey']
    JIRA.consumer_secret = config['JIRA']['ConsumerSecret']
    JIRA.request_token_url = config['JIRA']['RequestTokenUrl']
    JIRA.access_token_url = config['JIRA']['AccessTokenUrl']
    JIRA.authorize_url = config['JIRA']['AuthorizeUrl']
    JIRA.ca_cert_file = config['JIRA']['CACertFile']
    JIRA.oauth_token = config['JIRA']['OAuthToken']
    JIRA.oauth_secret = config['JIRA']['OAuthSecret']
    if JIRA.oauth_token == '':
        print("No OAuth Token Do you want to auth now?")
        response = input("Y/N")
        if response.upper() == "Y":
            authorize(JIRA)
            config['JIRA']['OAuthToken'] = JIRA.oauth_token
            config['JIRA']['OAuthSecret'] = JIRA.oauth_secret
            with open(CONFIG_FILE, 'w') as file:
                config.write(file)
                print("Tokens stored in config file")
    return


def fetch_issue(issue_id):
    '''Fetch and present the issue data from JIRA'''
    issue_url = '/rest/api/2/issue/' + issue_id
    resp, content = make_request(issue_url, "GET")
    response = json.loads(content.decode('utf8'))
    print("Issue ID: " + response['id'])
    print("Status: " + response['fields']['status']['name'])
    print("Summary : " + response['fields']['summary'])
    print("Description: " + response['fields']['description'])
    print("Story Points: " + str(response['fields']['customfield_10113']))



def make_request(url, method):
    '''Make a HTTP Request to JIRA Server'''
    access_token = oauth.Token(JIRA.oauth_token, JIRA.oauth_secret)
    consumer = oauth.Consumer(JIRA.consumer_key, JIRA.consumer_secret)
    client = oauth.Client(consumer, access_token)
    if JIRA.ca_cert_file != '':
        client.ca_certs = JIRA.ca_cert_file
    client.set_signature_method(SignatureMethod_RSA_SHA1())
    resp, content = client.request(JIRA.base_url + url, method)
    return resp, content
    #resp, content = client.request(JIRA.base_url + "/rest/api/2/filter/17575", "GET")

def main():
    '''Core Functions'''
    parser = argparse.ArgumentParser(description="CLI to JIRA")
    commands_parser = parser.add_subparsers(title="Available Commands", dest='command')
    issue_parser = commands_parser.add_parser("issue")
    issue_parser.add_argument("issue_id", help="Issue identifier")
    search_parser = commands_parser.add_parser("search")
    search_parser.add_argument("search_term", help="Search Term")
    args = parser.parse_args()
    if os.path.exists(CONFIG_FILE):
        read_config()
        if args.command == "issue":
            print("issue is: " + args.issue_id)
            fetch_issue(args.issue_id)
        elif args.command == "search":
            print("you searched for: " + args.search_term)
    else:
        print("Config File does not exist")
        print("do you want to create a template ~/.config/jira_cli")
        answer = input("Y/N")
        if answer.upper() == "Y":
            print("You Accepted")
            gen_config()
            print("Please edit " + CONFIG_FILE + "as needed")
        else:
            print("Goodbye!")


if __name__ == '__main__.py':
    main()
