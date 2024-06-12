import hashlib
import json
from appwrite.client import Client
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

    # You can log messages to the console
    context.log("Hello, Logs!")

    # If something goes wrong, log an error
    context.error("Hello, Errors!")

    # The `ctx.req` object contains the request data
    if context.req.method == "GET":
        # Send a response with the res object helpers
        # `ctx.res.send()` dispatches a string back to the client
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
        base_url = "https://short.url/"
        full_shortened_url = f"{base_url}{shortened_url}"
        
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
