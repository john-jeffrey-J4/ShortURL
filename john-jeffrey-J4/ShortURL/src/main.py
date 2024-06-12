from appwrite.client import Client
import hashlib
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
        url_to_shorten = context.req.query_string
        context.log(url_to_shorten)

        return context.res.json(
            {
                "error": "Hello Bro",
            },
        )

        if not url_to_shorten:
            return context.res.json(
                {
                    "error": "URL parameter is missing",
                },
            )

        # Shorten the URL using a hash
        shortened_url = hashlib.sha256(url_to_shorten.encode()).hexdigest()[:8]

        # Construct the shortened URL (this is just an example)
        base_url = "https://short.url/"
        full_shortened_url = f"{base_url}{shortened_url}"

        # Send the shortened URL back to the client
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
