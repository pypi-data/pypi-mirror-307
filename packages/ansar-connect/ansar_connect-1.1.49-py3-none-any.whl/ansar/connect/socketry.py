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

import queue as sq
import threading as thr
import errno
import socket
import select
import re
import string
from nacl.public import PrivateKey, PublicKey, Box
import ansar.create as ar
from .transporting_if import ts
from .http import ApiServerStream, ApiClientSession, ApiClientStream

from copy import copy

__all__ = [
	'HostPort',
	'LocalPort',
	'ScopeOfIP',
	'local_private_public',
	'Blob',
	'CreateFrame',
	'ListenForStream',
	'ConnectStream',
	'StopListening',
	'Listening',
	'Accepted',
	'Connected',
	'NotListening',
	'NotAccepted',
	'NotConnected',
	'Close',
	'Closed',
	'Abandoned',
	'SocketSelect',
	'SocketChannel',
]

# Machine states.
class INITIAL: pass
class PENDING: pass
class NORMAL: pass
class CHECKING: pass
class CLEARING: pass

#
#
LOCAL_HOST = '127.0.0.1'

class HostPort(object):
	"""Combination of an IP address or name, and a port number.

	:param host: IP address or name
	:type host: str
	:param port: network port
	:type port: int
	"""
	def __init__(self, host=None, port=None):
		self.host = host
		self.port = port
	
	def __str__(self):
		return f'{self.host}:{self.port}'

	def inet(self):
		return (self.host, self.port)

class LocalPort(HostPort):
	def __init__(self, port=None):
		HostPort.__init__(self, LOCAL_HOST, port)

HOST_PORT_SCHEMA = {
	'host': str,
	'port': int,
}

ar.bind(HostPort, object_schema=HOST_PORT_SCHEMA)
ar.bind(LocalPort, object_schema=HOST_PORT_SCHEMA)

#
#
DOTTED_IP = re.compile(r'(\d+)\.(\d+)\.(\d+)\.(\d+)')
ScopeOfIP = ar.Enumeration(OTHER=0, LOCAL=1, PRIVATE=2, PUBLIC=3)

def local_private_public(ip):
	m = DOTTED_IP.match(ip)
	if m is None:
		return ScopeOfIP.OTHER
	# Have complete verification of dotted layout
	b0 = int(m.groups()[0])
	b1 = int(m.groups()[1])

	# Not dotted -------- None
	# 127.x.x.x --------- 0, localhost
	# 10.x.x.x ---------- 1, private
	# 192.168.x.x ------- 1, private
	# 172.[16-31].x.x --- 1, private
	# else -------------- 2, public

	if b0 == 127:
		return ScopeOfIP.LOCAL
	elif b0 == 10:
		return ScopeOfIP.PRIVATE
	elif b0 == 192 and b1 == 168:
		return ScopeOfIP.PRIVATE
	elif b0 == 172 and (b1 > 15 and b1 < 32):
		return ScopeOfIP.PRIVATE
	return ScopeOfIP.PUBLIC

#
#
class Blob(object):
    def __init__(self, block=None):
        self.block = block

ar.bind(Blob, object_schema={'block': ar.Block()})

#
#
class CreateFrame(object):
	"""Capture values needed for async object creation.

	:param object_type: type to be created
	:type object_type: function or Point-based class
	:param args: positional parameters
	:type args: tuple
	:param kw: named parameters
	:type kw: dict
	"""
	def __init__(self, object_type, *args, **kw):
		self.object_type = object_type
		self.args = args
		self.kw = kw

# Control messages sent to the sockets thread
# via the control channel.
class ListenForStream(object):
	def __init__(self, requested_ipp=None, create_session=None, upgrade=None, encrypted=False,
			api_server=None, default_to_request=True, ansar_client=False):
		self.requested_ipp = requested_ipp or HostPort()
		self.create_session = create_session
		self.upgrade = upgrade
		self.encrypted = encrypted
		self.api_server = api_server
		self.default_to_request = default_to_request
		self.ansar_client = ansar_client

class ConnectStream(object):
	def __init__(self, requested_ipp=None, create_session=None, upgrade=None, encrypted=False, self_checking=False,
			api_client=None, ansar_server=False):
		self.requested_ipp = requested_ipp or HostPort()
		self.create_session = create_session
		self.upgrade = upgrade
		self.encrypted = encrypted
		self.self_checking = self_checking
		self.api_client = api_client
		self.ansar_server = ansar_server

class StopListening(object):
	def __init__(self, listening_ipp=None):
		self.listening_ipp = listening_ipp or HostPort()

# Update messages from sockets thread to app.
class Listening(object):
	"""Session notification, server presence established.

	:param requested_ipp: IP and port to listen at
	:type requested_ipp: HostPort
	:param listening_ipp: established IP and port
	:type listening_ipp: HostPort
	:param encrypted: is the client encrypting
	:type encrypted: bool
	"""
	def __init__(self, listening_address=None, requested_ipp=None, listening_ipp=None, encrypted=False):
		self.listening_address = listening_address
		self.requested_ipp = requested_ipp or HostPort()
		self.listening_ipp = listening_ipp or HostPort()
		self.encrypted = encrypted

class Accepted(object):
	"""Session notification, transport to client established.

	:param requested_ipp: IP and port listening at
	:type requested_ipp: HostPort
	:param accepted_ipp: local IP and port
	:type accepted_ipp: HostPort
	:param remote_address: address of SocketProxy
	:type remote_address: async address
	:param opened_at: moment of acceptance
	:type opened_at: datetime
	"""
	def __init__(self, listening_address=None, listening_ipp=None, accepted_ipp=None, remote_address=None, opened_at=None):
		self.listening_address = listening_address
		self.listening_ipp = listening_ipp or HostPort()
		self.accepted_ipp = accepted_ipp or HostPort()
		self.remote_address = remote_address
		self.opened_at = opened_at

class Connected(object):
	"""Session notification, transport to server established.

	:param requested_ipp: IP and port to connect to
	:type requested_ipp: HostPort
	:param connected_ipp: local IP and port
	:type connected_ipp: HostPort
	:param remote_address: address of SocketProxy
	:type remote_address: async address
	:param opened_at: moment of connection
	:type opened_at: datetime
	"""
	def __init__(self, requested_ipp=None, connected_ipp=None, remote_address=None, opened_at=None):
		self.requested_ipp = requested_ipp or HostPort()
		self.connected_ipp = connected_ipp or HostPort()
		self.remote_address = remote_address
		self.opened_at = opened_at

class NotListening(ar.Faulted):
	"""Session notification, server not established.

	:param requested_ipp: IP and port to listen at
	:type requested_ipp: HostPort
	:param error_code: platform error number
	:type error_code: int
	:param error_text: platform error message
	:type error_text: str
	"""
	def __init__(self, requested_ipp=None, error_code=0, error_text=None):
		ar.Faulted.__init__(self, f'cannot listen at "{requested_ipp}"', error_text, exit_code=error_code)
		self.requested_ipp = requested_ipp or HostPort()

class NotAccepted(ar.Faulted):
	"""Session notification, transport to client not established.

	:param listening_ipp: IP and port listening at
	:type listening_ipp: HostPort
	:param error_code: platform error number
	:type error_code: int
	:param error_text: platform error message
	:type error_text: str
	"""
	def __init__(self, listening_ipp=None, error_code=0, error_text=None):
		ar.Faulted.__init__(self, f'cannot accept at "{listening_ipp}"', error_text, exit_code=error_code)
		self.listening_ipp = listening_ipp or HostPort()

class NotConnected(ar.Faulted):
	"""Session notification, transport to server established.

	:param requested_ipp: IP and port to connect to
	:type requested_ipp: HostPort
	:param error_code: platform error number
	:type error_code: int
	:param error_text: platform error message
	:type error_text: str
	"""
	def __init__(self, requested_ipp=None, error_code=0, error_text=None):
		ar.Faulted.__init__(self, f'cannot connect to "{requested_ipp}"', error_text, exit_code=error_code)
		self.requested_ipp = requested_ipp or HostPort()

CONTROL_SCHEMA = {
	'requested_ipp': ar.UserDefined(HostPort),
	'controller_address': ar.Address(),
	'remote_address': ar.Address(),
	'opened_at': ar.WorldTime(),
	'upgrade': ar.Type(),
	'create_session': ar.Type(),
	'connected_ipp': ar.UserDefined(HostPort),
	'listening_address': ar.Address(),
	'listening_ipp': ar.UserDefined(HostPort),
	'accepted_ipp': ar.UserDefined(HostPort),
	'condition': ar.Unicode(),
	'explanation': ar.Unicode(),
	'error_code': ar.Integer8(),
	'error_text': ar.Unicode(),
	'exit_code': ar.Integer8(),
	'encrypted': ar.Boolean(),
	'self_checking': ar.Boolean(),
	'api_server': ar.VectorOf(ar.Type()),
	'default_to_request': ar.Boolean(),
	'ansar_client': ar.Boolean(),
	'api_client': ar.Unicode(),
	'ansar_server': ar.Boolean(),
}

ar.bind(ListenForStream, object_schema=CONTROL_SCHEMA)
ar.bind(ConnectStream, object_schema=CONTROL_SCHEMA)
ar.bind(StopListening, object_schema=CONTROL_SCHEMA)
ar.bind(Listening, object_schema=CONTROL_SCHEMA, copy_before_sending=False)
ar.bind(Accepted, object_schema=CONTROL_SCHEMA)
ar.bind(Connected, object_schema=CONTROL_SCHEMA)
ar.bind(NotListening, object_schema=CONTROL_SCHEMA)
ar.bind(NotAccepted, object_schema=CONTROL_SCHEMA)
ar.bind(NotConnected, object_schema=CONTROL_SCHEMA)

# Session termination messages. Handshake between app
# and sockets thread to cleanly terminate a connection.
class Close(object):
	"""Session control, terminate the messaging transport.

	:param value: completion value for the session
	:type value: any
	"""
	def __init__(self, value=None):
		self.value = value

class Closed(ar.Faulted):
	"""Session notification, local termination of the messaging transport.

	:param value: completion value for the session
	:type value: any
	:param reason: short description
	:type reason: str
	:param opened_ipp: local IP address and port number
	:type opened_ipp: HostPort
	:param opened_at: moment of termination
	:type opened_at: datetime
	"""
	def __init__(self, value=None, reason=None, opened_ipp=None, opened_at=None):
		ar.Faulted.__init__(self, f'closed {opened_ipp}', reason)
		self.value = value
		self.opened_ipp = opened_ipp or HostPort()
		self.opened_at = opened_at

class Abandoned(ar.Faulted):
	"""Session notification, remote termination of the messaging transport.

	:param opened_ipp: local IP address and port number
	:type opened_ipp: HostPort
	:param opened_at: moment of termination
	:type opened_at: datetime
	"""
	def __init__(self, opened_ipp=None, opened_at=None):
		ar.Faulted.__init__(self, f'abandoned by {opened_ipp}')
		self.opened_ipp = opened_ipp or HostPort()
		self.opened_at = opened_at

ENDING_SCHEMA = {
	'value': ar.Any,
	'opened_ipp': ar.UserDefined(HostPort),
	'opened_at': ar.WorldTime(),
	'condition': ar.Unicode(),
	'explanation': ar.Unicode(),
	'error_code': ar.Integer8(),
	'error_text': ar.Unicode(),
	'exit_code': ar.Integer8(),
}

ar.bind(Close, object_schema=ENDING_SCHEMA, copy_before_sending=False)
ar.bind(Closed, object_schema=ENDING_SCHEMA, copy_before_sending=False)
ar.bind(Abandoned, object_schema=ENDING_SCHEMA, copy_before_sending=False)

#
#
class Shutdown(object):
	def __init__(self, s=None, value=False):
		self.s = s
		self.value = value

class Bump(object):
	def __init__(self, s=None):
		self.s = s

QUEUE_SCHEMA = {
	's': ar.Any,
	'value': ar.Any,
}

ar.bind(Shutdown, object_schema=QUEUE_SCHEMA, copy_before_sending=False)
ar.bind(Bump, object_schema=QUEUE_SCHEMA, copy_before_sending=False)

# Classes representing open sockets for one reason or another;
# - ControlChannel.... accepted end of backdoor into sockets loop.
# - TcpServer ........ an active listen
# - TcpClient ........ an active connect
# - TcpTransport ........ established transport, child of listen or connect

class ControlChannel(object):
	def __init__(self, s):
		self.s = s

class TcpServer(object):
	def __init__(self, s, request, listening, controller_address, upgrade):
		self.s = s
		self.request = request
		self.listening = listening
		self.controller_address = controller_address
		self.upgrade = upgrade

class TcpClient(object):
	def __init__(self, s, request, connected, controller_address, upgrade, encrypted, self_checking):
		self.s = s
		self.request = request
		self.connected = connected
		self.controller_address = controller_address
		self.upgrade = upgrade
		self.encrypted = encrypted
		self.self_checking = self_checking

# Underlying network constraints.
#
TCP_RECV = 4096
TCP_SEND = 4096
UDP_RECV = 4096
UDP_SEND = 4096

# Security/reliability behaviours.
#
NUMBER_OF_DIGITS = (7 * 3) + 2
GIANT_FRAME = 1048576

#
#
class Header(object):
	def __init__(self, to_address=None, return_address=None, tunnel=False):
		self.to_address = to_address
		self.return_address = return_address
		self.tunnel = tunnel

HEADER_SCHEMA = {
	"to_address": ar.TargetAddress(),
	"return_address": ar.Address(),
	"tunnel": ar.Boolean(),
}

ar.bind(Header, object_schema=HEADER_SCHEMA)

HEADING = ar.UserDefined(Header)
SPACE = ar.VectorOf(ar.Address())

#
#
class Relay(object):
	def __init__(self, block=None, space=None):
		self.block = block
		self.space = space

RELAY_SCHEMA = {
	"block": ar.Block(),
	"space": ar.VectorOf(ar.Address()),
}

ar.bind(Relay, object_schema=RELAY_SCHEMA)

# Conversion of messages to on-the-wire blocks, and back again.
# The deafult, fully typed, async, bidirectional messaging.
class MessageStream(object):
	def __init__(self, transport):
		self.transport = transport

		# Specific to input decoding.
		self.analysis_state = 1
		self.size_byte = bytearray()
		self.size_len = []
		self.frame_size = 0
		self.frame_byte = bytearray()

		# Inbound FSM processing of a frame.
		def s1(c):
			if c in b'0123456789,':
				nd = len(self.size_byte)
				if nd < NUMBER_OF_DIGITS:
					self.size_byte.append(c)
					return 1
				raise OverflowError(f'unlikely frame size with {nd} digits')
			elif c == 10:	# ord('\n')
				a = self.size_byte.split(b',')
				if len(a) != 3:
					raise ValueError(f'unexpected dimension')
				for b in a:
					if not b or not b.isdigit():
						raise ValueError(f'mangled frame dimensions')
				s0 = int(a[0])
				s1 = int(a[1])
				s2 = int(a[2])
				self.size_len = [s0, s1, s2]
				if s0 > s2 or (s0 + s1) > s2:
					raise ValueError(f'unlikely frame offsets')
				self.jump_size = s2
				if self.jump_size > GIANT_FRAME:
					raise OverflowError(f'oversize frame of {self.jump_size} bytes')
				elif self.jump_size == 0:
					return 3
				return 2
			raise ValueError(f'frame with unexpected {c} in digits')

		def s2(c):
			self.frame_byte.append(c)
			self.jump_size -= 1
			if self.jump_size == 0:
				return 3
			return 2

		def s3(c):
			if c == 10:
				return 0
			raise ValueError(f'unexpected {c} at end-of-frame')

		self.shift = {
			1: s1,
			2: s2,
			3: s3,
		}

	# Push a message onto the byte stream.
	def	message_to_block(self, mtr):
		m, t, r = mtr
		encoded_bytes = self.transport.encoded_bytes
		f = False
		key_box = self.transport.key_box
		codec = self.transport.codec

		# Types significant to streaming.
		# Be nice to move DH detection elsewhere.
		if isinstance(m, Blob):
			f = True
		elif isinstance(m, Diffie):
			self.transport.private_key = PrivateKey.generate()
			public_bytes = self.transport.private_key.public_key.encode()
			m.public_key = bytearray(public_bytes)
		elif isinstance(m, Hellman):
			self.transport.private_key = PrivateKey.generate()
			shared_bytes = bytes(m.public_key)
			shared_key = PublicKey(shared_bytes)
			self.transport.key_box = Box(self.transport.private_key, shared_key)
			public_bytes = self.transport.private_key.public_key.encode()
			m.public_key = bytearray(public_bytes)

		# Bring the parts together.
		# 1. Header
		h = Header(t, r, f)
		e = codec.encode(h, HEADING)
		b0 = e.encode('utf-8')
		n0 = len(b0)

		# 2. Message body - 1 of following 3.
		if f:
			b1 = m.block
			n1 = len(b1)
			s = codec.encode([], SPACE)
		elif isinstance(m, Relay):
			b1 = m.block
			n1 = len(b1)
			s = codec.encode(m.space, SPACE)
		else:
			space = []
			e = codec.encode(m, ar.Any(), space=space)
			b1 = e.encode('utf-8')
			n1 = len(b1)
			s = codec.encode(space, SPACE)

		# 3. Mutated addresses.
		b2 = s.encode('utf-8')

		# Combine into 1 and optionally encrypt.
		b0 += b1
		b0 += b2
		if key_box:
			b0 = key_box.encrypt(b0)
		n3 = len(b0)

		# Put frame on the transport.
		n = f'{n0},{n1},{n3}'
		encoded_bytes += n.encode('ascii')
		encoded_bytes += b'\n'
		encoded_bytes += b0
		encoded_bytes += b'\n'

	# Complete zero or more messages, using the given block.
	def recover_message(self, received, sockets):
		# Need a loop here because of encryption handshaking.
		codec = self.transport.codec
		upgrade = self.transport.upgrade
		remote_address = self.transport.remote_address
		diffie_hellman = self.transport.diffie_hellman

		for h, b_, a in self.recover_frame(received):
			s = h.decode('utf-8')
			header, v = codec.decode(s, HEADING)
			if v is not None:
				raise ValueError(f'header with unexpected versioning "{v}"')
			s = a.decode('utf-8')
			space, v = codec.decode(s, SPACE)

			to_address = header.to_address
			return_address = header.return_address

			if header.tunnel:					# Binary block - directly from the frame.
				body = Blob(b_)

			elif len(header.to_address) > 1:	# Passing through. Just received and headed back out.
				body = Relay(b_, space)

			else:
				# Need to recover the fully-typed message.
				s = b_.decode('utf-8')
				body, v = codec.decode(s, ar.Any(), space=space)
				if v is not None:
					if not upgrade:
						raise ValueError(f'body version "{v}" and no upgrade')
					body = upgrade(body, v)

				# Handling of encryption handshaking and keep-alives.
				if isinstance(body, Diffie):
					sockets.send(Hellman(body.public_key), remote_address)
					if not diffie_hellman:
						continue
					h = diffie_hellman[0]
					body, to_address, return_address = h
				elif isinstance(body, Hellman):
					public_bytes = bytes(body.public_key)
					public_key = PublicKey(public_bytes)
					self.transport.key_box = Box(self.transport.private_key, public_key)
					if not diffie_hellman:
						continue
					h = diffie_hellman[0]
					body, to_address, return_address = h
				elif isinstance(body, TransportEnquiry):
					body = TransportAck()
					to_address = header.return_address
					return_address = header.to_address
				else:
					pass	# Normal application messaging.

			yield body, to_address, return_address

	# Pull zero or more frames from the given block.
	def recover_frame(self, received):
		key_box = self.transport.key_box
		for c in received:
			next = self.shift[self.analysis_state](c)
			if next:
				self.analysis_state = next
				continue

			# Completed frame.
			f = bytes(self.frame_byte)
			if key_box:
				f = key_box.decrypt(f)

			# Breakout parts and yield.
			n0 = self.size_len[0]
			n1 = self.size_len[1]
			b2 = n0 + n1
			yield f[0:n0], f[n0:b2], f[b2:]

			# Restart.
			self.analysis_state = 1
			self.size_byte = bytearray()
			self.size_len = []
			self.frame_size = 0
			self.frame_byte = bytearray()

# Generic section of all network messaging.
class TcpTransport(object):
	def __init__(self, messaging_type, parent, controller_address, upgrade, opened):
		self.messaging = messaging_type(self)
		self.parent = parent
		self.controller_address = controller_address
		self.return_proxy = None
		self.local_termination = None
		self.remote_address = None

		self.codec = None

		self.pending = []			# Messages not yet in the loop.
		self.lock = thr.RLock()		# Safe sharing and empty detection.
		self.messages_to_encode = ar.deque()
		self.idling = False

		self.encoded_bytes = bytearray()

		self.diffie_hellman = None
		self.private_key = None
		self.key_box = None

		self.upgrade = upgrade

		self.opened = opened
		self.closing = False
		self.value = None

	def set_routing(self, return_proxy, local_termination, remote_address):
		# Define addresses for message forwarding.
		# return_proxy ........ address that response should go back to.
		# local_termination ... address of default target, actor or session.
		# remote_address ...... source address of connection updates, session or proxy.
		self.codec = ar.CodecJson(return_proxy=return_proxy, local_termination=local_termination)
		self.return_proxy = return_proxy
		self.local_termination = local_termination
		self.remote_address = remote_address

	# Output
	# Application to proxy.
	def put(self, m, t, r):
		try:
			self.lock.acquire()
			empty = len(self.pending) == 0
			t3 = (m, t, r)
			self.pending.append(t3)
		finally:
			self.idling = False
			self.lock.release()
		return empty

	def drain(self, a):
		try:
			self.lock.acquire()
			count = len(self.pending)
			a.extend(self.pending)
			self.pending = []
		finally:
			self.lock.release()
		return count

	# Proxy to transport.
	def send_a_block(self, s):
		t = self.queue_to_block()
		if t == 0:
			return False
		n = t if t <= TCP_SEND else TCP_SEND
		chunk = self.encoded_bytes[:n]
		n = s.send(chunk)
		if n:
			self.encoded_bytes = self.encoded_bytes[n:]
			return True
		return False

	def queue_to_block(self):
		encoded_bytes = self.encoded_bytes
		while len(encoded_bytes) < TCP_SEND:
			if len(self.messages_to_encode) == 0:
				added = self.drain(self.messages_to_encode)
				if added == 0:
					break
			# The message and to-return addresses.
			mtr = self.messages_to_encode.popleft()
			self.messaging.message_to_block(mtr)

		# Bytes available for a send.
		return len(encoded_bytes)

	# Input.
	def receive_a_message(self, received, sockets):
		for body, to_address, return_address in self.messaging.recover_message(received, sockets):
			self.idling = False
			sockets.forward(body, to_address, return_address)

#
#
class TransportTick(object):
	pass

class TransportCheck(object):
	pass

class TransportEnquiry(object):
	pass

class TransportAck(object):
	pass

ar.bind(TransportTick, copy_before_sending=False, execution_trace=False, message_trail=False)
ar.bind(TransportCheck, copy_before_sending=False, execution_trace=False, message_trail=False)
ar.bind(TransportEnquiry, copy_before_sending=False, execution_trace=False, message_trail=False)
ar.bind(TransportAck, copy_before_sending=False, execution_trace=False, message_trail=False)

IDLE_TRANSPORT = 60.0
RESPONSIVE_TRANSPORT = 5.0

class SocketKeeper(ar.Point, ar.StateMachine):
	"""Part of the watchdog function to keep network connections functional.

	Watchdog needs to run inside the socket proxy (access to transport) but
	cant because of codec processing of addresses. So this exists as a
	real address that can be used for TransportEnquiry/TransportAck
	exchanges.
	"""
	def __init__(self):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)

def SocketKeeper_INITIAL_Start(self, message):
	return NORMAL

def SocketKeeper_NORMAL_TransportEnquiry(self, message):
	# Prompted by the proxy, send the enquiry with this
	# object as the return address.
	self.send(message, self.parent_address)
	return NORMAL

def SocketKeeper_NORMAL_TransportAck(self, message):
	# Acknowledgement of the enquiry - push to the
	# true client, i.e. the proxy.
	self.send(message, self.parent_address)
	return NORMAL

def SocketKeeper_NORMAL_Stop(self, message):
	self.complete()

SOCKET_KEEPER_DISPATCH = {
	INITIAL: (
		(ar.Start,),
		()
	),
	NORMAL: (
		(TransportEnquiry, TransportAck, ar.Stop),
		()
	),
}

ar.bind(SocketKeeper, SOCKET_KEEPER_DISPATCH, thread='keeper', execution_trace=False)

#
#
class SocketProxy(ar.Point, ar.StateMachine):
	"""Local representation of an object at remote end of a network connection.

	:param s: associated network connection
	:type s: socket descriptor
	:param channel: async socket loop
	:type channel: internal
	:param transport: associated buffering
	:type transport: internal
	"""
	def __init__(self, s, channel, transport, self_checking=False):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.s = s
		self.channel = channel
		self.transport = transport
		self.self_checking = self_checking
		self.keeper = None
		self.checked = 0
	
	def first_few(self):
		if self.checked > 12:
			return False
		self.checked += 1
		return True

SOCKET_DOWN = (errno.ECONNRESET, errno.EHOSTDOWN, errno.ENETDOWN, errno.ENETRESET)

def SocketProxy_INITIAL_Start(self, message):
	if self.self_checking:
		self.keeper = self.create(SocketKeeper)
		self.start(TransportTick, IDLE_TRANSPORT, repeating=True)
	return NORMAL

#
#
def SocketProxy_NORMAL_Unknown(self, message):
	empty = self.transport.put(message, self.to_address, self.return_address)
	if empty:
		self.channel.send(Bump(self.s), self.address)
	return NORMAL

def SocketProxy_NORMAL_TransportTick(self, message):
	if self.transport.idling:
		# Too much time with no activity. Perform
		# an enquiry/ack verification that transport is
		# still functional.
		if self.first_few():
			self.log(ar.TAG_CONSOLE, f'Transport idle, send TransportEnquiry and start timer')
		self.send(TransportEnquiry(), self.keeper)
		self.start(TransportCheck, RESPONSIVE_TRANSPORT)
		return CHECKING
	self.transport.idling = True
	return NORMAL

def SocketProxy_NORMAL_Close(self, message):
	self.channel.send(Shutdown(self.s, message.value), self.address)
	if self.self_checking:
		self.send(ar.Stop(), self.keeper)
		return CLEARING
	self.complete()

def SocketProxy_NORMAL_Stop(self, message):
	self.channel.send(Shutdown(self.s), self.address)
	if self.self_checking:
		self.send(ar.Stop(), self.keeper)
		return CLEARING
	self.complete()

#
#
def SocketProxy_CHECKING_Unknown(self, message):
	empty = self.transport.put(message, self.to_address, self.return_address)
	if empty:
		self.channel.send(Bump(self.s), self.address)
	return CHECKING

def SocketProxy_CHECKING_TransportTick(self, message):
	# Ignore in this state.
	return CHECKING

def SocketProxy_CHECKING_TransportAck(self, message):
	# Transport verified. Return to normal operation.
	if self.first_few():
		self.log(ar.TAG_CONSOLE, f'Received TransportAck, return to normal operation')
	self.cancel(TransportCheck)
	self.transport.idling = False
	return NORMAL

def SocketProxy_CHECKING_TransportCheck(self, message):
	# No acknowledgement within time limit. Close
	# this connection down.
	if self.first_few():
		self.log(ar.TAG_CONSOLE, f'Timed out, close transport')
	self.channel.send(Shutdown(self.s, ar.TimedOut(message)), self.address)
	self.send(ar.Stop(), self.keeper)
	return CLEARING

def SocketProxy_CHECKING_Close(self, message):
	self.channel.send(Shutdown(self.s, message.value), self.address)
	self.send(ar.Stop(), self.keeper)
	return CLEARING

def SocketProxy_CHECKING_Stop(self, message):
	self.send(ar.Stop(), self.keeper)
	return CLEARING

def SocketProxy_CLEARING_Completed(self, message):
	self.cancel(TransportTick)
	self.complete()

TCP_PROXY_DISPATCH = {
	INITIAL: (
		(ar.Start,),
		()
	),
	NORMAL: (
		(ar.Unknown, TransportTick, Close, ar.Stop),
		()
	),
	CHECKING: (
		(ar.Unknown, TransportTick, TransportAck, TransportCheck, Close, ar.Stop),
		()
	),
	CLEARING: (
		(ar.Completed,),
		()
	),
}

ar.bind(SocketProxy, TCP_PROXY_DISPATCH, thread='socketry')

#
#
class Diffie(object):
	def __init__(self, public_key=None):
		self.public_key = public_key

class Hellman(object):
	def __init__(self, public_key=None):
		self.public_key = public_key

DH_SCHEMA = {
	'public_key': ar.Block(),
}

ar.bind(Diffie, object_schema=DH_SCHEMA, copy_before_sending=False)
ar.bind(Hellman, object_schema=DH_SCHEMA, copy_before_sending=False)



# Signals from the network represented
# as distinct classes - for dispatching.
class ReceiveBlock: pass
class ReadyToSend: pass
class BrokenTransport: pass

# CONTROL CHANNEL
# First two functions are for handling the 1-byte events
# coming across the control socket.
def ControlChannel_ReceiveBlock(self, control, s):
	s.recv(1)					   # Consume the bump.
	mr = self.pending.get()	# Message and account.

	# This second jump is to simulate the common handling of control
	# channel events and select events.
	c = type(mr[0])
	try:
		f = select_table[(ControlChannel, c)]
	except KeyError:
		self.fault('Unknown signal received at control channel (%s).' % (c.__name__,))
		return
	f(self, control, mr)

def ControlChannel_BrokenTransport(self, control, s):
	self.fault('The control channel to the selector is broken.')
	self.clear(s, ControlChannel)

# The rest of them handle the simulated receive of the
# actual message.

def ControlChannel_ListenForStream(self, control, mr):
	m, r = mr
	requested_ipp = m.requested_ipp
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		self.send(NotListening(requested_ipp, e.errno, str(e)), r)
		return

	def server_not_listening(e):
		server.close()
		self.send(NotListening(requested_ipp, e.errno, str(e)), r)

	try:
		server.setblocking(False)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.bind(requested_ipp.inet())
		server.listen(5)
	except socket.herror as e:
		server_not_listening(e)
		return
	except socket.gaierror as e:
		server_not_listening(e)
		return
	except socket.error as e:
		server_not_listening(e)
		return
	except OverflowError as e:
		server.close()
		self.send(NotListening(requested_ipp, 0, str(e)), r)
		return

	hap = server.getsockname()
	listening_ipp=HostPort(hap[0], hap[1])

	if m.encrypted:
		self.trace(f'Listening (encrypted) on "{listening_ipp}", requested "{requested_ipp}"')
	else:
		self.trace(f'Listening on "{listening_ipp}", requested "{requested_ipp}"')

	listening = Listening(listening_address=r, requested_ipp=requested_ipp,
		listening_ipp=listening_ipp,
		encrypted=m.encrypted)

	self.networking[server] = TcpServer(server, m, listening, r, m.upgrade)
	self.receiving.append(server)
	self.faulting.append(server)

	self.send(listening, r)

def no_ending(value, parent, address):
	pass

def close_ending(proxy):
	def ending(value, parent, address):
		ar.send_a_message(Close(value), proxy, address)
	return ending

def open_stream(self, parent, s, opened):
	controller_address = parent.controller_address
	self_checking = False
	ts = MessageStream

	if isinstance(parent, TcpClient):
		self_checking = parent.self_checking
		if parent.request.api_client:
			ts = ApiClientStream
	elif isinstance(parent, TcpServer):
		if parent.request.api_server is not None:
			ts = ApiServerStream

	transport = TcpTransport(ts, parent, controller_address, parent.upgrade, opened)
	proxy_address = self.create(SocketProxy, s, self.channel, transport, self_checking=self_checking, object_ending=no_ending)

	cs = parent.request.create_session
	if cs:
		# Create the ending function that swaps the Completed message to the parent for a
		# Close message to the proxy.

		ending = close_ending(proxy_address)
		session_address = self.create(cs.object_type, *cs.args,
			controller_address=controller_address, remote_address=proxy_address,
			object_ending=ending,
			**cs.kw)
		transport.set_routing(proxy_address, session_address, session_address)
	elif ts == ApiClientStream:
		ending = close_ending(proxy_address)
		session_address = self.create(ApiClientSession,
			controller_address=controller_address, remote_address=proxy_address,
			object_ending=ending)
		transport.set_routing(proxy_address, session_address, session_address)
	else:
		transport.set_routing(proxy_address, controller_address, proxy_address)

	self.networking[s] = transport
	return transport, proxy_address

def ControlChannel_ConnectStream(self, control, mr):
	m, r = mr
	requested_ipp = m.requested_ipp
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.setblocking(False)
	except socket.error as e:
		self.send(NotConnected(requested_ipp, e.errno, str(e)), r)
		return

	def client_not_connected(e):
		client.close()
		self.send(NotConnected(requested_ipp, e.errno, str(e)), r)

	try:
		e = client.connect_ex(requested_ipp.inet())
		if e:
			# Connect request cannot complete. Check for codes indicating
			# async issue. If not it's a real error.
			if e not in (errno.EINPROGRESS, errno.EWOULDBLOCK, errno.EAGAIN):
				client.close()
				self.send(NotConnected(requested_ipp, e, 'Connect incomplete and no pending indication.'), r)
				return

			# Build a transient "session" that just exists to catch
			# an initial, either send or fault (a receive is treated
			# as an error). True session is constructed on receiving
			# a "normal" send event.
			pending = TcpClient(client, m, None, r, m.upgrade, m.encrypted, m.self_checking)

			self.networking[client] = pending
			self.receiving.append(client)
			self.sending.append(client)
			self.faulting.append(client)
			return

	except socket.herror as e:
		client_not_connected(e)
		return
	except socket.gaierror as e:
		client_not_connected(e)
		return
	except socket.error as e:
		client_not_connected(e)
		return
	except OverflowError as e:
		client.close()
		self.send(NotConnected(requested_ipp, 0, str(e)), r)
		return

	hap = client.getsockname()
	connected_ipp = HostPort(hap[0], hap[1])

	connected = Connected(requested_ipp=requested_ipp,
		connected_ipp=connected_ipp,
		opened_at=ar.world_now())

	parent = TcpClient(client, m, connected, r, m.upgrade, m.encrypted, m.self_checking)
	transport, proxy_address = open_stream(self, parent, client, connected)
	connected.remote_address = proxy_address

	self.networking[client] = transport
	self.receiving.append(client)
	self.sending.append(client)
	self.faulting.append(client)

	if m.encrypted:
		self.trace(f'Connected (encrypted) to "{requested_ipp}", at local address "{connected_ipp}"')
		not_connected = NotConnected(requested_ipp, None, None)
		transport.diffie_hellman = (
			(connected, r, transport.remote_address),
			(not_connected, r))
		# Start the exchange. Public key filled out during
		# streaming.
		self.send(Diffie(), proxy_address)
		return
	self.trace(f'Connected to "{requested_ipp}", at local address ""{connected_ipp}"')

	self.forward(connected, r, transport.remote_address)

def ControlChannel_StopListening(self, control, mr):
	m, r = mr
	listening_ipp = m.listening_ipp
	def server(t):
		if not isinstance(t, TcpServer):
			return False
		h = t.listening.listening_ipp.host == listening_ipp.host
		p = t.listening.listening_ipp.port == listening_ipp.port
		return h and p

	# Find server belonging to sender
	# and clear from engine.
	sockets = [k for k, v in self.networking.items() if server(v)]
	if len(sockets) == 1:
		self.clear(sockets[0], TcpServer)
		text = 'stopped "%s"(%d)' % (listening_ipp.host, listening_ipp.port)
	else:
		text = 'not listening to "%s"(%d)' % (listening_ipp.host, listening_ipp.port)
	self.send(NotListening(listening_ipp, 0, text), r)

def ControlChannel_Stop(self, control, mr):
	m, r = mr
	def soc(p): # Server or client.
		return isinstance(p, (TcpServer, TcpClient))

	# Clear any servers and clients. Not
	# accepting or connecting any more.
	sockets = [k for k, v in self.networking.items() if soc(v)]
	for s in sockets:
		self.clear(s)

	# Only streams left. Except control channel. Sigh.
	# Kick off a proper teardown and wait until the handshaking
	# is done and there is nothing left to do.
	for k, v in self.networking.items():
		if isinstance(v, TcpTransport):
			# WAS Closed() but that certainly doesnt work
			# for session-based connections.
			self.send(ar.Stop(), v.remote_address)

	self.running = False

def ControlChannel_Bump(self, control, mr):
	m, r = mr
	if m.s.fileno() < 0:
		# Catches the situation where the socket has been abandoned
		# by the remote and the notification to the proxy arrives behind
		# the bump.
		return
	try:
		self.sending.index(m.s)
		return
	except ValueError:
		pass
	self.sending.append(m.s)

def ControlChannel_Shutdown(self, control, mr):
	m, r = mr
	try:
		transport = self.networking[m.s]
	except KeyError:
		# Already cleared by Abandoned codepath.
		return
	transport.closing = True
	transport.value = m.value
	m.s.shutdown(socket.SHUT_RD)

# Dispatch of socket signals;
# - ReceiveBlock ...... there are bytes to recv
# - ReadyToSend ....... an opportunity to send
# - BrokenTransport ... error on socket
# and server/client/connection;
# - TcpServer ......... listen waiting to accept
# - TcpClient ......... partial connect
# - TcpTransport ......... established connection

def TcpServer_ReceiveBlock(self, server, s):
	listening = server.listening
	try:
		accepted, hap = s.accept()
		accepted.setblocking(False)
	except socket.error as e:
		self.send(NotAccepted(listening.requested_ipp, e.errno, str(e)), server.controller_address)
		return

	opened_at = ar.world_now()
	transport, proxy_address = open_stream(self, server, accepted, None)
	self.receiving.append(accepted)
	self.sending.append(accepted)
	self.faulting.append(accepted)

	accepted_ipp = HostPort(hap[0], hap[1])

	accepted = Accepted(listening_address=listening.listening_address, listening_ipp=listening.listening_ipp,
		accepted_ipp=accepted_ipp, remote_address=transport.remote_address,
		opened_at=opened_at)
	transport.opened = accepted

	if listening.encrypted:
		self.trace(f'Accepted (encrypted) "{accepted_ipp}", requested "{listening.listening_ipp}"')
		not_accepted = NotAccepted(listening.requested_ipp, None, None)
		transport.diffie_hellman = (
			(accepted, server.controller_address, transport.remote_address),
			(not_accepted, server.controller_address))
		return
	self.trace(f'Accepted "{accepted_ipp}", requested "{listening.listening_ipp}"')

	self.forward(accepted, server.controller_address, transport.remote_address)

def TcpServer_BrokenTransport(self, server, s):
	listening = server.listening
	self.send(NotListening(listening.listening_ipp, 0, "signaled by networking subsystem"), server.controller_address)
	self.clear(s, TcpServer)

# TCP CLIENT
# A placeholder for the eventual outbound transport.
def TcpClient_ReceiveBlock(self, selector, s):
	client = s
	# NOT NEEDED IN TcpTransport_ReceiveBlock SO....
	#self.sending.remove(client)

	request = selector.request

	hap = client.getsockname()
	connected_ipp = HostPort(hap[0], hap[1])
	requested_ipp = request.requested_ipp

	# CANNOT BUILD A STREAM AND IMMEDIATELY TEAR IT DOWN ON AN EXCEPTION.
	# THIS WILL MAY CREATE A SESSION OBJECT WHEN THERE IS NO REMOTE AND MAY
	# NEVER BE. DO IT AFTER A SUCCESSFUL RECV().
	#connected = Connected(requested_ipp=request.requested_ipp,
	#	connected_ipp=HostPort(hap[0], hap[1]),
	#	opened_at=ar.world_now())
	#selector.connected = connected

	#transport, proxy_address = open_stream(self, selector, client, connected.opened_at)
	#connected.remote_address = proxy_address

	try:
		scrap = s.recv(TCP_RECV)

		# No exception. New transport.
		connected = Connected(requested_ipp=requested_ipp,
			connected_ipp=connected_ipp,
			opened_at=ar.world_now())

		selector.connected = connected
		transport, proxy_address = open_stream(self, selector, client, connected)
		connected.remote_address = proxy_address

		self.trace(f'Connected to "{requested_ipp}", at local address "{connected_ipp}"')

		if selector.encrypted:
			self.trace(f'Connected (encrypted) to "{requested_ipp}", at local address "{connected_ipp}"')
			not_connected = NotConnected(requested_ipp, None, None)
			transport.diffie_hellman = (
				(connected, transport.controller_address, transport.remote_address),
				(not_connected, selector.controller_address))
			self.send(Diffie(), proxy_address)
			return
		self.trace(f'Connected to "{requested_ipp}", at local address "{connected_ipp}"')

		self.forward(connected, transport.controller_address, transport.remote_address)

		if not scrap:
			# Immediate shutdown. Need to
			# generate the full set of messages.
			#self.clear(s, TcpTransport)
			return

		try:
			transport.receive_a_message(scrap, self)
		except (ar.CodecFailed, OverflowError, ValueError) as e:
			value = ar.Faulted(condition='cannot stream inbound', explanation=str(e))
			self.warning(str(value))
			close_session(transport, value, s)
		return

	except socket.error as e:
		self.send(NotConnected(request.requested_ipp, e.errno, str(e)), selector.controller_address)
		self.clear(s, TcpClient)
		#self.send(NotConnected(request.requested_ipp, e.errno, str(e)), transport.controller_address)
		#self.send(ar.Stop(), transport.remote_address)
		#self.clear(s, TcpTransport)
		return

def TcpClient_ReadyToSend(self, selector, s):
	client = s
	#self.sending.remove(client)

	request = selector.request
	hap = client.getsockname()
	connected_ipp = HostPort(hap[0], hap[1])
	requested_ipp = request.requested_ipp

	connected = Connected(requested_ipp=requested_ipp,
		connected_ipp=connected_ipp,
		opened_at=ar.world_now())
	selector.connected = connected

	transport, proxy_address = open_stream(self, selector, client, connected)
	connected.remote_address = proxy_address
	#receiving.append( client)
	#self.faulting.append( client)

	if selector.encrypted:
		self.trace(f'Connected (encrypted) to "{requested_ipp}", at local address "{connected_ipp}"')
		not_connected = NotConnected(requested_ipp, None, None)
		transport.diffie_hellman = (
			(connected, transport.controller_address, transport.remote_address),
			(not_connected, selector.controller_address))
		# Start the exchange of public keys.
		self.send(Diffie(), proxy_address)
		return
	self.trace(f'Connected to "{requested_ipp}", at local address "{connected_ipp}"')

	self.forward(connected, transport.controller_address, transport.remote_address)

def TcpClient_BrokenTransport(self, selector, s):
	text = 'fault on pending connect, unreachable, no service at that address or blocked'
	self.send(NotConnected(selector.requested_ipp, 0, text), selector.controller_address)
	self.clear(s, TcpClient)

def close_session(transport, value, s):
	transport.closing = True
	transport.value = value
	s.shutdown(socket.SHUT_RDWR)

def end_of_session(self, transport, s, reason=None):
	if isinstance(transport.opened, Connected):
		ipp = transport.opened.connected_ipp
	elif isinstance(transport.opened, Accepted):
		ipp = transport.opened.accepted_ipp
	else:
		ipp = None

	if transport.closing:
		c = Closed(value=transport.value,
			reason=reason,
			opened_ipp=ipp,
			opened_at=transport.opened.opened_at)
		self.forward(c, transport.controller_address, transport.remote_address)
	else:
		self.send(ar.Stop(), transport.remote_address)
		a = Abandoned(opened_ipp=ipp,
			opened_at=transport.opened.opened_at)
		self.forward(a, transport.controller_address, transport.remote_address)
	self.clear(s, TcpTransport)

def TcpTransport_ReadyToSend(self, transport, s):
	try:
		if transport.send_a_block(s):
			return
	except (ar.CodecFailed, OverflowError, ValueError) as e:
		value = ar.Faulted(condition='cannot stream outbound', explanation=str(e))
		self.warning(str(value))
		close_session(transport, value, s)
		return

	try:
		self.sending.remove(s)
	except ValueError:
		pass

# A network transport for the purpose of exchanging
# messages between machines.

def TcpTransport_ReceiveBlock(self, transport, s):
	try:
		scrap = s.recv(TCP_RECV)
		if not scrap:
			end_of_session(self, transport, s, 'empty socket')
			return

		try:
			transport.receive_a_message(scrap, self)
		except (ar.CodecFailed, OverflowError, ValueError) as e:
			value = ar.Faulted(condition='cannot stream inbound', explanation=str(e))
			self.warning(str(value))
			close_session(transport, value, s)
		return

	except socket.error as e:
		if e.errno == errno.ECONNREFUSED:
			self.fault('Connection refused')
		elif e.errno not in SOCKET_DOWN:
			self.fault('Socket termination [%d] %s' % (e.errno, e.strerror))
		end_of_session(self, transport, s, reason=e.strerror)
		return

def TcpTransport_BrokenTransport(self, selector, s):
	end_of_session(self, selector, s, reason='broken socket')

#
#
def control_channel():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(False)
	server.bind(("127.0.0.1", 0))
	server.listen(1)

	server_address = server.getsockname()

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.setblocking(False)
	e = client.connect_ex(server_address)

	readable, writable, exceptional = select.select([server], [], [server])
	if not readable:
		client.close()
		server.close()
		raise RuntimeError('Forming control channel, select has not received connect notification.')

	accepted, client_address = server.accept()
	accepted.setblocking(False)

	accept_address = accepted.getsockname()

	return server, accepted, client

def control_close(lac):
	# Close the listen and the connect. Accepted
	# will be closed by SocketSelect.
	lac[2].close()
	lac[0].close()

#
#
BUMP = b'X'

class SocketChannel(object):
	def __init__(self, pending=None, client=None):
		'''
		This is the per-object client end of the control
		channel into the network I/O loop.
		'''
		self.pending = pending
		self.client = client

	def send(self, message, address):
		self.pending.put((message, address))
		buffered = self.client.send(BUMP)
		if buffered != 1:
			raise RuntimeError('Control channel not accepting commands.')

# Damn. Sent from sockets thread to creator. They
# need it to inject messages into loop.
SOCKET_CHANNEL_SCHEMA = {
	'pending': ar.Any,
	'client': ar.Any,
}

ar.bind(SocketChannel, object_schema=SOCKET_CHANNEL_SCHEMA, copy_before_sending=False)

#
#
select_table = {
	# Handling of inbound control messages.
	(ControlChannel, ReceiveBlock):	 ControlChannel_ReceiveBlock,		# Signals down the control channel.
	(ControlChannel, BrokenTransport):  ControlChannel_BrokenTransport,

	# Made to look as if the select thread can actually receive
	# sockets signals and application messages. Called from above.
	(ControlChannel, ListenForStream):  ControlChannel_ListenForStream,		# Process signals to sockets.
	(ControlChannel, ConnectStream):	ControlChannel_ConnectStream,
	(ControlChannel, Shutdown):		 ControlChannel_Shutdown,
	(ControlChannel, Bump):			 ControlChannel_Bump,
	(ControlChannel, StopListening):	ControlChannel_StopListening,
	(ControlChannel, ar.Stop):		  ControlChannel_Stop,

	# Operational sockets
	(TcpServer,	ReceiveBlock):	   TcpServer_ReceiveBlock,			# Accept inbound connections.
	(TcpServer,	BrokenTransport):	TcpServer_BrokenTransport,

	(TcpClient,   ReceiveBlock):		TcpClient_ReceiveBlock,			# Deferred connections.
	(TcpClient,   ReadyToSend):		 TcpClient_ReadyToSend,
	(TcpClient,   BrokenTransport):	 TcpClient_BrokenTransport,

	(TcpTransport,   ReceiveBlock):		TcpTransport_ReceiveBlock,
	(TcpTransport,   ReadyToSend):		 TcpTransport_ReadyToSend,
	(TcpTransport,   BrokenTransport):	 TcpTransport_BrokenTransport,
}

class SocketSelect(ar.Threaded, ar.Stateless):
	def __init__(self):
		ar.Threaded.__init__(self)
		ar.Stateless.__init__(self)

		# Construct the control channel and access object.
		self.pending = sq.Queue()
		self.lac = control_channel()
		self.channel = SocketChannel(self.pending, self.lac[2])

		# Load control details into socket tables.
		self.listening = self.lac[0]
		self.accepted = self.lac[1]
		self.networking = {
			self.accepted: ControlChannel(self.accepted),	# Receives 1-byte BUMPs.
		}

		# Active socket lists for select.
		self.receiving = [self.accepted]
		self.sending = []
		self.faulting = self.receiving + self.sending

		# Live.
		self.running = True

	def clear(self, s, expected=None):
		# Remove the specified socket from operations.
		try:
			t = self.networking[s]
		except KeyError:
			self.warning('Attempt to remove unknown socket')
			return None

		if expected and not isinstance(t, expected):
			self.warning('Unexpected networking object "%s" (expecting "%s")' % (t.__class__.__name__, expected.__name__))
			return None

		del self.networking[s]
		try:
			self.receiving.remove(s)
		except ValueError:
			pass
		try:
			self.sending.remove(s)
		except ValueError:
			pass
		try:
			self.faulting.remove(s)
		except ValueError:
			pass
		s.close()
		return t

def SocketSelect_Start(self, message):
	# Provide channel details to parent for access
	# by application.
	self.send(self.channel, self.parent_address)

	def clean_sockets():
		self.receiving = [s for s in self.receiving if s.fileno() > -1]
		self.sending = [s for s in self.receiving if s.fileno() > -1]
		self.faulting = [s for s in self.receiving if s.fileno() > -1]

	while self.running or len(self.networking) > 1:
		R, S, F = select.select(self.receiving, self.sending, self.faulting)

		# IF FAILS
		# for every socket in every list --- select([sock],[],[],0)
		# to find which one has failed.

		for r in R:
			try:
				#h = id(r)
				#if h in self.handshaking:
				#	r.do_handshake()
				#	self.handshaking.discard(h)
				#	continue

				a = self.networking[r]
				c = a.__class__
				j = select_table[(c, ReceiveBlock)]
			except KeyError:
				continue
			except ValueError:
				#clean_sockets()
				continue
			j(self, a, r)

		for s in S:
			try:
				#h = id(s)
				#if h in self.handshaking:
				#	s.do_handshake()
				#	self.handshaking.discard(h)
				#	continue

				a = self.networking[s]
				c = a.__class__
				j = select_table[(c, ReadyToSend)]
			except KeyError:
				continue
			except ValueError:
				#clean_sockets()
				continue
			j(self, a, s)

		for f in F:
			try:
				#h = id(f)
				#if h in self.handshaking:
				#	f.do_handshake()
				#	self.handshaking.discard(h)
				#	continue

				a = self.networking[f]
				c = a.__class__
				j = select_table[(c, BrokenTransport)]
			except KeyError:
				continue
			except ValueError:
				#clean_sockets()
				continue
			j(self, a, f)

	control_close(self.lac)
	self.complete()

ar.bind(SocketSelect, (ar.Start,))
