#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from flask_mail import Message,Mail

mail = Mail()

def send_email(to, subject, template):
    msg = Message()

