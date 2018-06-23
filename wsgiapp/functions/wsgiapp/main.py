# coding: utf-8

import sys
import pathlib
import awsgi
from wsgiapp.main import app

vendor_path = str(pathlib.Path('./vendor').absolute())
sys.path.append(vendor_path)


def lambda_handler(event, context):
    return awsgi.response(app, event, context)
