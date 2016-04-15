#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
from flask import Flask, jsonify, after_this_request
import config_import as ci

app = Flask(__name__)

@app.route('/api/jump/1.0/')

def api_response():

    # Open result file & read each line
    result_file = codecs.open(ci.result_file, 'r', 'utf-8')
    line = result_file.readlines()

    date  = str(line[0]).rstrip("\n")
    title = str(line[1]).rstrip("\n")
    status = str(line[2]).rstrip("\n")

    result_file.close()

    @after_this_request
    def d_header(response):
        response.headers['Content-Type'] = 'application/json; charset=utf-8'

        return response

    return jsonify(date=date,
                   title=title,
                   status=status)

if __name__ == '__main__':
    app.run(debug=True)
