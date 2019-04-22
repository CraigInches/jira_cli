''' Main functions for jira_cli app '''
import os
from configparser import ConfigParser
from pathlib import Path
import oauth2 as oauth
from .jira import JiraInstance
from .auth import authorize, SignatureMethod_RSA_SHA1


CONFIG_FILE = str(Path.home()) + '/.config/jira_cli'

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
    jira = JiraInstance("jira")
    config = ConfigParser()
    config.read(CONFIG_FILE)
    jira.base_url = config['JIRA']['BaseUrl']
    jira.consumer_key = config['JIRA']['ConsumerKey']
    jira.consumer_secret = config['JIRA']['ConsumerSecret']
    jira.request_token_url = config['JIRA']['RequestTokenUrl']
    jira.access_token_url = config['JIRA']['AccessTokenUrl']
    jira.authorize_url = config['JIRA']['AuthorizeUrl']
    jira.ca_cert_file = config['JIRA']['CACertFile']
    jira.oauth_token = config['JIRA']['OAuthToken']
    jira.oauth_secret = config['JIRA']['OAuthSecret']
    if jira.oauth_token == '':
        print("No OAuth Token Do you want to auth now?")
        response = input("Y/N")
        if response.upper() == "Y":
            authorize(jira)
            config['JIRA']['OAuthToken'] = jira.oauth_token
            config['JIRA']['OAuthSecret'] = jira.oauth_secret
            with open(CONFIG_FILE, 'w') as file:
                config.write(file)
                print("Tokens stored in config file")
    return jira

def main():
    '''Core Functions'''
    if os.path.exists(CONFIG_FILE):
        jira = read_config()
        access_token = oauth.Token(jira.oauth_token, jira.oauth_secret)
        consumer = oauth.Consumer(jira.consumer_key, jira.consumer_secret)
        client = oauth.Client(consumer, access_token)
        if jira.ca_cert_file != '':
            client.ca_certs = jira.ca_cert_file
        client.set_signature_method(SignatureMethod_RSA_SHA1())
        resp, content = client.request(jira.base_url + "/rest/api/2/filter/17575", "GET")
        print(content)
        print(resp)

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
