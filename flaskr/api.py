from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .gpt import AssistantAPI
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('api', __name__, url_prefix='/api')
ass = AssistantAPI()

@bp.route('/gen',methods=['POST'])
def gen():
    if request.method == 'POST':
        chat_request = request.json
        if chat_request:
            try:
                logging.info(chat_request[-1])
                response = ass.process_user_request(chat_request)
                logging.info(" --> Response: \"" + response + "\"")
                return response, 200
            except Exception as e:
                logging.error(chat_request)
                logging.error(e)
                return 'Internal Server Error', 500
        else:
            return 'The request of the user is empty', 400