# -*- coding: utf-8 -*-
"""Entry point and option parsing for messenging-only support program."""

from __future__ import annotations

import smtplib
import time
from email.headerregistry import Address
from email.message import EmailMessage
from typing import Iterable, Optional, Sequence
import os


class InvalidReceiverEmailAddress(Exception):
	pass


def to_email_address_object(
	email_address: str, display_name: str, default_email_domain: Optional[str] = None
) -> Address:
	"""
	Converts given email_address and display_name string into an email.headerregistry.Address object .
	"""
	aux: Sequence[str] = email_address.split("@", 2)
	if len(aux) < 2:
		if default_email_domain and (len(aux) == 1):
			aux = (aux[0], default_email_domain)
		else:
			raise InvalidReceiverEmailAddress(email_address)
	return Address(display_name, aux[0], aux[1])


class AttachmentContent:
	"""
	AttachmentContent represent the content of an attachment file.
	"""

	__slots__ = (
		"data",
		"main_type",
		"sub_type",
		"filename",
	)

	def __init__(
		self, data: bytes, main_type: str, sub_type: str, filename: str
	) -> None:
		"""
		:param data: The content of the attachment.
		:param main_type: Main MIME type of the attachment (eg: `text`).
		:param sub_type: Sub MIME type of the attachment (eg: `html`).
		:param filename: The name of the attachment file.
		"""
		self.data = data
		self.main_type = main_type
		self.sub_type = sub_type
		self.filename = filename


class EmailMessenger:
	__slots__ = (
		"_sender_address",
		"_smtp_host",
		"_smtp_port",
		"_smtp_tls",
		"_smtp_timeout",
		"_output_path",
		"_output_name_prefix",
	)

	def __init__(
		self,
		sender_address: Address,
		smtp_host: str,
		smtp_port: int,
		smtp_tls: bool = False,
		smtp_timeout: float = 15.0,
		output_path: Optional[str] = None,
		output_name_prefix: str = "m-",
	):
		self._sender_address = sender_address
		if not smtp_host:
			self._smtp_host: Optional[str] = None
			self._smtp_port: int = 0
			self._smtp_tls: bool = False
			self._smtp_timeout: float = smtp_timeout
		elif smtp_host[0] == "/":
			self._smtp_host = None
			self._smtp_port = 0
			self._smtp_tls = False
			self._smtp_timeout = smtp_timeout
			if not output_path:
				output_path = smtp_host
		else:
			self._smtp_host = smtp_host
			self._smtp_port = smtp_port
			self._smtp_tls = smtp_tls
			self._smtp_timeout = smtp_timeout
		self._output_path = os.path.abspath(output_path) if output_path else None
		if self._output_path:
			os.makedirs(self._output_path, 0o700, exist_ok=True)
		self._output_name_prefix = output_name_prefix

	def make_message(
		self,
		receiver_addresses: Iterable[Address],
		subject_text: str,
		body_plain_text: str,
		body_html: str,
		attachments: Optional[Iterable[AttachmentContent]] = None,
	) -> EmailMessage:
		msg = EmailMessage()
		msg["From"] = self._sender_address
		msg["To"] = receiver_addresses
		msg["Subject"] = subject_text
		msg.set_content(body_plain_text, cte="8bit")
		msg.add_alternative(body_html, subtype="html")
		if attachments:
			for a in attachments:
				msg.add_attachment(
					a.data,
					maintype=a.main_type,
					subtype=a.sub_type,
					filename=a.filename,
				)
		return msg

	def send_message(self, msg: EmailMessage):
		if self._output_path:
			filename = self._output_name_prefix + str(int(time.time() * 1000))
			with open(os.path.join(self._output_path, filename), "wb") as fp:
				fp.write(bytes(msg))
		if self._smtp_host:
			if self._smtp_tls:
				with smtplib.SMTP_SSL(
					self._smtp_host, self._smtp_port, timeout=self._smtp_timeout
				) as s:
					s.send_message(msg)
			else:
				with smtplib.SMTP(
					self._smtp_host, self._smtp_port, timeout=self._smtp_timeout
				) as s:
					s.send_message(msg)
