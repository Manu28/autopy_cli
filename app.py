#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################################################
# Auteur: ETO
# Date creation : 29/06/2022
# Version: 1.0
# Commentaire: Service de auto AutoPy cli
#######################################################################################

# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# compose_flask/app.py
import filecmp
import json
import logging

import os
import shutil
import uuid
from asyncio import sleep
from datetime import datetime, date
from threading import Thread, Event


from flask import json, send_file, Flask
from flask import request, jsonify

from autopy import run_project, run_project_thread
from const import CLI_SERVICE_NO_PORT
from project.project_factory import ProjectFactory

HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

app = Flask(__name__)



def validate_json(json_data):
    try:
        json.loads(json_data)
    except ValueError as err:
        return False
    return True


@app.route('/autopy/v1/prj/ping')
def autopy_prj_ping():
    result = {"etat": "OK", "value": "data"}
    return jsonify(result), 200, HEADERS


@app.route('/autopy/v1/prj/<project_name>/script/<script_name>/run', methods=['GET'])
def autopy_prj_script_run(project_name, script_name ):
    """
    Lancement d'un script
    :param project_name: nom du projet
    :param script_name: nom du script a lancer
    :return:
    """
    source_persistance_name = "aws";
    run_project(project_name, script_name, source_persistance_name, cmd_name=None)

@app.route('/autopy/v1/prj/<project_name>/script/<script_name>/run/thread', methods=['GET'])
def autopy_prj_script_run_thread(project_name, script_name ):
    """
    Lancement d'un script
    :param project_name: nom du projet
    :param script_name: nom du script a lancer
    :return:
    """
    source_persistance_name = "aws";
    run_project_thread(project_name, script_name, source_persistance_name, cmd_name=None)


@app.route('/autopy/v1/prj/<project_name>/script/<script_name>/stop/thread', methods=['GET'])
def autopy_prj_script_stop_thread(project_name, script_name ):
    """
    Lancement d'un script
    :param project_name: nom du projet
    :param script_name: nom du script a lancer
    :return:
    """
    source_persistance_name = "aws";
    run_project_thread(project_name, script_name, source_persistance_name, cmd_name="stop")


@app.route('/autopy/v1/prj/new', methods=['POST'])
def autopy_prj_new():
    param = request.get_json()


    if param['scripts'] == None:
        scripts_list= ["covid_collector.json", "covid_reporter.json", "covid_conf_stat.json", "covid_publication.json"]

        scripts = None
    else:
        scripts = param['scripts']
        scripts_list= []
        for s in param['scripts']:
            scripts_list.append(s['script_name'])

    datas = param['datas']
    security_data =  param['security']


    config = {
    "project_name": param['project_name'],
    "script_list": param['scripts'],
    "cmd_list": ["covid_aut.yaml"],
    "data_list": "@dir",
    "security": "security.json",
    "path_script": "../business/covid/script/",
    "source_persistance_name": param['persistance']}




    if config["data_list"] == "@dir":
        from os import listdir
        from os.path import isfile, join
        mypath = f"../business/covid/script/data_model"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        config["data_list"] = onlyfiles



    project_covid_stat = ProjectFactory(project_name=param['project_name'], script_list=scripts_list,
                                        cmd_list=config["cmd_list"], data_list=config["data_list"],
                                        security=config["security"],
                                        path_script=config["path_script"], path_security=config["path_script"],
                                        source_persistance_name=config["source_persistance_name"], scripts=scripts , datas= datas, security_data= security_data )

    data = project_covid_stat.build_graphql()

    result = {"etat": "OK", "value": data}

    return jsonify(result), 200, HEADERS

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app.run(host="0.0.0.0", port=CLI_SERVICE_NO_PORT, debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
