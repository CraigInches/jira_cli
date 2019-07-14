import base64
import urllib.parse
import oauth2 as oauth
from tlslite.utils import keyfactory
from .conf import Config

class SignatureMethod_RSA_SHA1(oauth.SignatureMethod):
    name = 'RSA-SHA1'

    def signing_base(self, request, consumer, token):
        sig = (
            oauth.escape(request.method),
            oauth.escape(request.normalized_url),
            oauth.escape(request.get_normalized_parameters()),
            )

        key = '%s&' % oauth.escape(consumer.secret)
        if token:
            key += oauth.escape(token.secret)
        raw = '&'.join(sig)
        return key, raw

    def sign(self, request, consumer, token):
        key, raw = self.signing_base(request, consumer, token)
        raw2 = str.encode(raw)
        with open('./keys/jira_privatekey.pem', 'r') as keyfile:
            data = keyfile.read()
        private_key_string = data.strip()

        private_key = keyfactory.parsePrivateKey(private_key_string)
        signature = private_key.hashAndSign(raw2)

        return base64.b64encode(signature)


def authorize(instance):
    '''Performs OAuth authentication with server and returns tokens'''
    consumer = oauth.Consumer(Config.get_consumer_key(instance),
                              Config.get_consumer_secret(instance))
    client = oauth.Client(consumer)
    if Config.get_ca_cert_file(instance) != '':
        client.ca_certs = Config.get_ca_cert_file(instance)
    client.set_signature_method(SignatureMethod_RSA_SHA1())
    resp, content = client.request(Config.get_url(instance) +
                                   Config.get_request_token_url(instance), "POST")
    request_token = dict(urllib.parse.parse_qsl(content))
    print("Go to the following link in your browser:")
    print("%s?oauth_token=%s" % (Config.get_url(instance)+ Config.get_authorize_url(instance),
                                 request_token[b'oauth_token'].decode('utf8')))
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = input('Have you authorized me? (y/n) ')
    token = oauth.Token(request_token[b'oauth_token'],
                        request_token[b'oauth_token_secret'])
    client = oauth.Client(consumer, token)
    if Config.get_ca_cert_file(instance) != '':
        client.ca_certs = Config.get_ca_cert_file(instance)
    client.set_signature_method(SignatureMethod_RSA_SHA1())
    resp, content = client.request(Config.get_url(instance) +
                                   Config.get_access_token_url(instance), "POST")
    access_token = dict(urllib.parse.parse_qsl(content))
    print("You may now access protected resources")
    oauth_token = access_token[b'oauth_token'].decode('utf8')
    auth_secret = access_token[b'oauth_token_secret'].decode('utf8')
    return oauth_token, auth_secret
