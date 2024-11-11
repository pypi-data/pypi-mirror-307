# The MIT License (MIT)
#
# Copyright (c) 2024 Scott Lau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

from sc_utilities import Singleton
from sc_utilities import log_init

log_init()

import pandas as pd
from sc_config import ConfigUtils
from sc_exam_checker import PROJECT_NAME, __version__
import argparse
import requests
import os
import time
import random
from bs4 import BeautifulSoup


def _check_exams(exam: dict) -> int:
    logging.getLogger(__name__).info("processing exam {}".format(exam.get("exam")))
    headers = {
        "content-type": exam.get("content_type"),
        "cache-control": "no-cache",
    }
    s = requests.Session()
    s.headers.update(headers)
    url = exam.get("url")
    response = requests.get(url=url, headers=s.headers, cookies=s.cookies)
    status_code = response.status_code
    if status_code != 200:
        logging.getLogger(__name__).error("failed to request url {} error code {}".format(url, status_code))
        return status_code

    response_text = response.text
    soup = BeautifulSoup(response_text, 'lxml')
    all_links = soup.find_all('a')
    if all_links is None or len(all_links) <= 0:
        logging.getLogger(__name__).error("no links found")
        return 1
    logging.getLogger(__name__).debug("exam web page content {}".format(response_text))
    keywords = exam.get("keywords")
    if not isinstance(keywords, list) or len(keywords) <= 0:
        logging.getLogger(__name__).error("keywords {} configuration is invalid or not found".format(keywords))
        return 1

    for link in all_links:
        all_found = True
        logging.getLogger(__name__).debug("processing link {}".format(link))
        for keyword in keywords:
            if keyword not in link.text:
                logging.getLogger(__name__).debug("keyword {} not found".format(keyword))
                all_found = False
                break
        if all_found:
            logging.getLogger(__name__).info("all keywords have been found in link {}".format(link))
            return 0
    logging.getLogger(__name__).info("no link contains all the keywords {}".format(keywords))
    return 1


class Runner(metaclass=Singleton):

    def __init__(self):
        project_name = PROJECT_NAME
        ConfigUtils.clear(project_name)
        self._config = ConfigUtils.get_config(project_name)

        self._exams = list()
        exams = self._config.get("env.exams")
        if isinstance(exams, list) and len(exams) > 0:
            self._exams.extend(exams)

    def run(self, *, args):
        logging.getLogger(__name__).info("arguments {}".format(args))
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        logging.getLogger(__name__).info("configurations {}".format(self._config.as_dict()))

        for exam in self._exams:
            result = _check_exams(exam)
            if result != 0:
                logging.getLogger(__name__).error("check exam {} failed {}".format(exam.get("exam"), result))
        return 0


def main():
    try:
        parser = argparse.ArgumentParser(description='Python project')
        args = parser.parse_args()
        state = Runner().run(args=args)
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        return 1
    else:
        return state
