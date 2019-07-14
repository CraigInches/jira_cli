'''Jira Specific Classes'''
import json
import oauth2 as oauth
from .conf import Config
from .auth import SignatureMethod_RSA_SHA1, authorize

class JiraIssue:
    '''Define attributes for a Jira Issue'''
    def __init__(self, issue_id):
        self.issue_id = issue_id
        self.description = ''
        self.summary = ''
        self.assignee = ''
        self.creator = ''
        self.comments = []

def fetch_issue(issue_id, instance):
    '''Fetch and present the issue data from JIRA'''
    issue_url = '/rest/api/2/issue/' + issue_id
    resp, content = make_request(issue_url, "GET", instance)
    response = json.loads(content.decode('utf8'))
    print("Issue ID: " + response['id'])
    print("Status: " + response['fields']['status']['name'])
    print("Summary : " + response['fields']['summary'])
    print("Description: " + response['fields']['description'])
    print("Story Points: " + str(response['fields']['customfield_10113']))

def make_request(url, method, instance):
    '''Make a HTTP Request to JIRA Server'''
    print(instance)
    if Config.get_oauth_token(instance) == '':
        oauth_token, oauth_secret = authorize(instance)
        Config.set_oauth_token(instance, oauth_token)
        Config.set_oauth_token(instance, oauth_secret)
    access_token = oauth.Token(Config(instance).oauth_token, Config(instance).oauth_secret)
    consumer = oauth.Consumer(Config(instance).consumer_key, Config(instance).consumer_secret)
    client = oauth.Client(consumer, access_token)
    if Config(instance).ca_cert_file != '':
        client.ca_certs = Config(instance).ca_cert_file
    client.set_signature_method(SignatureMethod_RSA_SHA1())
    resp, content = client.request(Config(instance).baseurl + url, method)
    return resp, content
