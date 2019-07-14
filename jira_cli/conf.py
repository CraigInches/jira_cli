''' config options for app '''
from configparser import ConfigParser
from pathlib import Path


CONFIG_FILE = str(Path.home()) + '/.config/jira_cli'

def get_file():
    return CONFIG_FILE

def gen_config(instance):
    '''Generate a template config for User'''
    config = ConfigParser()
    config[instance] = {
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

class Config:
    '''Read Config and parse into the Jira Instance Object'''
    def __init__(self, instance):
        config = ConfigParser()
        config.read(CONFIG_FILE)
        self.baseurl = config[instance]['baseurl']
        self.consumer_key = config[instance]['ConsumerKey']
        self.consumer_secret = config[instance]['ConsumerSecret']
        self.request_token_url = config[instance]['RequestTokenUrl']
        self.access_token_url = config[instance]['AccessTokenUrl']
        self.authorize_url = config[instance]['AuthorizeUrl']
        self.ca_cert_file = config[instance]['CACertFile']
        self.oauth_token = config[instance]['OAuthToken']
        self.oauth_secret = config[instance]['OAuthSecret']

    @classmethod
    def write_config(cls, instance):
        conf = ConfigParser()
        conf[instance] = {}
        conf[instance]['baseurl'] = cls(instance).get_url
        conf[instance]['ConsumerKey'] = cls(instance).get_consumer_key
        conf[instance]['ConsumerSecret'] = cls(instance).get_consumer_secret
        conf[instance]['RequestTokenUrl'] = cls(instance).get_request_token_url
        conf[instance]['AccessTokenUrl'] = cls(instance).get_access_token_url
        conf[instance]['AuthorizedUrl'] = cls(instance).get_authorize_url
        conf[instance]['CACertFile'] = cls(instance).get_ca_cert_file
        conf[instance]['OAuthToken'] = cls(instance).get_oauth_token
        conf[instance]['OAuthSecret'] = cls(instance).get_oauth_secret
        with open(CONFIG_FILE, 'x') as file:
            conf.write(file)

    @classmethod
    def get_url(cls, instance):
        return cls(instance).baseurl

    @classmethod
    def get_consumer_key(cls, instance):
        return cls(instance).consumer_key

    @classmethod
    def get_consumer_secret(cls, instance):
        return cls(instance).consumer_secret

    @classmethod
    def get_request_token_url(cls, instance):
        return cls(instance).request_token_url

    @classmethod
    def get_access_token_url(cls, instance):
        return cls(instance).access_token_url

    @classmethod
    def get_authorize_url(cls, instance):
        return cls(instance).authorize_url

    @classmethod
    def get_ca_cert_file(cls, instance):
        return cls(instance).ca_cert_file

    @classmethod
    def get_oauth_token(cls, instance):
        return cls(instance).oauth_token

    @classmethod
    def get_oauth_secret(cls, instance):
        return cls(instance).oauth_secret

    @classmethod
    def set_oauth_token(cls, instance, token):
        return cls(instance).oauth_token

    @classmethod
    def set_oauth_secret(cls, instance, secret):
        return cls(instance).oauth_secret
