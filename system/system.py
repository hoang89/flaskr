from flask import Blueprint, render_template, abort, request, json, logging, redirect, url_for
from flask.globals import current_app as APP
from constant import *

system_information = Blueprint('system', __name__)

def wrong_param(message):
    data = {
        'status': PARAM_NOT_MATCH,
        'message': message,
        'error_code': 0
    }
    return json.jsonify(**data)

@system_information.route('/system/information')
@system_information.route('/system/information/<device_id>')
def information(device_id=''):
    if device_id == '':
        return wrong_param('Please submit device_id');
    res = {
        'android_version': 1.0,
        'ios_version': 1,
        'maintain': False
    }
    data = {
        'status': 1,
        'message': '',
        'error_code': 0,
        'data': res
    }
    return json.jsonify(**data)

@system_information.route('/system/maintain')
def maintain():
    data = {
        'status': 1,
        'message': '',
        'error_code': 0,
        'maintain': False
    }
    return json.jsonify(**data)