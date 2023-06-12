#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :redprint.py
@说明        :
@时间        :2020/12/18 20:22:21
'''

class Redprint:
    """docstring for Redprint."""
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        '''实现redprint向blueprint的注册'''
        def decorator(f):
            self.mound.append((f, rule, options))
            return f
        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            endpoint = options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)