# Setup
Run `docker compose up -d` to run both the api and the memcache on two containers locally.

Each container will be on the same network and will be able to communicate with each other.

# Register URL
To Register a URL, send a POST request to:

`http://localhost:8080/register?url=https://www.pictureofhotdog.com/`

This will register the given url (in this case, "https://www.pictureofhotdog.com/") and will return an id that is used to retrieve the full URL.

# Get URL
To get the full URL from it's shortened form (the id that is returned when registering it) send a GET request to:

`http://localhost:8080/url/06f8082`

With the given id, the API will return the full URL (in this case, the URL is "https://www.pictureofhotdog.com/", the one used when registering).