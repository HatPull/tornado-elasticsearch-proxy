==================
Proxy Request Flow
==================

User comes to the proxy.

User can be anonymous

Postgres will have db of record, but will push to an elastic search users index.

Syncing will use elastic utils 

This users index will be available to Tornado.

For now user index will be mixed with tornado's cluster that it is the proxy server to.

in future, separate cluster, not accessible to client.




users index has fields: 
	users (string)
	indices (string)
	cluster  (bool)
	permissions