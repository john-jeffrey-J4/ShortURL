import hashlib
from appwrite.client import Client
from appwrite.services.databases import Databases
import uuid

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
    databases = Databases(client)
    if context.req.method == "OPTIONS":
        return context.res.set_headers({
            'Access-Control-Allow-Origin': 'https://shortener-front-end-ten.vercel.app',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        }).send('')
        
    # The `ctx.req` object contains the request data
    if context.req.method == "GET":
        # Send a response with the res object helpers
        # `ctx.res.send()` dispatches a string back to the client

        path_param = context.req.path
        context.log(path_param)
        all_data = databases.list_documents(
            database_id="66694407002556133624",
            collection_id="666944250024f4a2b507"
        )
        if path_param == "/listall":
            all_data_return = []
            for datum in all_data['documents']:
                all_data_return.append({"original_url": datum.get(
                    'originalurl'), "shortened_url": datum.get('hashurl')})

            return context.res.set_headers({
                'Access-Control-Allow-Origin': 'https://shortener-front-end-ten.vercel.app',
            }).json({
                "data": all_data_return
            })
        else:

            for datum in all_data['documents']:
                if datum.get('hashurl') == path_param[1:]:
                    redirect_url = datum.get('originalurl')
                    context.log(redirect_url)
                    return context.res.redirect(f'{redirect_url}', 301)

            return context.res.send("Data not Found")

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

        all_data = databases.list_documents(
            database_id="66694407002556133624",
            collection_id="666944250024f4a2b507"
        )
        for datum in all_data['documents']:
            if datum.get('hashurl') == full_shortened_url:
                return context.res.json(
                    {
                        "original_url": url_to_shorten,
                        "shortened_url": full_shortened_url,
                    }
                )

        result = databases.create_document(
            database_id="66694407002556133624",
            collection_id="666944250024f4a2b507",
            document_id=str(uuid.uuid4().hex),
            data={"hashurl": full_shortened_url,
                  "originalurl": url_to_shorten},
        )
        context.log(result)

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
