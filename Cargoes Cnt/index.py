import logging
from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define a route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    # Retrieve form data from the request
    input_data = request.form['input_data']

    # Make a request to your REST API
    api_url = 'https://connect.cargoes.com/flow/api/public_tracking/v1/generateSharingUrl'
    payload = {
        'containerNumber': input_data
    }
    headers = {
        "X-DPW-ApiKey": "dL6SngaHRXZfvzGA716lioRD7ZsRC9hs",
        "X-DPW-Org-Token": "Y9ddEGne0FwnLUO6GKVdwdyCAXbP9URO"
    }

    # Log the request message
    request_info = {
        "uri": api_url,
        "method": "POST",
        "headers": headers,
        "body": payload
    }
    logger.debug("Request: %s", request_info)

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        # API request was successful
        api_response = response.json()
        logger.debug("API Response: %s", api_response)  # Print the API response

        # Check if 'url' key exists in the API response
        if 'url' in api_response:
            url = api_response['url']
            return redirect(url)  # Redirect the user to the URL
        else:
            error_message = 'API response does not contain the "url" key'
            logger.error(error_message)
            return render_template('error.html', error=error_message)
    else:
        # Handle API request failure
        error_message = 'API request failed: ' + response.text
        logger.error(error_message)
        return render_template('error.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
