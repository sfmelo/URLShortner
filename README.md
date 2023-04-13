# Setup
Run `docker compose up -d` to run both the api and the memcache on two containers locally.

Each container will be on the same network and will be able to communicate with each other.

# Register URL
To register a URL, send a POST request to:

`http://localhost:8080/register?url=<url>`

Where `<url>` is the URL you want to be shortened. This will register it and return an `id` that is used to retrieve the full URL.

# Get URL
To get the full URL from it's shortened form, send a GET request to:

`http://localhost:8080/url/<id>`

Where `<id>` is the shortened version that was returned when registering the URL. This will return the full URL.



# Example

We want to register the URL https://www.pictureofhotdog.com/ in order to have a shortened form. To do that, we send the POST request (in this example, it's being sent through cURL):

`$ curl -X POST http://localhost:8080/register\?url\=https://www.pictureofhotdog.com/`

`{"id":"06f8082"}`

This will the url and will return an `id` that is used to retrieve the full URL.

With the given `id`, the API will return the full URL when we send a GET request:

`$ curl  http://localhost:8080/url/06f8082`

`{"url":"https://www.pictureofhotdog.com/"}`