import hashlib
from appwrite.client import Client
from appwrite.services.databases import Databases
import os


# This is your Appwrite function
# It's executed each time we get a request
def main(context):
    # Why not try the Appwrite SDK?
    #
    # client = (
    #     Client()
    #     .set_endpoint("https://cloud.appwrite.io/v1")
    #     .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
    #     .set_key(os.environ["APPWRITE_API_KEY"])
    # )
    client = Client()
    (client
     .set_endpoint('https://cloud.appwrite.io/v1')  # Your API Endpoint
     .set_project('666929470005a01fd522')  # Your project ID
     .set_key('42b747d591fb0d006152c329021807af8eb2c05f77d44808fbc6c91e28ddc73d4987fc7c85d1e584c8da035a8d1babd931643095288c7f1fcef2c29105c6379b24f915ace30be0e79ab551144a8266406034cba6935cb6c9cc7b4dde519f69b4e2c775b4b9879cc89dafe352155929a6605ab726a15f21fe572444ec1fe0ab0d')  # Your secret API key
     )
    # You can log messages to the console
    context.log("Hello, Logs!")

    # If something goes wrong, log an error
    context.error("Hello, Errors!")

    # The `ctx.req` object contains the request data
    if context.req.method == "GET":
        # Send a response with the res object helpers
        # `ctx.res.send()` dispatches a string back to the client
        databases = Databases(client)
        all_data = databases.list_documents(
            database_id="66694407002556133624",
            collection_id="666944250024f4a2b507"
        )
        for datum in all_data['documents']:
            if datum.get('hashurl') == '9d2b7e3d':
                redirect_url = datum.get('orginalurl')
                return context.res.redirect(redirect_url, 301)

        return context.res.send("Hello, World!")
    if context.req.method == "POST":
        req_data = context.req.body
        url_to_shorten = req_data['url']
        if "url" not in req_data:
            return context.res.json(
                {
                    "error": "URL parameter is missing",
                },
            )
        shortened_url = hashlib.sha256(url_to_shorten.encode()).hexdigest()[:8]
        full_shortened_url = f"{shortened_url}"

        return context.res.json(
            {
                "original_url": url_to_shorten,
                "shortened_url": full_shortened_url,
            }
        )

    # `ctx.res.json()` is a handy helper for sending JSON
    return context.res.json(
        {
            "motto": "Build like a team of hundreds_",
            "learn": "https://appwrite.io/docs",
            "connect": "https://appwrite.io/discord",
            "getInspired": "https://builtwith.appwrite.io",
        }
    )
