# -*- coding: utf-8 -*-
from __future__ import (division, print_function, absolute_import, unicode_literals)

__all__ = ["httpsRequest"]

import os
import sys
import time
import requests

base_url = "https://api.github.com"

def getAuth():
    return {"client_id": os.environ['USERNAME'], "client_secret": os.environ['PASSWORD']}


def httpsRequest(endpoint, method="GET", retries=0, **kwargs):
    payload = dict(getAuth(), **kwargs)
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "alanwooo/crawler",
    }
    print (payload)
    try:
        r = getattr(requests, method.lower())(base_url + endpoint,
                                              params=payload,
                                              headers=headers)
    except requests.exceptions.ConnectionError:
        if retries < 10:
            print("Retrying {0}".format(endpoint))
            return httpsRequest(endpoint, method=method, retries=retries+1,
                              **kwargs)

    if r.status_code != requests.codes.ok:
        if r.status_code == 403:
            # This probably means that the rate limit was reached.
            # Wait for rate limit to reset and then re-submit the request.
            remain = int(r.headers["X-RateLimit-Remaining"])
            if remain < 1:
                reset = int(r.headers["X-RateLimit-Reset"]) - time.time()
                print("Waiting {0} seconds for rate limit to reset..."
                      .format(reset))
                time.sleep(max(1.0, reset))
                return httpsRequest(endpoint, method=method, **kwargs)

        r.raise_for_status()

    return r

