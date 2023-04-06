import hashlib
from flask import Flask, request, abort, jsonify
from pymemcache.client.base import Client

URL_SIZE = 7

app = Flask(__name__)

class URLHashInUseException(Exception):
    "Raised when a URL is already in the cache or there is a collison"
    pass

class URLCache:
    def __init__(self):
        self.url_cache = Client('localhost:5000')
        self._h = hashlib.sha256()
    
    def register(self, url):
        self._h.update(url)
        shortened = self._h.hexdigest()[:URL_SIZE]
        self.url_cache.add(shortened, url)
        return shortened
    
    def get(self, shortened):
        return self.url_cache.get(shortened)

url_cache = URLCache()
    
def custom_response(status_code, parameter, message):
    response = jsonify({'message': message})
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
    full_url = url_cache.get(shortened=url)
    if not full_url:
        return custom_response(404, "error" "url is not valid")

    return custom_response(302, "url", full_url)

if __name__=="__main__":
    app.run(debug=True)