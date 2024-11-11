import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")


class toqen:
  """
  A client class for interacting with the Toqen server.
  """
  def __init__(self, 
               toqen_ai_key, 
               org_id, 
               server_url = "https://toqen-server.onrender.com", 
               canary_prob = 0.1):
    self.server_url = server_url
    self.toqen_ai_key = toqen_ai_key
    self.org_id = org_id
    self.canary_prob = canary_prob
    print('TOQEN.AI: Client initialized')



  def collect(self, key, system_version, 
              dut, user_input, system_input, 
              dut_response, tag, ref_response = None, description=None):
    data = {
        'key'           : key,
        'system_version': system_version,
        'dut'           : dut,
        'user_input'    : user_input,
        'system_input'  : system_input,
        'dut_response'  : dut_response,
        'ref_response'  : ref_response,
        'tag'           : tag,
        'description'   : description,
    }

    response = requests.post(self.server_url+"/collect", json=data)
    if response.status_code == 200:
      response_data = response.json()
      echoed_message = response_data.get("results")
    else:
      response_dataata = response.json()
      echoed_message = f"Error: {response.status_code} - {response.text}"
    return echoed_message





  def userCriteria(self, userCriteria):
    data = {'userCriteria': userCriteria}
    response = requests.post(self.server_url+"/userCriteria", json=data)
    if response.status_code == 200:
      response_data = response.json()
      echoed_message = response_data.get("results")
    else:
      response_data = response.json()
      echoed_message = f"Error: {response.status_code} - {response.text}"
    return echoed_message

  def optimize_prompt(self, prompt, tag=None,  **kwargs):
    data = {
       "prompt": prompt,
       'toqen_ai_key':self.toqen_ai_key,
       'org_id':self.org_id,
       'canary_prob':self.canary_prob,
       'tag':tag,
       'kwargs':kwargs
       }
    # print(f"ECHO.AI: {kwargs}")
    response = requests.post(self.server_url+"/optimize_prompt", json=data)
    if response.status_code == 200:
    # Successful response
        response_data = response.json()
        echoed_message = response_data.get("results")
        # print(f"TOQEN.AI: {echoed_message}")
    else:
        # Error response
        response_data = response.json()
        echoed_message = f"Error: {response.status_code} - {response.text}"
    return echoed_message  
  
  def run(self,name, dut,df, fileurl=None ,**kwargs):
    data = {
       'name' : name,
       'dut' : dut,
       'fileurl' : fileurl,
       'df': df.to_json(),
       "toqen_ai_key": self.toqen_ai_key,
       "org_id": self.org_id,
       "canary_prob": self.canary_prob,
       'kwargs': kwargs
    }
    response = requests.post(self.server_url+"/run", json=data)
    if response.status_code == 200:
    # Successful response
        response_data = response.json()
        echoed_message = response_data.get("results")
        # print(f"TOQEN.AI: {echoed_message}")
    else:
        # Error response
        response_data = response.json()
        echoed_message = f"Error: {response.status_code} - {response.text}"
    return echoed_message

  def chat(self, text_prompt, **kwargs):
    data = {
       "message": text_prompt, 
       'toqen_ai_key':self.toqen_ai_key,
       'org_id':self.org_id,
       'canary_prob':self.canary_prob,
       'kwargs':kwargs
       }
    # print(f"ECHO.AI: {kwargs}")
    response = requests.post(self.server_url+"/chat", json=data)

    # Check response status code
    if response.status_code == 200:
    # Successful response
        response_data = response.json()
        echoed_message = response_data.get("message")
        # print(f"TOQEN.AI: {echoed_message}")
    else:
        # Error response
        response_data = response.json()
        echoed_message = f"Error: {response.status_code} - {response.text}"
        # print(echoed_message)
        

    return echoed_message


# Export the EchoClient class
__all__ = ['toqen']
