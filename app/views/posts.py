from flask import render_template, request, flash, get_flashed_messages, Blueprint, redirect, url_for, jsonify

posts = Blueprint('posts', __name__)


@posts.route('/collect/<pid>')
def collect(pid):
    return jsonify({'result': 'ok'})
