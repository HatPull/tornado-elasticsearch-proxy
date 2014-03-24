#!/usr/bin/env python
import tornado.ioloop
import tornado.web
import tornado.httpclient
import os, sys

#Set up the path
sys.path.insert(0, os.path.abspath(".."))

#Import the settings
import settings

class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.authenticate_request()

    def authenticate_request(self):

        #Cut the first slash "/" off the path and split the rest
        path_parts = self.request.path[1:].split('/')
        es_call = None
        indices = []
        policies = []

        #Step 1: Which Elastic Search call is the request making? (meta calls don't count)
        meta_calls = ['_all', '_primary', '_local']
        for part in path_parts:
            if part.startswith('_') and part not in meta_calls:
                es_call = part
                break
    
        if es_call is None:
             #We add the two calls _home, and _document that don't exist in the real elasticsearch path
             #assuming home if the path is empty or one char and _document if the path is longer
             if self.request.path == '/':
                 es_call = '_home'
             else:
                 es_call = '_document'

        print
        print 'REQUEST: %s' % self.request.path
        print 'PATH PARTS: %s' % path_parts
        print 'ES CALL: %s' % es_call

        #Step 2: Is this a cluster call, or a call to indices?
        if self.request.path == '/' or path_parts[0].startswith('_') and path_parts[0] != '_all':
            cluster_call = True
        else:
            cluster_call = False
            #This is a call to an index or multiple indices - so we get those
            request_indices = path_parts[0].split(',')
           
          
        #Step 3: Find matching policies  
        #Step 3, Part 1: Find policies that match the scope of the request
        scope_available_policies = [] 
        for policy in settings.POLICIES:
            if '*' in policy.scope:
                scope_available_policies.append(policy) 
            elif cluster_call and 'cluster' in policy.scope: 
                scope_available_policies.append(policy) 
            else:
                for request_index in request_indices:
                    if 'index:%s' % request_index in policy.scope:
                        scope_available_policies.append(policy) 
            
        #Step 3, Part 2: From the scope available policies, find policies that can be used by 
        #this individual user
        user_available_policies = [] 
        for policy in scope_available_policies:
            if '*' in policy.users:
                user_available_policies.append(policy) 
        

        print 'POLICIES: %s' % policies
        
        if not len(user_available_policies): 
            self.set_status(403)
            self.finish('Access Denied')

        #Step 4: Validate the policies and see which users have access
        #If there are no matching policies for this user, we deny access        
        granted = False
        for policy in policies:
            if policy['user'] in [logged_in_user, 'anonymous', '*']:
                for permission_name in policy['permissions']:
                    permission = config['permissions'][permission_name]
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
        print

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
    def head(self, *args, **kwargs):
        self.call_cluster()

    @tornado.web.asynchronous
    def options(self, *args, **kwargs):
        self.call_cluster()

    def call_cluster(self):
        #Based on: https://github.com/senko/tornado-proxy/blob/master/tornado_proxy/proxy.py
        def handle_response(response):
            if response.error and not isinstance(response.error,
                    tornado.httpclient.HTTPError):
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

        remote_url = config['cluster']['url'] + self.request.path 
        if self.request.query:
            remote_url += '?' + self.request.query
        
        req = tornado.httpclient.HTTPRequest(
            url=remote_url,
            auth_mode=config['cluster']['auth_mode'],
            auth_username=config['cluster']['auth_username'],
            auth_password=config['cluster']['auth_password'],
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
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
