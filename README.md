
# Collecting and Submiting MongoDB Atlas Logs to Datadog
![Atlas Logs](https://p-qkfgo2.t2.n0.cdn.getcloudapp.com/items/p9uYZXQo/fee610bc-86e1-44e5-aaf4-c36cdec5fb5f.jpg?v=adb56fc3106e90c15d9b6695eb4844f9)
---
MongoDB Atlas currently offer two methods to collect logs: via the [MongoDB Atlas UI](https://www.mongodb.com/docs/atlas/mongodb-logs/) or via the [MongoDB Admin API](https://www.mongodb.com/docs/atlas/reference/api-resources-spec/v2/). While Datadog has a web integration with MongoDB to pull metrics from Atlas, pulling logs are not supported at this time (10/23). 

For this reason, this repo will walk you through how to use the Datadog agent to collect MongoDB Atlas logs via the API through Datadogs [Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7).


### What is a Custom Agent Check?
Datadogs agent gets installed on your infrastructure (VMs, EC2s) to collect system metrics and offers integration specific metrics (redis metrics, postgres metrics, iis metrics, nginx metrics, self hosted mongo metrics, etc) which can be enabled in the agent configuration. However, you can create your own checks to run a python script that performs any task. Essentially, the agent runs cron jobs that run a python script at a set interval.

## Setting Up Mongo Credentials

#### We have four main steps:
- Create an API Key
- Grab the Atlas Project ID and Hosts
- Clone and run the Agent Check
- Add the Atlas credentials / variables and restart the agent

### Create an API Key in the Atlas Organization
Go to the Organizations page and select Access manager in the left hand nav bar.

![API Key](https://p-qkfgo2.t2.n0.cdn.getcloudapp.com/items/GGuy5E1r/59a1c008-e835-4011-812a-3faf0f7767ab.jpg?v=64a657e20bd727ce481edaeeaf32311a)

Create a new API Key. The API Key must have the Project Monitoring Admin role.

Once created, copy the Public and Private Key. You can also add an API Access List (list or range of IPs that will be able to make this connection). If you do not add an IP Address, all IPs will be allowed.

### Grab the Atlas Project ID and Hosts

Grab the Project ID from the Organization projects page.

![ProjectId](https://p-qkfgo2.t2.n0.cdn.getcloudapp.com/items/4guRXZk8/c95af086-dac1-4379-99aa-ea01c552bea5.jpg?source=viewer&v=0ba993e4d828ca733ca8fdf9fe019813)
---
Grab the hostname of the Mongo instance. Select the project that you want to collect logs for and go the the Database tab. Click on monitoring and go to the overview tab to see the instance (host) names for your cluster.

![Hosts](https://p-qkfgo2.t2.n0.cdn.getcloudapp.com/items/p9uYZ6d8/c1fb033c-de4b-486e-83dd-d6d168f988fa.jpg?v=763bc9b0d6ce3fb71348986f2d462452)
---

My cluster name is test so the host names are test-shard-*.1epsy.mongodb.net.

### Clone and run the Agent Check

```git clone https://github.com/thedogwiththedataonit/MongoAtlasLogCheck.git```

If you havent done so already - [Install the Datadog Agent](https://docs.datadoghq.com/agent/)

Now we have to move two files into the agent to complete our custom agent check. Here are the steps:
- Go to the [Agent Directory](https://docs.datadoghq.com/agent/configuration/agent-configuration-files/?tab=agentv6v7#agent-configuration-directory), ```/etc/datadog-agent/``` on linux.
- Move [mongo_atlas.py](https://github.com/thedogwiththedataonit/MongoAtlasLogCollection/blob/main/checks.d/mongo_atlas.py) into -> ```/etc/datadog-agent/checks.d```
- Move the entire directory [mongo_atlas.d](https://github.com/thedogwiththedataonit/MongoAtlasLogCollection/tree/main/conf.d) (including the conf.yaml file) into -> ```/etc/datadog-agent/conf.d```

### Adding Configurations into mongo_atlas.d/conf.yaml file
Input the API Key credentials, log names, hosts, and the project ID.
```
init_config:

instances:
  - hosts:
      - <MONGO_HOST>
      - <MONGO_HOST>
    project_id: <PROJECT_ID>
    atlas_public_key: <ATLAS_API_PUBLIC_KEY>
    atlas_private_key: <ATLAS_API_PRIVATE_KEY>
    log_names:
      - mongodb
      - mongodb-audit-log
    min_collection_interval: 300
    port: 10519
    

logs:
  - type: tcp
    port: 10519
    service: "mongo_atlas"
    source: "mongodb"
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `<MONGO_HOST>` | `string` | **Required**. The primary or secondary MongoDB host found in the MongoDB Metrics Overview page. |
| `<PROJECT_ID>` | `string` | **Required**. The The Atlas Project ID can be found in the Atlas UI in the Organization -> Projects page. |
| `<ATLAS_API_PUBLIC_KEY>` | `string` | **Required**. Atlas API Public Key |
| `log_names` | `list` | **Required**. The log names you want to collect. Valid log names are ["mongodb", "mongos", "mongodb-audit-log", "mongos-audit-log"](https://www.mongodb.com/docs/atlas/mongodb-logs/#in-the-download-logs-modal-edit-the-following-fields) |
| `min_collection_interval` | `int` | **Optional**. Collection is run every 5 minutes by default. Value in seconds. |
| `port` | `int` | **Required**. Port the Agent Check submits. The Datadog Agent listens on a port for logs via TCP. Make sure this matches the logs.port section below. |

---
### Restart the Agent
Once you have filled out this section, [restart the Datadog Agent](https://docs.datadoghq.com/agent/configuration/agent-commands/?tab=agentv6v7#restart-the-agent). 
You can also access the [Datadog Agent Manager GUI](http://127.0.0.1:5002/) to restart and manage your agent (agent must be installed).

![agentstatus](https://p-qkfgo2.t2.n0.cdn.getcloudapp.com/items/P8uDXQOz/ee67a325-0d64-4895-83ae-3cd7aca1b4e1.jpg?v=8a39510fc8d03fee0f2cb17249b96b05)

This is also where you can confirm that the integration is working correctly.

## API Reference

#### Get Logs from a host
The python check runs a get request to the following endpoint with a digest auth header. View the [API here](https://www.mongodb.com/docs/atlas/reference/api-resources-spec/v2/#tag/Monitoring-and-Logs/operation/getHostLogs).
```http
  GET https://cloud.mongodb.com/api/atlas/v1.0/groups/{project_id}/clusters/{mongodb_host}/logs/{log_name}.gz?startDate={start_time}&endDate={end_time}"
```
Using version 1, not sure why v2 wasn't working.

---

## Conclusion

If you have any questions or insights to add on this solution please contact me at thomas.park@datadoghq.com




