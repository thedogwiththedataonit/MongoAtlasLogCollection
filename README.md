# https://cloud.mongodb.com/api/atlas/v2/groups/{groupId}/clusters/{hostName}/logs/{logName}.gz


# Create an API Key in an Organization
Go to the Organizations page and select Access manager in the left hand nav bar.

Click on "Create API Key" (button) on the right.

Once created, copy the Public and Private Key. Make sure to also add an API Access List (list or range of IPs that will be able to make this connection). If you do not add an IP Address, all IPs will be allowed.

Grab the Project ID (group ID)

Grab the hostname of the Mongo instance. I went to the monitoring page and grabbed the primary DB host name.

Define a logName, this will be the label that identifies what log file you want to return.
- mongodb
- mongos
- mongodb-audit-log
- mongos-audit-log
For Audit related logs, enable Databse Auditing. https://www.mongodb.com/docs/atlas/database-auditing/?_ga=2.254145608.1132057786.1698961418-1230547859.1697058332&_gac=1.213446246.1698075413.CjwKCAjws9ipBhB1EiwAccEi1IsAddZZYNJ5NT6cakHHFu3Z9BLUaECj9f5VvuOoDdAmNH4E7CoyLhoC9fUQAvD_BwE

# Submission Methods
- Write to a File, Datadog Agent tails
- Submit via HTTP
- Agent Check

# MongoAtlasLogCheck
