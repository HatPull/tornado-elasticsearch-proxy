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

from .functions import (
    parse_request,
    get_policies_for_resource,
    get_policies_for_user,
    authenticate_call_and_method
)


class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.authenticate_request()

    def authenticate_request(self):
        # Ignore any paths in settings.IGNORE_PATHS with an empty response
        if self.request.path in settings.IGNORE_PATHS:
            self.finish()
            return

        # Parse the call into its separate parts e.g. index / document / call
        parsed_request = parse_request(self.request)

        # Get policies that apply to the current user
        user_policies = get_policies_for_user(
            user=None,
            policies=settings.POLICIES
        )

        # Refine user_policies by finding the subset of policies
        # that apply just to the resources of the parsed request
        policies = get_policies_for_resource(
            cluster=parsed_request['cluster'],
            indices=parsed_request['indices'],
            policies=user_policies
        )

        # Can the user do what they are requesting,
        # given the policies that have been found?
        # If not, deny access.
        granted = authenticate_call_and_method(
            policies,
            parsed_request['call'],
            self.request.method
        )

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
        # Based on:
        # https:// \
        # github.com/senko/tornado-proxy/blob/master/tornado_proxy/proxy.py
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

tornado.httpclient.AsyncHTTPClient.configure(
    "tornado.curl_httpclient.CurlAsyncHTTPClient"
)

if __name__ == "__main__":
    application.listen(settings.LISTEN_PORT, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
