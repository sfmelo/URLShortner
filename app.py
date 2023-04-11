import hashlib
import os
from flask import Flask, request, abort, jsonify
from pymemcache.client.base import Client

URL_SIZE = 7
MEMCACHE_HOST = "localhost"
MEMCACHE_PORT = "11211"
DEBUG=os.getenv("DEBUG", False)

app = Flask(__name__)

class URLCache:
    def __init__(self, host=MEMCACHE_HOST, port=MEMCACHE_PORT):
        self.url_cache = Client(f"{host}:{port}")
        self.encoding = "ascii"
    
    def register(self, url):
        shortened = hashlib.sha1(bytes(url, encoding=self.encoding)).hexdigest()[:URL_SIZE]
        self.url_cache.add(shortened, url)
        return shortened
    
    def get(self, shortened):
        result = self.url_cache.get(shortened)
        if not result:
            return None
        return str(result, encoding=self.encoding)
    
url_cache = URLCache()
    
def custom_response(status_code, parameter, message):
    response = jsonify({parameter: message})
    response.status_code = status_code
    return response
        
@app.route('/register', methods=['POST'])
def register_url():
    url = request.args['url']
    if not url:
        return custom_response(400, "error", "no url query parameter provided")
    
    shortened = url_cache.register(url=url)    
    return custom_response(201, "id", shortened)


@app.route('/url/<url>', methods=['GET'])
def get_full_url(url):
    full_url = str(url_cache.get(shortened=url))
    if not full_url or full_url == "None":
        return custom_response(404, "error", "url is not valid")
    return custom_response(302, "url", full_url)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080, debug=DEBUG)