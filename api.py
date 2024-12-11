from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from gpt import AssistantAPI

bp = Blueprint('api', __name__, url_prefix='/api')

ass = AssistantAPI()

@bp.route('/gen',methods=['POST'])
def gen():
    if request.method == 'POST':
        user_request = request.form['content']
        if user_request:
            return ass.process_user_request(user_request)
        else: 
            return 'The request of the user is empty.', 400