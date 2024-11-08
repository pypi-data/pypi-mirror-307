# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import random
import sys
import os
import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')

import flask
from flask import Flask, request, send_from_directory, redirect, url_for
from flask import stream_with_context, Response
import html
import pandas as pd

import webbrowser
import threading

from flask_cors import CORS

import json
import time
from pathlib import Path

from vega_datasets import data as vega_data

from data_formulator.agents.agent_concept_derive import ConceptDeriveAgent
from data_formulator.agents.agent_data_transform_v2 import DataTransformationAgentV2
from data_formulator.agents.agent_data_rec import DataRecAgent

from data_formulator.agents.agent_sort_data import SortDataAgent
from data_formulator.agents.agent_data_load import DataLoadAgent
from data_formulator.agents.agent_data_clean import DataCleanAgent
from data_formulator.agents.agent_code_explanation import CodeExplanationAgent

from data_formulator.agents.client_utils import get_client

from dotenv import load_dotenv

APP_ROOT = Path(os.path.join(Path(__file__).parent)).absolute()

print(APP_ROOT)

# try to look for stored openAI keys information from the ROOT dir, 
# this file might be in one of the two locations
load_dotenv(os.path.join(APP_ROOT, "..", "..", 'openai-keys.env'))
load_dotenv(os.path.join(APP_ROOT, 'openai-keys.env'))

import os

app = Flask(__name__, static_url_path='', static_folder=os.path.join(APP_ROOT, "dist"))
CORS(app)

@app.route('/vega-datasets')
def get_example_dataset_list():
    dataset_names = vega_data.list_datasets()
    example_datasets = [
        {"name": "gapminder", "challenges": [
            {"text": "Create a line chart to show the life expectancy trend of each country over time.", "difficulty": "easy"},
            {"text": "Visualize the top 10 countries with highest life expectancy in 2005.", "difficulty": "medium"},
            {"text": "Find top 10 countries that have the biggest difference of life expectancy in 1955 and 2005.", "difficulty": "hard"},
            {"text": "Rank countries by their average population per decade. Then only show countries with population over 50 million in 2005.", "difficulty": "hard"}
        ]},
        {"name": "income", "challenges": [
            {"text": "Create a line chart to show the income trend of each state over time.", "difficulty": "easy"},
            {"text": "Only show washington and california's percentage of population in each income group each year.", "difficulty": "medium"},
            {"text": "Find the top 5 states with highest percentage of high income group in 2016.", "difficulty": "hard"}
        ]},
        {"name": "disasters", "challenges": [
            {"text": "Create a scatter plot to show the number of death from each disaster type each year.", "difficulty": "easy"},
            {"text": "Filter the data and show the number of death caused by flood or drought each year.", "difficulty": "easy"},
            {"text": "Create a heatmap to show the total number of death caused by each disaster type each decade.", "difficulty": "hard"},
            {"text": "Exclude 'all natural disasters' from the previous chart.", "difficulty": "medium"}
        ]},
        {"name": "movies", "challenges": [
            {"text": "Create a scatter plot to show the relationship between budget and worldwide gross.", "difficulty": "easy"},
            {"text": "Find the top 10 movies with highest profit after 2000 and visualize them in a bar chart.", "difficulty": "easy"},
            {"text": "Visualize the median profit ratio of movies in each genre", "difficulty": "medium"},
            {"text": "Create a scatter plot to show the relationship between profit and IMDB rating.", "difficulty": "medium"},
            {"text": "Turn the above plot into a heatmap by bucketing IMDB rating and profit, color tiles by the number of movies in each bucket.", "difficulty": "hard"}
        ]},
        {"name": "unemployment-across-industries", "challenges": [
            {"text": "Create a scatter plot to show the relationship between unemployment rate and year.", "difficulty": "easy"},
            {"text": "Create a line chart to show the average unemployment per year for each industry.", "difficulty": "medium"},
            {"text": "Find the 5 most stable industries (least change in unemployment rate between 2000 and 2010) and visualize their trend over time using line charts.", "difficulty": "medium"},
            {"text": "Create a bar chart to show the unemployment rate change between 2000 and 2010, and highlight the top 5 most stable industries with least change.", "difficulty": "hard"}
        ]}
    ]
    dataset_info = []
    print(dataset_names)
    for dataset in example_datasets:
        name = dataset["name"]
        challenges = dataset["challenges"]
        try:
            info_obj = {'name': name, 'challenges': challenges, 'snapshot': vega_data(name).to_json(orient='records')}
            dataset_info.append(info_obj)
        except:
            pass
    
    response = flask.jsonify(dataset_info)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/vega-dataset/<path:path>')
def get_datasets(path):
    try:
        df = vega_data(path)
        # to_json is necessary for handle NaN issues
        data_object = df.to_json(None, 'records')
    except Exception as err:
        print(path)
        print(err)
        data_object = "[]"
    response = data_object
    return response

@app.route('/check-available-models', methods=['GET', 'POST'])
def check_available_models():

    results = []

    # dont need to check if it's empty
    if os.getenv("ENDPOINT") is None:
        return json.dumps(results)

    client = get_client(os.getenv("ENDPOINT"), "")
    models = [model.strip() for model in os.getenv("MODELS").split(',')]

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Respond 'I can hear you.' if you can hear me. Do not say anything other than 'I can hear you.'"},
                ]
            )

            print(f"model: {model}")
            print(f"welcome message: {response.choices[0].message.content}")

            if "I can hear you." in response.choices[0].message.content:
                results.append({
                    "endpoint": "default",
                    "key": "",
                    "model": model
                })
        except:
            pass

    return json.dumps(results)

@app.route('/test-model', methods=['GET', 'POST'])
def test_model():
    
    if request.is_json:
        app.logger.info("# code query: ")
        content = request.get_json()
        endpoint = html.escape(content['endpoint'].strip())
        key = html.escape(f"{content['key']}".strip())

        print(content)

        client = get_client(endpoint, key)
        model = html.escape(content['model'].strip())

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Respond 'I can hear you.' if you can hear me. Do not say anything other than 'I can hear you.'"},
                ]
            )

            print(f"model: {model}")
            print(f"welcome message: {response.choices[0].message.content}")

            if "I can hear you." in response.choices[0].message.content:
                result = {
                    "endpoint": endpoint,
                    "key": key,
                    "model": model,
                    "status": 'ok',
                    "message": ""
                }
        except Exception as e:
            print(f"Error: {e}")
            error_message = str(e)
            result = {
                "endpoint": endpoint,
                "key": key,
                "model": model,
                "status": 'error',
                "message": error_message,
            }
    else:
        {'status': 'error'}
    
    return json.dumps(result)

@app.route("/", defaults={"path": ""})
def index_alt(path):
    print(app.static_folder)
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(404)
def page_not_found(e):
    # your processing here
    print(app.static_folder)
    return send_from_directory(app.static_folder, "index.html") #'Hello 404!' #send_from_directory(app.static_folder, "index.html")

###### test functions ######

@app.route('/hello')
def hello():
    values = [
            {"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43},
            {"a": "D", "b": 91}, {"a": "E", "b": 81}, {"a": "F", "b": 53},
            {"a": "G", "b": 19}, {"a": "H", "b": 87}, {"a": "I", "b": 52}
        ]
    spec =  {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "A simple bar chart with embedded data.",
        "data": { "values": values },
        "mark": "bar",
        "encoding": {
            "x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},
            "y": {"field": "b", "type": "quantitative"}
        }
    }
    return json.dumps(spec)


@app.route('/hello-stream')
def streamed_response():
    def generate():
        values = [
            {"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43},
            {"a": "D", "b": 91}, {"a": "E", "b": 81}, {"a": "F", "b": 53},
            {"a": "G", "b": 19}, {"a": "H", "b": 87}, {"a": "I", "b": 52}
        ]
        spec =  {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": "A simple bar chart with embedded data.",
            "data": { "values": [] },
            "mark": "bar",
            "encoding": {
                "x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},
                "y": {"field": "b", "type": "quantitative"}
            }
        }
        for i in range(3):
            time.sleep(3)
            spec["data"]["values"] = values[i:]
            yield json.dumps(spec)
    return Response(stream_with_context(generate()))


###### agent related functions ######

@app.route('/process-data-on-load', methods=['GET', 'POST'])
def process_data_on_load_request():

    if request.is_json:
        app.logger.info("# process data query: ")
        content = request.get_json()
        token = content["token"]

        client = get_client(content['model']['endpoint'], content['model']['key'])
        model = content['model']['model']
        app.logger.info(f" model: {content['model']}")
        
        agent = DataLoadAgent(client=client, model=model)
        candidates = agent.run(content["input_data"])
        
        candidates = [c['content'] for c in candidates if c['status'] == 'ok']

        response = flask.jsonify({ "status": "ok", "token": token, "result": candidates })
    else:
        response = flask.jsonify({ "token": -1, "status": "error", "result": [] })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/derive-concept-request', methods=['GET', 'POST'])
def derive_concept_request():

    if request.is_json:
        app.logger.info("# code query: ")
        content = request.get_json()
        token = content["token"]

        client = get_client(content['model']['endpoint'], content['model']['key'])
        model = content['model']['model']
        app.logger.info(f" model: {content['model']}")
        
        agent = ConceptDeriveAgent(client=client, model=model)

        #print(content["input_data"])

        candidates = agent.run(content["input_data"], [f['name'] for f in content["input_fields"]], 
                                       content["output_name"], content["description"])
        
        candidates = [c['code'] for c in candidates if c['status'] == 'ok']

        response = flask.jsonify({ "status": "ok", "token": token, "result": candidates })
    else:
        response = flask.jsonify({ "token": -1, "status": "error", "result": [] })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/clean-data', methods=['GET', 'POST'])
def clean_data_request():

    if request.is_json:
        app.logger.info("# data clean request")
        content = request.get_json()
        token = content["token"]

        client = get_client(content['model']['endpoint'], content['model']['key'])
        model = content['model']['model']

        app.logger.info(f" model: {content['model']}")
        
        agent = DataCleanAgent(client=client, model=model)

        candidates = agent.run(content['content_type'], content["raw_data"], content["image_cleaning_instruction"])
        
        candidates = [c for c in candidates if c['status'] == 'ok']

        response = flask.jsonify({ "status": "ok", "token": token, "result": candidates })
    else:
        response = flask.jsonify({ "token": -1, "status": "error", "result": [] })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/codex-sort-request', methods=['GET', 'POST'])
def sort_data_request():

    if request.is_json:
        app.logger.info("# sort query: ")
        content = request.get_json()
        token = content["token"]

        client = get_client(content['model']['endpoint'], content['model']['key'])
        model = content['model']['model']
        app.logger.info(f" model: {content['model']}")

        agent = SortDataAgent(client=client, model=model)
        candidates = agent.run(content['field'], content['items'])

        #candidates, dialog = limbo_concept.call_codex_sort(content["items"], content["field"])
        candidates = candidates if candidates != None else []
        response = flask.jsonify({ "status": "ok", "token": token, "result": candidates })
    else:
        response = flask.jsonify({ "token": -1, "status": "error", "result": [] })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/derive-data', methods=['GET', 'POST'])
def derive_data():

    if request.is_json:
        app.logger.info("# request data: ")
        content = request.get_json()        
        token = content["token"]

        client = get_client(content['model']['endpoint'], content['model']['key'])
        model = content['model']['model']
        app.logger.info(f" model: {content['model']}")

        # each table is a dict with {"name": xxx, "rows": [...]}
        input_tables = content["input_tables"]
        new_fields = content["new_fields"]
        instruction = content["extra_prompt"]

        print("spec------------------------------")
        print(new_fields)
        print(instruction)

        mode = "transform"
        if len(new_fields) == 0:
            mode = "recommendation"

        if mode == "recommendation":
            # now it's in recommendation mode
            agent = DataRecAgent(client, model)
            results = agent.run(input_tables, instruction)
        else:
            agent = DataTransformationAgentV2(client=client, model=model)
            results = agent.run(input_tables, instruction, [field['name'] for field in new_fields])

        repair_attempts = 0
        while results[0]['status'] == 'error' and repair_attempts == 0: # only try once
            error_message = results[0]['content']
            new_instruction = f"We run into the following problem executing the code, please fix it:\n\n{error_message}\n\nPlease think step by step, reflect why the error happens and fix the code so that no more errors would occur."

            prev_dialog = results[0]['dialog']

            if mode == "transform":
                results = agent.followup(input_tables, prev_dialog, [field['name'] for field in new_fields], new_instruction)
            if mode == "recommendation":
                results = agent.followup(input_tables, prev_dialog, new_instruction)

            repair_attempts += 1
        
        response = flask.jsonify({ "token": token, "status": "ok", "results": results })
    else:
        response = flask.jsonify({ "token": "", "status": "error", "results": [] })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/refine-data', methods=['GET', 'POST'])
def refine_data():

    if request.is_json:
        app.logger.info("# request data: ")
        content = request.get_json()        
        token = content["token"]

        client = get_client(content['model']['endpoint'], content['model']['key'])
        model = content['model']['model']
        app.logger.info(f" model: {content['model']}")

        # each table is a dict with {"name": xxx, "rows": [...]}
        input_tables = content["input_tables"]
        output_fields = content["output_fields"]
        dialog = content["dialog"]
        new_instruction = content["new_instruction"]
        
        print("previous dialog")
        print(dialog)

        # always resort to the data transform agent       
        agent = DataTransformationAgentV2(client, model=model)
        results = agent.followup(input_tables, dialog, [field['name'] for field in output_fields], new_instruction)

        repair_attempts = 0
        while results[0]['status'] == 'error' and repair_attempts == 0: # only try once
            error_message = results[0]['content']
            new_instruction = f"We run into the following problem executing the code, please fix it:\n\n{error_message}\n\nPlease think step by step, reflect why the error happens and fix the code so that no more errors would occur."
            prev_dialog = results[0]['dialog']

            results = agent.followup(input_tables, prev_dialog, [field['name'] for field in output_fields], new_instruction)
            repair_attempts += 1

        response = flask.jsonify({ "token": token, "status": "ok", "results": results})
    else:
        response = flask.jsonify({ "token": "", "status": "error", "results": []})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/code-expl', methods=['GET', 'POST'])
def request_code_expl():
    if request.is_json:
        app.logger.info("# request data: ")
        content = request.get_json()        
        token = content["token"]

        client = get_client(content['model']['endpoint'], content['model']['key'])
        model = content['model']['model']
        app.logger.info(f" model: {content['model']}")

        # each table is a dict with {"name": xxx, "rows": [...]}
        input_tables = content["input_tables"]
        code = content["code"]
        
        code_expl_agent = CodeExplanationAgent(client=client, model=model)
        expl = code_expl_agent.run(input_tables, code)
    else:
        expl = ""
    return expl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data Formulator")
    parser.add_argument("-p", "--port", type=int, default=5000, help="The port number you want to use")
    return parser.parse_args()


def run_app():
    args = parse_args()

    url = "http://localhost:{0}".format(args.port)
    threading.Timer(2, lambda: webbrowser.open(url, new=2)).start()

    app.run(host='0.0.0.0', port=args.port, threaded=True)
    
if __name__ == '__main__':
    #app.run(debug=True, host='127.0.0.1', port=5000)
    #use 0.0.0.0 for public
    run_app()
