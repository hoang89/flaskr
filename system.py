__author__ = 'hoangnn'

from flask import Flask, request, session, g, redirect, url_for, abort, render_template,flash

@app.route('/system/information')
def information():
    return "this is information of system"