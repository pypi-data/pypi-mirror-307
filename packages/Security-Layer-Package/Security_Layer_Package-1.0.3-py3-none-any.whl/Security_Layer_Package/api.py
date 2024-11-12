import requests

# Define the API endpoint
url = 'http://127.0.0.1:8888'
# prompt='hello'
# Make the API call



# Display the response in the app
def detection(prompt):
    response = requests.get(url+'/english/'+prompt)
    return(float(response.text[1:-1]))