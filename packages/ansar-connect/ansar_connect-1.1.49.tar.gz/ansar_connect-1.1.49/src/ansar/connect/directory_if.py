# Author: Scott Woods <scott.18.ansar@gmail.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
__docformat__ = 'restructuredtext'

import ansar.create as ar
from .socketry import *

__all__ = [
	'ScopeOfService',
	'Published',
	'NotPublished',
	'Subscribed',
	'Available',
	'NotAvailable',
	'Delivered',
	'NotDelivered',
	'Clear',
	'Cleared',
	'Dropped',
	'NetworkEnquiry',
	'NetworkConnect',
	'DirectoryRoute',
	'DirectoryScope',
	'DirectoryAncestry',
]

# Build the local published/subscribed objects.
#
ScopeOfService = ar.Enumeration(PROCESS=1, GROUP=2, HOST=3, LAN=4, WAN=5)

#
#
class Published(object):
	"""Session notification, server presence established.

	:param requested_name: name the server is known by
	:type requested_name: str
	:param requested_scope: highest level that name has been registered 
	:type requested_scope: enumeration
	:param listening_ipp: network presence created on behalf
	:type listening_ipp: HostPort
	:param published_at: moment of publication
	:type published_at: datetime
	"""
	def __init__(self, requested_name=None, requested_scope=ScopeOfService.WAN, listening_ipp=None, published_at=None):
		self.requested_name = requested_name
		self.requested_scope = requested_scope
		self.listening_ipp = listening_ipp or HostPort()
		self.published_at = published_at

class NotPublished(ar.Faulted):
	"""Session notification, server presence not established.

	:param requested_name: intended name of the server
	:type requested_name: str
	:param reason: short description
	:type reason: str
	"""
	def __init__(self, requested_name=None, reason=None):
		ar.Faulted.__init__(self, f'cannot publish "{requested_name}"', reason)
		self.requested_name = requested_name
		self.reason = reason

class Subscribed(object):
	"""Session notification, client search established.

	:param requested_search: name the client is looking for (regular expression)
	:type requested_search: str
	:param requested_scope: highest level that search has been registered 
	:type requested_scope: enumeration
	:param subscribed_at: moment of subscription
	:type subscribed_at: datetime
	"""
	def __init__(self, requested_search=None, requested_scope=ScopeOfService.WAN, subscribed_at=None):
		self.requested_search = requested_search
		self.requested_scope = requested_scope
		self.subscribed_at = subscribed_at

#
#
class Available(object):
	"""Session notification, transport to server established.

	:param matched_search: name the client was looking for (regular expression)
	:type matched_search: str
	:param matched_name: name the server is known by
	:type matched_name: str
	:param matched_scope: level at which match was made
	:type matched_scope: enumeration
	:param opened_at: start of messaging
	:type opened_at: datetime
	:param route_key: unique id for this session
	:type route_key: str
	:param agent_address: internal pub-sub controller
	:type agent_address: async address
	"""
	def __init__(self, subscriber_address=None, matched_search=None, matched_name=None, matched_scope=None, opened_at=None, route_key=None, agent_address=None):
		self.subscriber_address = subscriber_address
		self.matched_search = matched_search
		self.matched_name = matched_name
		self.matched_scope = matched_scope
		self.opened_at = opened_at
		self.route_key = route_key
		self.agent_address = agent_address

class NotAvailable(ar.Faulted):
	"""Session notification, transport to server not established.

	:param matched_search: name the client was looking for (regular expression)
	:type matched_search: str
	:param matched_name: name the server is known by
	:type matched_name: str
	:param matched_scope: level at which match was made
	:type matched_scope: enumeration
	:param route_key: unique id for this session
	:type route_key: str
	:param reason: why the session could not proceed
	:type reason: str
	:param agent_address: internal pub-sub controller
	:type agent_address: async address
	"""
	def __init__(self, matched_search=None, matched_name=None, matched_scope=None, route_key=None, reason=None, agent_address=None):
		ar.Faulted.__init__(self, 'no subsciber peer', reason)
		self.matched_search = matched_search
		self.matched_name = matched_name
		self.matched_scope = matched_scope
		self.route_key = route_key
		self.reason = reason
		self.agent_address = agent_address

class Delivered(object):
	"""Session notification, transport to client established.

	:param matched_search: name the client was looking for (regular expression)
	:type matched_search: str
	:param matched_name: name the server is known by
	:type matched_name: str
	:param matched_scope: level at which match was made
	:type matched_scope: enumeration
	:param opened_at: start of messaging
	:type opened_at: datetime
	:param route_key: unique id for this session
	:type route_key: str
	:param agent_address: internal pub-sub controller
	:type agent_address: async address
	"""
	def __init__(self, publisher_address=None, matched_search=None, matched_name=None, matched_scope=None, opened_at=None, route_key=None, agent_address=None):
		self.publisher_address = publisher_address
		self.matched_search = matched_search
		self.matched_name = matched_name
		self.matched_scope = matched_scope
		self.opened_at = opened_at
		self.route_key = route_key
		self.agent_address = agent_address

class NotDelivered(ar.Faulted):
	"""Session notification, transport to client not established.

	:param matched_search: name the client was looking for (regular expression)
	:type matched_search: str
	:param matched_name: name the server is known by
	:type matched_name: str
	:param matched_scope: level at which match was made
	:type matched_scope: enumeration
	:param route_key: unique id for this session
	:type route_key: str
	:param reason: why the session could not proceed
	:type reason: str
	:param agent_address: internal pub-sub controller
	:type agent_address: async address
	"""
	def __init__(self, matched_search=None, matched_name=None, matched_scope=None, route_key=None, reason=None, agent_address=None):
		ar.Faulted.__init__(self, 'no publisher peer', reason)
		self.matched_search = matched_search
		self.matched_name = matched_name
		self.matched_scope = matched_scope
		self.route_key = route_key
		self.reason = reason
		self.agent_address = agent_address

class Clear(object):
	def __init__(self, session=None, value=None):
		self.session = session
		self.value = value

class Cleared(object):
	"""Session notification, shutdown of transport by local end.

	:param matched_search: name the client was looking for (regular expression)
	:type matched_search: str
	:param matched_name: name the server is known by
	:type matched_name: str
	:param matched_scope: level at which match was made
	:type matched_scope: enumeration
	:param route_key: unique id for this session
	:type route_key: str
	:param reason: why the session could not proceed
	:type reason: str
	:param value: result of session
	:type value: any
	"""
	def __init__(self, matched_search=None, matched_name=None, matched_scope=None, route_key=None, reason=None, value=None):
		ar.Faulted.__init__(self, 'peer cleared', reason)
		self.matched_search = matched_search
		self.matched_name = matched_name
		self.matched_scope = matched_scope
		self.route_key = route_key
		self.reason = reason
		self.value = value

class Dropped(ar.Faulted):
	"""Session notification, shutdown of transport by remote end.

	:param matched_search: name the client was looking for (regular expression)
	:type matched_search: str
	:param matched_name: name the server is known by
	:type matched_name: str
	:param matched_scope: level at which match was made
	:type matched_scope: enumeration
	:param route_key: unique id for this session
	:type route_key: str
	:param reason: why the session could not proceed
	:type reason: str
	"""
	def __init__(self, matched_search=None, matched_name=None, matched_scope=None, route_key=None, reason=None):
		ar.Faulted.__init__(self, 'peer dropped', reason)
		self.matched_search = matched_search
		self.matched_name = matched_name
		self.matched_scope = matched_scope
		self.route_key = route_key
		self.reason = reason

ENDING_SCHEMA = {
	'publisher_address': ar.Address(),
	'subscriber_address': ar.Address(),
	'matched_search': ar.Unicode(),
	'matched_name': ar.Unicode(),
	'matched_scope': ScopeOfService,
	'opened_at': ar.WorldTime(),
	'route_key': ar.Unicode(),
	'session': ar.Any,
	'value': ar.Any,
	'reason': ar.Unicode(),
	'condition': ar.Unicode(),
	'explanation': ar.Unicode(),
	'error_text': ar.Unicode(),
	'error_code': ar.Integer8(),
	'exit_code': ar.Integer8(),
}

ar.bind(Clear, object_schema=ENDING_SCHEMA, copy_before_sending=False)
ar.bind(Cleared, object_schema=ENDING_SCHEMA, copy_before_sending=False)
ar.bind(Dropped, object_schema=ENDING_SCHEMA, copy_before_sending=False)

SHARED_SCHEMA = {
	'requested_search': ar.Unicode(),
	'requested_name': ar.Unicode(),
	'requested_scope': ScopeOfService,
	'listening_ipp': ar.UserDefined(HostPort),
	'agent_address': ar.Address(),
	'published_at': ar.WorldTime(),
	'subscribed_at': ar.WorldTime(),
}

SHARED_SCHEMA.update(ENDING_SCHEMA)

ar.bind(Subscribed, object_schema=SHARED_SCHEMA)
ar.bind(Published, object_schema=SHARED_SCHEMA)
ar.bind(Available, object_schema=SHARED_SCHEMA)
ar.bind(NotAvailable, object_schema=SHARED_SCHEMA)
ar.bind(Delivered, object_schema=SHARED_SCHEMA)
ar.bind(NotDelivered, object_schema=SHARED_SCHEMA)

# matched[route_key] = a (address of ServiceRoute)
# and
# route_key added to each find and listing set
# self.directory[service_name] = [message, set()]
# self.find[k] = [message, set(), dfa]
# where k =
# f'{subscriber_address}/{requested_search}'
class DirectoryRoute(object):
	def __init__(self, search_or_listing=None, agent_address=None, route_key=None):
		self.search_or_listing = search_or_listing
		self.agent_address = agent_address
		self.route_key = route_key or ar.default_set()

DIRECTORY_ROUTE_SCHEMA = {
	'search_or_listing': ar.Unicode(),
	'agent_address': ar.Address(),
	'route_key': ar.SetOf(ar.Unicode()),
}

ar.bind(DirectoryRoute, object_schema=DIRECTORY_ROUTE_SCHEMA)

class DirectoryScope(object):
	def __init__(self, scope=None, connect_above=None, started=None, connected=None, not_connected=None,
			listing=None, find=None, accepted=None):
		self.scope = scope
		self.connect_above = connect_above or HostPort()
		self.started = started
		self.connected = connected
		self.not_connected = not_connected
		self.listing = listing or ar.default_vector()
		self.find = find or ar.default_vector()
		self.accepted = accepted or ar.default_vector()

DIRECTORY_SCOPE_SCHEMA = {
	'scope' : ScopeOfService,
	'connect_above': ar.Any(),
	'started': ar.WorldTime(),
	'connected': ar.WorldTime(),
	'not_connected': ar.Unicode(),
	'listing': ar.VectorOf(ar.UserDefined(DirectoryRoute)),
	'find': ar.VectorOf(ar.UserDefined(DirectoryRoute)),
	'accepted': ar.VectorOf(ar.UserDefined(HostPort)),
}

ar.bind(DirectoryScope, object_schema=DIRECTORY_SCOPE_SCHEMA)

#
#
class NetworkEnquiry(object):
	def __init__(self, lineage=None):
		self.lineage = lineage or ar.default_vector()

NETWORK_ENQUIRY_SCHEMA = {
	'lineage': ar.VectorOf(DirectoryScope),
}

ar.bind(NetworkEnquiry, object_schema=NETWORK_ENQUIRY_SCHEMA)

#
#
class NetworkConnect(object):
	def __init__(self, scope=None, connect_above=None):
		self.scope = scope
		self.connect_above = connect_above

NETWORK_CONNECT_SCHEMA = {
	'scope': ScopeOfService,
	'connect_above': ar.Any(),
}

ar.bind(NetworkConnect, object_schema=NETWORK_CONNECT_SCHEMA)

#
#
class DirectoryAncestry(object):
	def __init__(self, lineage=None):
		self.lineage = lineage or ar.default_vector()

DIRECTORY_ANCESTRY_SCHEMA = {
	'lineage': ar.VectorOf(DirectoryScope),
}

ar.bind(DirectoryAncestry, object_schema=DIRECTORY_ANCESTRY_SCHEMA)
