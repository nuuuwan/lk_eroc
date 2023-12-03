import json
import os
import tempfile

import requests
from utils import JSONFile, Log, hashx

TIMEOUT = 30

log = Log('WWW')


class WWW:
    def __init__(self, url):
        self.url = url

    def post_nocache(self, data=None):
        response = requests.post(self.url, data=data, timeout=TIMEOUT)
        content = response.text
        n = len(content) / 1_000_000
        log.debug(f"POST {self.url} {data} ({n:.3f}MB) complete.")
        return content

    def post(self, data=None):
        h = hashx.md5(json.dumps(dict(url=self.url, data=data)))
        DIR_CACHE = os.path.join(tempfile.gettempdir(), 'utils.www.cache')
        if not os.path.exists(DIR_CACHE):
            os.makedirs(DIR_CACHE)
        cache_path = os.path.join(DIR_CACHE, h + " .json")
        json_file = JSONFile(cache_path)

        if json_file.exists:
            return json_file.read()

        content = self.post_nocache(data)
        json_file.write(content)
        return content
