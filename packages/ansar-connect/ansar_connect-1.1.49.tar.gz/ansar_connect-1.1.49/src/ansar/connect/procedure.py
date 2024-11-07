# Author: Scott Woods <scott.18.ansar@gmail.com>
# MIT License
#
# Copyright (c) 2022, 2023 Scott Woods
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

""".

.
"""
__docformat__ = 'restructuredtext'

__all__ = [
	'NetworkSettings',
	'PingSettings',
	'CloudSettings',
	'procedure_network',
	'procedure_ping',
	'procedure_signup',
	'procedure_login',
	'procedure_account',
	'procedure_directory',
]

import os
import getpass
import uuid
import ansar.connect as ar
from ansar.encode.args import QUOTED_TYPE, SHIPMENT_WITH_QUOTES, SHIPMENT_WITHOUT_QUOTES
from ansar.create.procedure import DEFAULT_HOME, DEFAULT_GROUP, HOME, GROUP
from ansar.create.procedure import open_home, role_status
from ansar.create.object import decoration_store, object_settings
from ansar.connect.group_if import GroupSettings
from ansar.connect.standard import *
from .foh_if import *
from .wan import *
from .product import *
from .directory_if import *

DEFAULT_ACCOUNT_ACTION = 'show'

# Per-command arguments as required.
# e.g. command-line parameters specific to create.
class NetworkSettings(object):
	def __init__(self, group_name=None, home_path=None,
			connect_scope=None, to_scope=None,
			product_name=None, product_instance=None,
			encrypted=False,
			custom_host=None, custom_port=None,
			reserved=False,
			connect_file=None, connect_disable=False,
			published_services=False, subscribed_searches=False, routed_matches=False, accepted_processes=False,
			host_and_port=False, start_time=False):
		self.group_name = group_name
		self.home_path = home_path
		self.connect_scope = connect_scope
		self.to_scope = to_scope
		self.product_name = product_name
		self.product_instance = product_instance
		self.encrypted = encrypted
		self.custom_host = custom_host
		self.custom_port = custom_port
		self.reserved = reserved
		self.connect_file = connect_file
		self.connect_disable = connect_disable
		self.published_services = published_services
		self.subscribed_searches = subscribed_searches
		self.routed_matches = routed_matches
		self.accepted_processes = accepted_processes
		self.host_and_port = host_and_port
		self.start_time = start_time

NETWORK_SETTINGS_SCHEMA = {
	'group_name': ar.Unicode(),
	'home_path': ar.Unicode(),
	'connect_scope': ScopeOfService,
	'to_scope': ScopeOfService,
	'product_name': ar.Unicode(),
	'product_instance': InstanceOfProduct,
	'encrypted': ar.Boolean(),
	'custom_host': ar.Unicode(),
	'custom_port': ar.Integer8(),
	'reserved': ar.Boolean(),
	'connect_file': ar.Unicode(),
	'connect_disable': ar.Boolean(),
	'published_services': ar.Boolean(),
	'subscribed_searches': ar.Boolean(),
	'routed_matches': ar.Boolean(),
	'accepted_processes': ar.Boolean(),
	'host_and_port': ar.Boolean(),
	'start_time': ar.Boolean(),
}

ar.bind(NetworkSettings, object_schema=NETWORK_SETTINGS_SCHEMA)

#
#
def lfa_text(d):
	f, l, a = len(d.listing), len(d.find), len(d.accepted)
	s = f'{f}/{l}/{a}'
	return s

def output_ancestry(self, ancestry, network):
	for d in reversed(ancestry.lineage):

		scope = ScopeOfService.to_name(d.scope) if d.scope else '?'
		if isinstance(d.connect_above, ar.HostPort):
			connecting_ipp = d.connect_above
			display_name = str(connecting_ipp)
		elif isinstance(d.connect_above, ProductAccess):
			connecting_ipp = d.connect_above.access_ipp
			e = InstanceOfProduct.to_name(d.connect_above.product_instance)
			display_name = f'{d.connect_above.product_name}/{e}'
		elif isinstance(d.connect_above, WideAreaAccess):
			connecting_ipp = d.connect_above.access_ipp
			display_name = f'{d.connect_above}'
		else:
			continue

		if connecting_ipp.host is None:
			continue

		started = ar.world_to_text(d.started) if d.started else '-'
		connected = ar.world_to_text(d.connected) if d.connected else '-'
		lfa = lfa_text(d)

		note = []
		if network.host_and_port:
			note.append(str(connecting_ipp))
		if network.start_time:
			note.append(started)

		if connecting_ipp.host is None:
			note.append('DISABLED')
		elif d.not_connected:
			note.append(d.not_connected)

		key_name = {k: r.search_or_listing for r in d.listing for k in r.route_key}
		if note:
			s = ', '.join(note)
			ar.output_line(f'+ {scope} {display_name} ({s})')
		else:
			ar.output_line(f'+ {scope} {display_name}')
		if network.published_services:
			ar.output_line(f'+ Published services ({len(d.listing)})', tab=1)
			for r in d.listing:
				ar.output_line(f'+ {r.search_or_listing} ({len(r.route_key)})', tab=2)
		if network.subscribed_searches:
			ar.output_line(f'+ Subscribed searches ({len(d.find)})', tab=1)
			for r in d.find:
				ar.output_line(f'+ {r.search_or_listing} ({len(r.route_key)})', tab=2)
				if network.routed_matches:
					for k in r.route_key:
						ar.output_line(f'+ "{key_name[k]}"', tab=3)
		if network.accepted_processes:
			ar.output_line(f'+ Accepted processes ({len(d.accepted)})', tab=1)
			for a in d.accepted:
				ar.output_line(f'+ {a}', tab=2)

def scope_host(scope):
	if scope == ar.ScopeOfService.HOST:
		return ANSAR_LOCAL_HOST
	elif scope == ar.ScopeOfService.LAN:
		return ANSAR_LAN_HOST
	return None

def procedure_network(self, network, group, home):
	group = ar.word_argument_2(group, network.group_name, DEFAULT_GROUP, GROUP)
	home = ar.word_argument_2(home, network.home_path, DEFAULT_HOME, HOME)

	if '.' in group:
		e = ar.Rejected(group_name=(group, f'no-dots name'))
		raise ar.Incomplete(e)
	group_role = f'group.{group}'

	hb = open_home(home)

	# if not hb.role_exists(group_role):
	#	e = ar.Failed(group_exists=(f'group "{group}" not found', None))
	#	raise ar.Incomplete(e)
	# TBD - auto-create or not.
	settings = GroupSettings()
	hr = hb.open_role(group_role, settings, None, ar.NodeProperties(executable='ansar-group'))

	_, running = role_status(self, hb, [group_role])
	if running:
		e = ar.Failed(group_running=(f'group "{group}" is already running', None))
		raise ar.Incomplete(e)

	settings = hr.role_settings[2]				# From the group.
	connect_above = settings.connect_above
	accept_below = ar.LocalPort(0)				# Grab an ephemeral for consistency.

	a = self.create(ar.ServiceDirectory, ar.ScopeOfService.GROUP, connect_above, accept_below)
	self.directory = a

	try:
		# Directory responds with a HostPort.
		m = self.select(ar.HostPort, ar.Stop)
		if isinstance(m, ar.HostPort):
			connect_above = m
	
		# Wait for a grace period.
		self.start(ar.T2, seconds=1.5)
		self.select(ar.T2, ar.Stop)

		# Look for expression of connect or default to scan.
		if network.connect_scope and network.to_scope:					# ProductAccess or HostPort
			connect_scope = network.connect_scope
			to_scope = network.to_scope
			if network.product_name and network.product_instance:		# ProductAccess
				shared_host = network.custom_host or scope_host(to_scope)
				shared_port = network.custom_port or ANSAR_SHARED_PORT
				access_ipp = ar.HostPort(shared_host, shared_port)
				connect_above= ProductAccess(access_ipp=access_ipp,
					encrypted=network.encrypted,
					product_name=network.product_name,
					product_instance=network.product_instance)
			elif network.product_name or network.product_instance:		# Error
				e = ar.Faulted('need both product name and product instance')
				raise ar.Incomplete(e)
			elif network.reserved:										# Reserved space.
				reserved_host = network.custom_host or scope_host(to_scope)
				reserved_port = network.custom_port or ANSAR_RESERVED_PORT
				connect_above = ar.HostPort(reserved_host, reserved_port)
			else:														# HostPort for connect_scope -> to_scope
				dedicated_host = network.custom_host or scope_host(to_scope)
				dedicated_port = network.custom_port or ANSAR_DEDICATED_PORT
				connect_above = ar.HostPort(dedicated_host, dedicated_port)

		elif network.connect_scope and network.connect_file:			# Explicit.
			connect_file = network.connect_file
			try:
				f = ar.File(connect_file, ar.Any(), decorate_names=False)
				connect_above, _ = f.recover()
			except (ar.FileFailure, ar.CodecError) as e:
				s = str(e)
				f = ar.Failed(connect_file=(s, None))
				self.complete(f)
			
		elif network.connect_scope and network.connect_disable:			# Explicit.
			connect_above = ar.HostPort()

		elif network.connect_scope or network.to_scope:					# Error.
			e = ar.Faulted('need both ends to make a connection', 'use --connect-scope and --to-scope (or --connect-scope and --connect-file)')
			raise ar.Incomplete(e)

		else:	# Scan.
			s = ar.DirectoryScope(scope=GROUP, connect_above=connect_above,
				started=ar.world_now(),
				connected=None)
			e = ar.NetworkEnquiry(lineage=[s])
			self.send(e, self.directory)

			m = self.select(ar.DirectoryAncestry, ar.Stop)
			if isinstance(m, DirectoryAncestry):
				output_ancestry(self, m, network)
				return None
			return None

		if network.to_scope and network.to_scope <= network.connect_scope:
			e = ar.Faulted('connection is upside down', 'target scope must be higher than the source scope')
			raise ar.Incomplete(e)

		a = ar.NetworkConnect(scope=network.connect_scope, connect_above=connect_above)
		self.send(a, self.directory)

		m = self.select(ar.Anything, ar.Ack, ar.Faulted, ar.Stop)
		if isinstance(m, ar.Anything):		# Group change.
			settings = hr.role_settings[2]
			settings.connect_above = m.thing
			try:
				decoration_store(hr.role_settings, settings)
			except (ar.FileFailure, ar.CodecFailed) as e:
				self.reply(ar.Failed(group_connect=(e, None)))
			self.reply(ar.Ack())
		elif isinstance(m, ar.Ack):			# Didnt involve group change.
			return None
		elif isinstance(m, ar.Faulted):		# Failure in the hierarchy.
			return m
		else:
			return None
		# Now the response to the actual
		# NetworkConnect request.
		m = self.select(ar.Ack, ar.Stop)

	finally:
		self.send(ar.Stop(), self.directory)
		self.select(ar.Completed, ar.Stop)

	return None

class PingSettings(object):
	def __init__(self, service_name=None, group_name=None, home_path=None, ping_count=None):
		self.service_name = service_name
		self.group_name = group_name
		self.home_path = home_path
		self.ping_count = ping_count

PING_SETTINGS_SCHEMA = {
	'service_name': ar.Unicode(),
	'group_name': ar.Unicode(),
	'home_path': ar.Unicode(),
	'ping_count': ar.Integer8(),
}

ar.bind(PingSettings, object_schema=PING_SETTINGS_SCHEMA)

# Attempt a few pings in the hope there is an echo. A test for connectivity,
# some measure of life-or-death at the remote end and also the time taken
# for a round trip. Which is not representative of the time taken over peer
# connections and relays.
def ping_service(self, service, count):
	p = ar.Ping()
	count = count or 8
	for i in range(count):
		self.send(p, service.agent_address)
		started = ar.clock_now()
		m = self.select(ar.Ack, ar.Stop, seconds=2.0)

		if isinstance(m, ar.Ack):					# An echo.
			span = ar.clock_now() - started
			t = ar.span_to_text(span)
			ar.output_line(f'+ received ack after {t}' )

		elif isinstance(m, ar.SelectTimer):		# Too long.
			ar.output_line('+ timed out')
			continue
		else:
			return	# Interrupted.

		# Insert a delay to allow really slow echoes to
		# pass and to not create a burst of traffic.
		self.start(ar.T1, 1.0)
		m = self.select(ar.T1, ar.Stop)
		if isinstance(m, ar.T1):
			pass
		else:
			return	# Interrupted.

	return ar.Faulted(f'service {service} not found')

# Look for the specified service with the purpose
# of pinging the named agent.
def find_ping(self, lineage, service, count):
	for a in lineage:
		for s in a.listing:
			if s.search_or_listing == service:
				t = ar.ScopeOfService.to_name(a.scope)
				ar.output_line(f'[{t}] {service} ({len(s.agent_address)} hops)')
				ping_service(self, s, count)
				return None

	# No such service.
	return ar.Faulted(f'service {service} not found')

def procedure_ping(self, ping, service, group, home):
	service = ar.word_argument_2(service, ping.service_name, None, 'service')
	group = ar.word_argument_2(group, ping.group_name, DEFAULT_GROUP, GROUP)
	home = ar.word_argument_2(home, ping.home_path, DEFAULT_HOME, HOME)

	if '.' in group:
		e = ar.Rejected(group_name=(group, f'no-dots name'))
		raise ar.Incomplete(e)
	group_role = f'group.{group}'

	hb = open_home(home)

	if not hb.role_exists(group_role):
		e = ar.Failed(group_exists=(f'group "{group}" not found', None))
		raise ar.Incomplete(e)

	_, running = role_status(self, hb, [group_role])
	if running:
		e = ar.Failed(group_running=(f'group "{group}" is already running', None))
		raise ar.Incomplete(e)

	settings = GroupSettings()
	hr = hb.open_role(group_role, settings, None, ar.NodeProperties(executable='ansar-group'))

	settings = hr.role_settings[2]				# From the group.
	connect_above = settings.connect_above
	accept_below = ar.LocalPort(0)				# Disabled.

	a = self.create(ar.ServiceDirectory, ar.ScopeOfService.GROUP, connect_above, accept_below)
	self.assign(a, None)
	self.directory = a

	try:
		# Directory responds with a HostPort
		# Then wait for a grace period.
		m = self.select(ar.HostPort, ar.Stop)
		if isinstance(m, ar.HostPort):
			connect_above = m
		self.start(ar.T2, seconds=1.5)
		self.select(ar.T2, ar.Stop)

		s = ar.DirectoryScope(connect_above=connect_above,
			started=ar.world_now(),
			connected=None)
		e = ar.NetworkEnquiry(lineage=[s])
		self.send(e, self.directory)

		m = self.select(ar.DirectoryAncestry, ar.Stop)
		if isinstance(m, DirectoryAncestry):
			return find_ping(self, m.lineage, service, ping.ping_count)

	finally:
		self.send(ar.Stop(), self.directory)
		self.select(ar.Completed, ar.Stop)

	return None

# Keyboard input.
# Form/field filling.
def complete_field(name, t):
	if name == 'password':
		d = getpass.getpass(f'Password: ')
		return d

	ip = name.capitalize()
	ip = ip.replace('_', ' ')
	try:
		kb = input(f'{ip}: ')
	except (ValueError, EOFError):
		return None
	if kb is None or not isinstance(kb, str) or len(kb) < 1:
		return None

	if isinstance(t, QUOTED_TYPE):
		sh = SHIPMENT_WITH_QUOTES % (kb,)
	else:
		sh = SHIPMENT_WITHOUT_QUOTES % (kb,)
	try:
		encoding = ar.CodecJson()
		d, _ = encoding.decode(sh, t)
	except ar.CodecFailed as e:
		f = ar.Faulted(f'cannot accept input for "{ip}"', str(e))
		raise ar.Incomplete(f)
	return d

def complete_form(self, form, set_none=True):
	schema = form.__art__.value
	for k, v in schema.items():
		if k == 'login_token':
			continue
		t = getattr(form, k, None)
		if t is not None:				# Value already present in form.
			continue
		d = complete_field(k, v)
		if d is None and not set_none:	# Empty data entry and not forcing nulls.
			continue
		setattr(form, k, d)

#
#

class CloudSettings(object):
	def __init__(self, add=False, read=False,
			update=False, delete=False,	export=False,
			login_id=None, login_email=None,
			password=None,
			family_name=None, given_name=None, nick_name=None,
			honorific=None,
			directory_id=None,
			product_name=None, product_instance=None,
			organization_name=None, organization_location=None,
			export_file=None, access_name=None,
			show_identities=False, show_times=False):
		self.add = add
		self.read = read
		self.update = update
		self.delete = delete
		self.export = export
		self.login_id = login_id
		self.login_email = login_email
		self.password = password
		self.family_name = family_name
		self.given_name = given_name
		self.nick_name = nick_name
		self.honorific = honorific
		self.directory_id = directory_id
		self.organization_name = organization_name
		self.organization_location = organization_location
		self.product_name = product_name
		self.product_instance = product_instance
		self.export_file = export_file
		self.access_name = access_name
		self.show_identities = show_identities
		self.show_times = show_times

ACCOUNT_SETTINGS_SCHEMA = {
	'add': ar.Boolean(),
	'read': ar.Boolean(),
	'update': ar.Boolean(),
	'delete': ar.Boolean(),
	'export': ar.Boolean(),
	'login_id': ar.UUID(),
	'login_email': ar.Unicode(),
	'password': ar.Unicode(),
	'family_name': ar.Unicode(),
	'given_name': ar.Unicode(),
	'nick_name': ar.Unicode(),
	'honorific': ar.Unicode(),
	'directory_id': ar.UUID(),
	'organization_name': ar.Unicode(),
	'organization_location': ar.Unicode(),
	'product_name': ar.Unicode(),
	'product_instance': InstanceOfProduct,
	'export_file': ar.Unicode(),
	'access_name': ar.Unicode(),
	'show_identities': ar.Boolean(),
	'show_times': ar.Boolean(),
}

ar.bind(CloudSettings, object_schema=ACCOUNT_SETTINGS_SCHEMA)

# Standardize checking and diagnostics for all the
# cloud interactions.
def crud_address_and_token(crud, ipp, token):
	if crud > 1:
		f = ar.Faulted('multiple operations specified', 'not supported')
		return f
	if not ipp:
		f = ar.Faulted('no address defined for the ansar cloud')
		return f
	if not token:
		f = ar.Faulted('not logged in', 'need to signup or login')
		return f
	return None

def connect_cloud(self, cloud_ip, encrypted):
	session = None
	ar.connect(self, ar.HostPort(cloud_ip, FOH_PORT), encrypted=encrypted)
	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.Connected):
		session = self.return_address
	elif isinstance(m, ar.NotConnected):
		pass
	else:
		m = ar.Aborted()
	return session, m

# Create a new account.
def procedure_signup(self, settings, account):
	cloud_ip = settings.cloud_ip

	f = crud_address_and_token(1, cloud_ip, uuid.uuid4())
	if f:
		return f

	encrypted = settings.encrypted
	session, m = connect_cloud(self, cloud_ip, encrypted)
	if session is None:
		return m

	try:
		return account_signup(self, session, settings, account)
	finally:
		self.send(ar.Close(), session)
		self.select(ar.Closed, ar.Stop)

def account_signup(self, session, settings, account):
	'''Create a new account with a primary login access.'''
	signup = AccountSignup(login_email=account.login_email,
			password=account.password,
			family_name=account.family_name, given_name=account.given_name,
			nick_name=account.nick_name,
			honorific=account.honorific,
			organization_name=account.organization_name,
			organization_location=account.organization_location)
	complete_form(self, signup)

	self.send(signup, session)
	m = self.select(AccountOpened, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, AccountOpened):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()

	# Save the login token for easy access for
	# next few minutes.
	settings.login_token = m.login_token
	settings.login_id = m.login_id

	self.debug(f'Storing signup {m.login_token}, {m.login_id}')

	ar.store_settings(settings)
	return None

# Refresh the session with an account.
def procedure_login(self, settings, account):
	'''CRUD for the login entity.'''
	cloud_ip = settings.cloud_ip
	login_token = settings.login_token or uuid.uuid4()

	f = crud_address_and_token(1, cloud_ip, login_token)
	if f:
		return f

	encrypted = settings.encrypted
	session, m = connect_cloud(self, cloud_ip, encrypted)
	if session is None:
		return m

	try:
		if account.add:
			return login_add(self, login_token, session, account)
		elif account.read:
			return login_read(self, login_token, session, settings, account)
		elif account.update:
			return login_update(self, login_token, session, account)
		elif account.delete:
			return login_delete(self, login_token, session, account)
		return login_open(self, session, account)		# Creds for existing account, update token.
	finally:
		self.send(ar.Close(), session)
		self.select(ar.Closed, ar.Stop)

def login_open(self, session, account):
	'''Open an existing account.'''
	login = AccountLogin(login_email=account.login_email, password=account.password)
	complete_form(self, login)

	self.send(login, session)
	m = self.select(AccountOpened, ar.Faulted, ar.Closed, ar.Abandoned, ar.Stop)
	if isinstance(m, AccountOpened):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, (ar.Closed, ar.Abandoned)):
		return m
	else:
		return ar.Aborted()

	# Save the login token for easy access for
	# next few minutes.
	settings = ar.object_custom_settings()
	settings.login_token = m.login_token
	settings.login_id = m.login_id

	self.debug(f'Storing signup {m.login_token}, {m.login_id}')

	ar.store_settings(settings)
	return None

def login_add(self, login_token, session, account):
	'''Add an auxiliary login to the current account.'''
	add = LoginAdd(login_token=login_token,
		login_email=account.login_email, password=account.password,
		family_name=account.family_name, given_name=account.given_name,
		nick_name=account.nick_name, honorific=account.honorific)
	complete_form(self, add)

	self.send(add, session)
	m = self.select(LoginPage, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, LoginPage):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		return m
	else:
		return ar.Aborted()
	return None

def login_read(self, login_token, session, settings, account):
	'''Read a login within the current account.'''
	login_id=account.login_id or settings.login_id		# Explicit command arg or current login.
	read = LoginRead(login_token=login_token, login_id=login_id)
	complete_form(self, read)

	self.send(read, session)
	m = self.select(LoginPage, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, LoginPage):
		if not object_settings.pure_object:
			output_login(m, account)
			return None
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()
	return m

def login_update(self, login_token, session, account):
	'''Update a login in the current account.'''
	add = LoginUpdate(login_token=login_token,
		login_email=account.login_email, password=account.password,
		family_name=account.family_name, given_name=account.given_name,
		nick_name=account.nick_name, honorific=account.honorific)
	a = account.login_email or account.password or account.family_name or account.given_name or account.nick_name or account.honorific
	if not a:
		complete_form(self, add, set_none=False)

	self.send(add, session)
	m = self.select(LoginPage, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, LoginPage):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		return m
	else:
		return ar.Aborted()
	return None

def login_delete(self, login_token, session, account):
	'''Delete a login within the current account.'''
	
	# DO NOT default to current login_id.
	delete = LoginDelete(login_token=login_token, login_id=account.login_id)
	complete_form(self, delete)

	self.send(delete, session)
	m = self.select(LoginDeleted, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, LoginDeleted):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		return m
	else:
		return ar.Aborted()
	return None

# CRUD for the account entity. Well, more like RUD as
# the create part is covered by signup and login.
def procedure_account(self, settings, account):
	'''CRUD for the account entity.'''
	cloud_ip = settings.cloud_ip
	login_token = settings.login_token

	crud = sum([account.add, account.read, account.update, account.delete])

	f = crud_address_and_token(crud, cloud_ip, login_token)
	if f:
		return f

	encrypted = settings.encrypted
	session, m = connect_cloud(self, cloud_ip, encrypted)
	if session is None:
		return m

	try:
		if account.update:
			return account_update(self, login_token, session, account)
		elif account.delete:
			return account_delete(self, login_token, session, account)
		return account_read(self, login_token, session, account)
	finally:
		self.send(ar.Close(), session)
		self.select(ar.Closed, ar.Stop)

def account_read(self, login_token, session, account):
	'''Read the current, logged-in account.'''
	read = AccountRead(login_token=login_token)

	self.send(read, session)
	m = self.select(AccountPage, ar.Faulted, ar.Abandoned, ar.Closed, ar.Stop)
	if isinstance(m, AccountPage):
		if not object_settings.pure_object:
			output_account(m, account)
			return None
	elif isinstance(m, ar.Stop):
		m = ar.Aborted()
	return m

def account_update(self, login_token, session, account):
	'''Update the current, logged-in account.'''
	update = AccountUpdate(login_token=login_token,
		organization_name=account.organization_name, organization_location=account.organization_location)
	complete_form(self, update)

	self.send(update, session)
	m = self.select(AccountPage, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, AccountPage):
		if not object_settings.pure_object:
			output_account(m, account)
			return None
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()
	return m

def account_delete(self, login_token, session, account):
	'''Delete the current, logged-in account.'''
	delete = AccountDelete(login_token=login_token)

	self.send(delete, session)
	m = self.select(AccountDeleted, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, AccountDeleted):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()
	return None

#
#
def procedure_directory(self, settings, account):
	'''CRUD for the directory entity.'''
	cloud_ip = settings.cloud_ip
	login_token = settings.login_token

	crud = sum([account.read, account.update, account.export])

	f = crud_address_and_token(crud, cloud_ip, login_token)
	if f:
		return f

	encrypted = settings.encrypted
	session, m = connect_cloud(self, cloud_ip, encrypted)
	if session is None:
		return m

	try:
		if account.add:
			return directory_add(self, login_token, session, account)
		elif account.update:
			return directory_update(self, login_token, session, account)
		elif account.delete:
			return directory_delete(self, login_token, session, account)
		elif account.export:
			return directory_export(self, login_token, session, account)
		return directory_read(self, login_token, session, account)
	finally:
		self.send(ar.Close(), session)
		self.select(ar.Closed, ar.Stop)

def directory_add(self, login_token, session, account):
	'''Add a directory to the current account.'''
	add = DirectoryAdd(login_token=login_token,
		product_name=account.product_name, product_instance=account.product_instance)
	complete_form(self, add)

	self.send(add, session)
	m = self.select(DirectoryPage, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, DirectoryPage):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()
	return None

def directory_read(self, login_token, session, account):
	'''Read a directory from the current account.'''
	read = DirectoryRead(login_token=login_token,
		directory_id=account.directory_id)
	complete_form(self, read)
	if not read.directory_id:
		f = ar.Faulted('directory id not specified', 'use --directory-id=<uuid>')
		return f

	self.send(read, session)
	m = self.select(DirectoryPage, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, DirectoryPage):
		if not object_settings.pure_object:
			output_directory(m, account)
			return None
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()
	return m

def directory_update(self, login_token, session, account):
	'''Update an existing directory in the current account.'''
	update = DirectoryUpdate(login_token=login_token, directory_id=account.directory_id,
		product_name=account.product_name, product_instance=account.product_instance)
	c = update.directory_id is not None and (update.product_name is not None or update.product_instance is not None)
	if not c:
		complete_form(self, update, set_none=False)
	if not account.directory_id:
		f = ar.Faulted('directory id not specified', 'use --directory-id=<uuid>')
		return f

	self.send(update, session)
	m = self.select(DirectoryPage, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, DirectoryPage):
		if not object_settings.pure_object:
			output_directory(m, account)
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()
	return None

def directory_delete(self, login_token, session, account):
	'''Delete an existing directory in the current account.'''
	delete = DirectoryDelete(login_token=login_token, directory_id=account.directory_id)
	complete_form(self, delete)

	self.send(delete, session)
	m = self.select(DirectoryDeleted, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, DirectoryDeleted):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		return m
	else:
		return ar.Aborted()
	return None

def directory_export(self, login_token, session, account):
	'''Export access details for a directory in the current account.'''
	settings = ar.object_custom_settings()
	cloud_ip = settings.cloud_ip

	export = DirectoryExport(login_token=login_token,
		directory_id=account.directory_id, access_name=account.access_name)
	complete_form(self, export)
	if not export.directory_id:
		f = ar.Faulted('directory id not specified', 'use --directory-id=<uuid>')
		return f
	if not export.access_name:
		f = ar.Faulted('access name not specified', 'use --access-name=<uuid>')
		return f

	self.send(export, session)
	m = self.select(DirectoryExported, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, DirectoryExported):
		cloud_ipp = ar.HostPort(cloud_ip, FOH_PORT)
		encrypted = settings.encrypted
		w = WideAreaAccess(access_ipp=cloud_ipp, encrypted=encrypted, access_token=m.access_token,
			account_id=m.account_id, directory_id=m.directory_id,
			product_name=m.product_name, product_instance=m.product_instance)
		f = output_access(w, account.export_file)
		if f:
			return f
		return None
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()
	return None

def output_access(access, export_file):
	if not export_file:
		try:
			encoding = ar.CodecJson(pretty_format=True)
			s = encoding.encode(access, ar.Any())
		except ar.CodecError as e:
			s = str(e)
			f = ar.Failed(encode_access=(s, None))
			return f
		ar.output_line(s)
		return None

	try:
		f = ar.File(export_file, ar.Any(), decorate_names=False)
		f.store(access)
	except (ar.FileFailure, ar.CodecError) as e:
		s = str(e)
		f = ar.Failed(encode_access_file=(s, None))
		return f
	return None

def output_account(account, settings):
	account_identity = ''

	notes = []
	if settings.show_identities:
		notes.append(f'{account.account_id}')
	if settings.show_times:
		t = ar.world_to_text(account.created)
		notes.append(t)

	if notes:
		n = ', '.join(notes)
		account_identity = f' ({n})'
	ar.output_line(f'+ Account {account}{account_identity}')
	ar.output_line(f'+ Number of logins: {account.number_of_logins}', tab=1)
	ar.output_line(f'+ Number of directores: {account.number_of_directories}', tab=1)
	ar.output_line(f'+ Number of relays: {account.number_of_relays}', tab=1)

	ar.output_line(f'+ Logins ({len(account.login_page)})', tab=1)
	for l in account.login_page:
		login_identity = ''
		login_notes = []
		if settings.show_identities:
			login_notes.append(f'{l.login_id}')
		if settings.show_times:
			t = ar.world_to_text(l.created)
			login_notes.append(t)

		if login_notes:
			n = ', '.join(login_notes)
			login_identity = f' ({n})'
		ar.output_line(f'+ {l}{login_identity}', tab=2)
		ar.output_line(f'+ Login email: {l.login_email}', tab=3)
		ar.output_line(f'+ Family name: {l.family_name}', tab=3)
		ar.output_line(f'+ Given name: {l.given_name}', tab=3)
		ar.output_line(f'+ Nick name: {l.nick_name}', tab=3)
		ar.output_line(f'+ Honorific: {l.honorific}', tab=3)

	ar.output_line(f'+ Directories ({len(account.directory_page)})', tab=1)
	for d in account.directory_page:
		directory_identity = ''
		directory_notes = []
		if settings.show_identities:
			directory_notes.append(f'{d.directory_id}')
		if settings.show_times:
			t = ar.world_to_text(d.created)
			directory_notes.append(t)

		if directory_notes:
			n = ', '.join(directory_notes)
			directory_identity = f' ({n})'
		ar.output_line(f'+ {d}{directory_identity}', tab=2)
		ar.output_line(f'+ Number of tokens: {d.number_of_tokens}', tab=3)
		ar.output_line(f'+ Connected routes: {d.connected_routes}', tab=3)
		ar.output_line(f'+ Messages per second: {d.messages_per_second}', tab=3)
		ar.output_line(f'+ Bytes per second: {d.bytes_per_second}', tab=3)
		ar.output_line(f'+ Exported token ({len(d.exported_name)})', tab=3)
		for t in d.exported_name:
			ar.output_line(f'+ {t}', tab=4)

def output_login(login, settings):
	login_identity = ''

	notes = []
	if settings.show_identities:
		notes.append(f'{login.account_id}')
	if settings.show_times:
		t = ar.world_to_text(login.created)
		notes.append(t)

	if notes:
		n = ', '.join(notes)
		login_identity = f' ({n})'

	ar.output_line(f'+ {login}{login_identity}')
	ar.output_line(f'+ Login email: {login.login_email}', tab=1)
	ar.output_line(f'+ Family name: {login.family_name}', tab=1)
	ar.output_line(f'+ Given name: {login.given_name}', tab=1)
	ar.output_line(f'+ Nick name: {login.nick_name}', tab=1)
	ar.output_line(f'+ Honorific: {login.honorific}', tab=1)

def output_directory(directory, settings):
	directory_identity = ''

	notes = []
	if settings.show_identities:
		notes.append(f'{directory.directory_id}')
	if settings.show_times:
		t = ar.world_to_text(directory.created)
		notes.append(t)

	if notes:
		n = ', '.join(notes)
		directory_identity = f' ({n})'

	ar.output_line(f'+ {directory}{directory_identity}')
	ar.output_line(f'+ Number of tokens: {directory.number_of_tokens}', tab=1)
	ar.output_line(f'+ Connected routes: {directory.connected_routes}', tab=1)
	ar.output_line(f'+ Messages per second: {directory.messages_per_second}', tab=1)
	ar.output_line(f'+ Bytes per second: {directory.bytes_per_second}', tab=1)
	ar.output_line(f'+ Exported token ({len(directory.exported_name)})', tab=1)
	for t in directory.exported_name:
		ar.output_line(f'+ {t}', tab=2)
