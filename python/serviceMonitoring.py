import psutil
import socket
import requests
from datetime import datetime
from flask import Flask
from flask import request

date = datetime.now()
dateStr = date.strftime('%d.%m.%Y %H:%M:%S.%f')
dt_obj = datetime.strptime(dateStr, '%d.%m.%Y %H:%M:%S.%f')
timestamp = dt_obj.timestamp() * 1000

#Check that the service is running

host_name = socket.gethostname()
services = ["RABBITMQ","HTTPD","POSTGRESQL","CHROME"]
detected_pids = set()
rbcapp1 = "DOWN"
service_status = "DOWN"
serviceDict = {}
serviceList = []
# Search for running processes that match our command string.
for proc in psutil.process_iter():
  for service in services:
    try:
        if service in proc.name().upper():
           # print(proc.name())
            detected_pids.add(str(proc.name))
            service_status = "UP"
            serviceDict = {
                           "service_name": service,
                           "service_status": service_status,
                           "host_name": host_name
                          }
            serviceList.append(serviceDict)
            #Creating the JSON file name format as required
            fileName = service + "-status-" + str(int(timestamp)) + ".json"
            with open(fileName, "w") as outfile:
                json.dump(serviceDict, outfile)
    # We could also get psutil.ZombieProcess or
    # psutil.AccessDenied.

    except psutil.NoSuchProcess:
        pass

print(serviceList)

app = Flask(__name__)
@app.route('/add',methods=['GET'])
def addJson():
   resp = requests.post('http://elasticsearch.com/add/', json=serviceDict)
   if resp.status_code != 201:
      raise ApiError('POST /add/ {}'.format(resp.status_code))
   return resp.status_code

@app.route('/healthcheck', methods=['GET'])
def getAllHealthCheck():
   if len(detected_pids) == len(services):
      rbcapp1 = "UP"
      print(rbcapp1)
      return "The rbcapp1 application is UP"
   else:
      return "The rbcapp1 application is DOWN"

@app.route('/healthcheck/<serviceName>',methods=['GET'])
def getServiceHealthCheck(serviceName):
   for ser in serviceList:
      if serviceName.upper() in str(ser):
         return ser['service_status']
      else:
         return "DOWN"

if __name__ == '__main__':
   app.run()
