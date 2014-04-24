#!/usr/bin/env python
import tornado.ioloop
import tornado.web
import tornado.httpclient
import os
import sys

#Set up the path
sys.path.insert(0, os.path.abspath('..'))

#Import the settings and functions
import settings
import functions


class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.authenticate_request()

    def authenticate_request(self):
        #Ignore any paths in settings.IGNORE_PATHS with an empty response
        if self.request.path in settings.IGNORE_PATHS:
            self.finish()
            return

        #Parse the call out into its separate parts like index / document / call
        parsed_request = functions.parse_request(self.request)

        #Get the policies that apply to the resource of the parsed request
        policies = functions.get_policies_for_resource(
            cluster=parsed_request['cluster'],
            indices=parsed_request['indices'],
            policies=settings.POLICIES
        )

        #Get policies that apply to the current user
        policies = functions.get_policies_for_user(
            user=None,
            policies=policies
        )

        #If there are no policies for this user and resource / return access denied
        if not len(policies):
            self.set_status(403)
            self.finish('Access Denied')
            return

        #Step 4: Validate the policies and see which users have access
        #If there are no matching policies for this user, we deny access
        granted = False
        for policy in policies:
            if policy['user'] in [logged_in_user, 'anonymous', '*']:
                for permission_name in policy['permissions']:
                    permission = settings['PERMISSIONS'][permission_name]
                    if (permission['allow_calls'] == '*' or es_call in permission['allow_calls']) \
                    and (permission['allow_methods'] == '*' or self.request.method in permission['allow_methods']):
                        granted = True
                        print "USER:%s GRANTED WITH: %s" % (policy['user'], permission)
                        break

            if granted:
                break

        if not granted:
            self.set_status(403)
            self.finish('Access Denied')
            print 'DENIED'

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.call_cluster()

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        self.call_cluster()

    @tornado.web.asynchronous
    def head(self, *args, **kwargs):
        self.call_cluster()

    @tornado.web.asynchronous
    def put(self, *args, **kwargs):
        self.call_cluster()

    @tornado.web.asynchronous
    def options(self, *args, **kwargs):
        self.call_cluster()

    def call_cluster(self):
        #Based on: https://github.com/senko/tornado-proxy/blob/master/tornado_proxy/proxy.py
        def handle_response(response):
            if response.error \
                and not isinstance(
                    response.error, tornado.httpclient.HTTPError):
                self.set_status(500)
                self.finish('Internal server error')
            else:
                self.set_status(response.code)
                for header in ('Date', 'Cache-Control',):
                    v = response.headers.get(header)
                    if v:
                        self.set_header(header, v)
                if response.body:
                    self.write(response.body)
                self.finish()

        remote_url = settings['ELASTICSEARCH']['url'] + self.request.path
        if self.request.query:
            remote_url += '?' + self.request.query

        req = tornado.httpclient.HTTPRequest(
            url=remote_url,
            auth_mode=settings['ELASTICSEARCH']['auth_mode'],
            auth_username=settings['ELASTICSEARCH']['auth_username'],
            auth_password=settings['ELASTICSEARCH']['auth_password'],
            method=self.request.method,
            body=self.request.body,
        )
        client = tornado.httpclient.AsyncHTTPClient()
        try:
            client.fetch(req, handle_response)
        except tornado.httpclient.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                handle_response(e.response)
            else:
                self.set_status(500)
                self.write('Internal server error')
                self.finish()


application = tornado.web.Application([
    (r"(.*)", MainHandler),
])

tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

if __name__ == "__main__":
    application.listen(settings.LISTEN_PORT, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
