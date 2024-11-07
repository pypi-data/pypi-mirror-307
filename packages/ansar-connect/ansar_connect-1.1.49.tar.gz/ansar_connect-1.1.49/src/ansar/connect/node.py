####################################################################################
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

""".

.
"""
__docformat__ = 'restructuredtext'

import os
import sys
import signal
import uuid
import time

import ansar.create as ar
import ansar.create.point as ap
from .socketry import *
from .directory_if import *
from .directory import *
from .wan import *
from .transporting import *

__all__ = [
	'NodeSettings',
	'node_settings',
	'NodeProperties',
	'node_passing',
	'sub_node_passing',
	'create_node',
]

#
#
class NodeSettings(object):
	def __init__(self, node_scope=None, group_port=None, accept_port=None):
		self.node_scope = node_scope
		self.group_port = group_port
		self.accept_port = accept_port

NODE_SETTINGS_SCHEMA = {
	'node_scope': ScopeOfService,
	'group_port': ar.Integer8(),
	'accept_port': ar.Integer8(),
}

ar.bind(NodeSettings, object_schema=NODE_SETTINGS_SCHEMA)

#
#
node_settings = NodeSettings()


#
#
class NodeProperties(object):
	def __init__(self, guid=None, created=None, executable=None, start_stop=None, retry=None, storage=None):
		self.guid = guid
		self.created = created
		self.executable = executable
		self.start_stop = start_stop or ar.default_deque()
		self.retry = retry or ar.RetryIntervals(step_limit=0)
		self.storage = storage
		#self.connect_above = connect_above					# HostPort or cloud connection or None.
		#self.accept_below = accept_below or HostPort()		# Must be a listen address.

NODE_PROPERTIES_SCHEMA = {
	'guid': ar.UUID(),
	'created': ar.WorldTime(),
	'executable': ar.Unicode(),
	'start_stop': ar.DequeOf(ar.StartStop),
	'retry': ar.UserDefined(ar.RetryIntervals),
	'storage': ar.Integer8(),
}

ar.bind(NodeProperties, object_schema=NODE_PROPERTIES_SCHEMA)

#
#
# Standard parameter processing. Check for name collision.
#
def node_passing(special_settings):
	if special_settings is not None:
		a = node_settings.__art__.value.keys()
		b = ar.object_settings.__art__.value.keys()
		c = special_settings.__art__.value.keys()
		d = set(a) & set(c)
		if len(d) > 0:
			j = ', '.join(c)
			raise ValueError('collision in settings names - {collisions}'.format(collisions=j))
		d = set(b) & set(c)
		if len(d) > 0:
			j = ', '.join(c)
			raise ValueError('collision in settings names - {collisions}'.format(collisions=j))
	executable, word, ls = ar.break_args()
	x1, r1 = ar.extract_args(node_settings, ls, ar.object_settings)
	x2, r2 = ar.extract_args(ar.object_settings, r1, special_settings)
	ar.arg_values(node_settings, x1)
	ar.arg_values(ar.object_settings, x2)
	return executable, word, r2

def sub_node_passing(special_settings, table):
	if special_settings is not None:
		a = node_settings.__art__.value.keys()
		b = ar.object_settings.__art__.value.keys()
		c = special_settings.__art__.value.keys()
		d = set(a) & set(c)
		if len(d) > 0:
			j = ', '.join(c)
			raise ValueError('collision in settings names - {collisions}'.format(collisions=j))
		d = set(b) & set(c)
		if len(d) > 0:
			j = ', '.join(c)
			raise ValueError('collision in settings names - {collisions}'.format(collisions=j))

	executable, ls1, sub, ls2, word = ar.sub_args()
	x1, r1 = ar.extract_args(node_settings, ls1, ar.object_settings)
	x2, r2 = ar.extract_args(ar.object_settings, r1, special_settings)
	ar.arg_values(node_settings, x1)
	ar.arg_values(ar.object_settings, x2)

	# Support for the concept of a noop pass, just for the
	# framework.
	def no_sub_required(s):
		return s.help or s.dump_settings or s.dump_input

	if sub is not None:
		try:
			sub_function, sub_settings = table[sub]
		except KeyError:
			raise ValueError(f'unknown sub-command "{sub}"')

		if sub_settings:
			x3, r3 = ar.extract_args(sub_settings, ls2, None)
			ar.arg_values(sub_settings, x3)
		else:
			r3 = ls2
	elif no_sub_required(ar.object_settings):
		# Give framework a chance to complete some
		# admin operation.
		sub_function = None
		r3 = ({}, {})
	else:
		raise ValueError('no-op command')

	bundle = (sub_function, # The sub-command function.
		r3,				 # Remainder from ls2, i.e. for passing to sub-component
		word)			   # Non-flag arguments.

	return executable, bundle, r2

#
#
def node_vector(self, object_type, settings, input, variables, fixed_value, key_value):
	role = ar.object_role()

	name_counts = ['"%s" (%d)' % (k, len(v)) for k, v in ap.pt.thread_classes.items()]

	executable = os.path.abspath(sys.argv[0])
	self.trace('Executable "%s" as node process (%d)' % (executable, os.getpid()))
	self.trace('Working folder "%s"' % (os.getcwd()))
	self.trace('Running object "%s"' % (object_type.__art__.path,))
	self.trace('Class threads (%d) %s' % (len(ap.pt.thread_classes), ','.join(name_counts)))

	# One source of directory information.
	# Persistent.
	p = role.properties

	def return_signal(value):
		ar.co.signal_received = signal.SIGKILL
		return value

	# Start with the scope enumeration passed through from
	# create_node().
	scope = node_settings.node_scope
	if scope is None:
		return ar.Failed(node_scope=(None, 'scope is undefined'))

	if scope == ScopeOfService.PROCESS:
		group_port = node_settings.group_port
		if group_port is None:
			connect_above = HostPort()
			self.trace('No group port available')
		else:
			connect_above = LocalPort(group_port)
			self.trace(f'Detected group port {connect_above}')
		
		accept_below = HostPort(host=None)				# Null. Disabled.

		a = self.create(ServiceDirectory, scope, connect_above, accept_below)
		pb.directory = a

		# Wait for operational directory, esp. ephemeral.
		m = self.select(HostPort, ar.Completed, ar.Stop, ar.Faulted)
		if isinstance(m, ar.Completed):
			return return_signal(m.value)
		elif isinstance(m, ar.Stop):
			# Directory stopped in AddOn.
			return return_signal(ar.Aborted())
		elif isinstance(m, ar.Faulted):
			return return_signal(m)

	pa = ()
	if settings is not None:
		pa = pa + (settings,)
	if input is not None:
		pa = pa + (input,)
	if variables is not None:
		pa = pa + (variables,)
	pa = pa + fixed_value

	a = self.create(object_type, *pa, **key_value)

	try:
		while True:
			m = self.select(ar.Completed, ar.Stop, ar.Pause, ar.Resume)

			if isinstance(m, ar.Completed):
				# Do a "fake" signaling. Sidestep all the platform machinery
				# and just set a global. It does avoid any complexities
				# arising from overlapping events. Spent far too much time
				# trying to untangle signals, exceptions and interrupted i/o.
				ar.co.signal_received = signal.SIGKILL
				return m.value
			elif isinstance(m, ar.Stop):
				# Received a Stop.
				self.send(m, a)
				m = self.select(ar.Completed)
				return m.value
			
			self.send(m, a)
	finally:
		pass

ar.bind_function(node_vector, lifecycle=True, message_trail=True, execution_trace=True)

#
#
def create_node(object_type, *fixed_value,
	factory_settings=None, factory_input=None, factory_variables=None,
	parameter_passing=node_passing, parameter_table=None,
	upgrade=None, logs=ar.log_to_nowhere,
	scope=ScopeOfService.PROCESS, **key_value):
	"""Creates an async pub-sub process shim around a "main" async object. Returns nothing.

	:param object_type: the type of an async object to be instantiated
	:type object_type: a function or a Point-based class
	:param fixed_value: position args to forward to the object
	:type fixed_value: tuple
	:param factory_settings: persistent values
	:type factory_settings: instance of a registered class
	:param factory_input: per-invocation values
	:type factory_input: instance of a registered class
	:param factory_variables: host environment values
	:type factory_variables: instance of a registered class
	:param parameter_passing: method for parsing sys.argv[]
	:type parameter_passing: a function
	:param parameter_table: table of sub-commands and their associated functions
	:type parameter_table: dict
	:param upgrade: function that accepts old versions of settings/input and produces the current version
	:type upgrade: function
	:param logs: a callable object expecting to receive log objects
	:type logs: function or class with __call__ method
	:param scope: level of the internal directory object
	:type scope: enumeration
	:param key_value: named args to forward to the object
	:type key_value: dict
	:rtype: None
	"""
	node_settings.node_scope = scope

	ar.create_object(object_type, *fixed_value,
		factory_settings=factory_settings, factory_input=factory_input, factory_variables=factory_variables,
		parameter_passing=parameter_passing, parameter_table=parameter_table,
		start_vector=node_vector,
		upgrade=upgrade, logs=logs, properties=NodeProperties, **key_value)
