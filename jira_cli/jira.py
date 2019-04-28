'''Jira Specific Classes'''

class JiraInstance:
    '''Defines the attrbutes of a Jira instace for use'''
    def __init__(self, name):
        self.name = name
        self.base_url = ''
        self.consumer_key = ''
        self.consumer_secret = ''
        self.request_token_url = ''
        self.access_token_url = ''
        self.authorize_url = ''
        self.ca_cert_file = ''
        self.oauth_token = ''
        self.oauth_secret = ''

class JiraIssue:
    '''Define attributes for a Jira Issue'''
    def __init__(self, issue_id):
        self.issue_id = issue_id
        self.description = ''
        self.summary = ''
        self.assignee = ''
        self.creator = ''
        self.comments = []
