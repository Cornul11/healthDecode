import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv

from summarizer import get_summary

from utils import get_param_util, get_title
from utils import get_visual_summary
from utils import get_text_from_file, get_lab_result_refs

app = Flask(__name__)
CORS(app)

load_dotenv()


@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':
        return 'Hello, World!'


@app.route('/analyzeLabResults', methods=['POST'])
def analyze_lab_results():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save('uploads/' + uploaded_file.filename)
        print(get_lab_result_refs('uploads/' + uploaded_file.filename))
    return jsonify(string=get_lab_result_refs('uploads/' + uploaded_file.filename))


@app.route('/analyzeDiagnosis', methods=['POST'])
def analyze_diagnosis():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save('uploads/' + uploaded_file.filename)
        print(get_text_from_file('uploads/' + uploaded_file.filename))
    return jsonify(string=get_text_from_file('uploads/' + uploaded_file.filename))


@app.route('/analysis', methods=['GET'])
def get_summary_text():
    if request.method == 'GET':
        url = request.args.get('url')
        return jsonify(string=get_summary(url), title=get_title(url))
    return "Not opening!"


@app.route('/GetTokenAndSubdomain', methods=['GET'])
def get_token_and_subdomain():
    """Get the access token"""
    if request.method == 'GET':
        try:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            data = {
                'client_id': str(os.environ.get('CLIENT_ID')),
                'client_secret': str(os.environ.get('CLIENT_SECRET')),
                'resource': 'https://cognitiveservices.azure.com/',
                'grant_type': 'client_credentials'
            }

            resp = requests.post('https://login.windows.net/' + str(os.environ.get('TENANT_ID')) + '/oauth2/token',
                                 data=data, headers=headers)
            json_resp = resp.json()

            if 'access_token' not in json_resp:
                print(json_resp)
                raise Exception('AAD Authentication error')

            token = json_resp['access_token']
            subdomain = str(os.environ.get('SUBDOMAIN'))

            return jsonify(token=token, subdomain=subdomain)
        except Exception as e:
            message = 'Unable to acquire Azure AD token. Check the debugger for more information.'
            print(message, e)
            return jsonify(error=message)


@app.route('/image-to-text/<filename>', methods=['GET'])
def image_to_text(filename):
    if request.method == 'GET':
        return get_text_from_file(str(filename) + '.pdf')
    return "Not opening!"


@app.route('/visual-summary/<filename>', methods=['GET'])
def get_visual(filename):
    if request.method == 'GET':
        return get_visual_summary(filename + '.pdf')
    return "Not opening!"


@app.route('/diagnosis/<filename>', methods=['GET'])
def get_diagnosis(filename):
    if request.method == 'GET':
        return get_param_util(filename + '.pdf', 'Diagnosis')
    return "Not opening!"


@app.route('/treatment/<filename>', methods=['GET'])
def get_treatment(filename):
    if request.method == 'GET':
        return get_param_util(filename + '.pdf', 'Treatment')
    return "Not opening!"
