import requests
from requests.auth import HTTPDigestAuth
import time
import gzip
from checks import AgentCheck
import socket

__version__ = "1.0.0"
base_url = "https://cloud.mongodb.com/api/atlas/v1.0/"

class HelloCheck(AgentCheck):
  def check(self, instance):
    atlas_user = instance['atlas_user']
    atlas_user_key = instance['atlas_user_key']
    project_id = instance['project_id']
    mongo_hosts = instance['hosts']
    log_names= instance['log_names']
    time_interval = instance['min_collection_interval']
    port = instance['port'] # port of agent listener
    auth = HTTPDigestAuth(atlas_user, atlas_user_key)

    for mongo_host in mongo_hosts:
      for log_name in log_names:
        get_recent_logs(auth, project_id, mongo_host, log_name, time_interval, port)

def get_recent_logs(auth, project_id, mongodb_host, log_name, time_interval, port):
    end_time = int(time.time())
    start_time = end_time - int(time_interval)
    url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{project_id}/clusters/{mongodb_host}/logs/{log_name}.gz?startDate={start_time}&endDate={end_time}"
    response = requests.get(url, auth = auth)
    unzipped = gzip.decompress(response.content)
    send_logs_to_agent_listener(unzipped, port)
    return unzipped

def send_logs_to_agent_listener(logs, port):
    host = "127.0.0.1"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(logs)
    client_socket.close()
    return