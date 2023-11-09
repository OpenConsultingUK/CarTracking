# Problem Statement: 
*The Geolocation Tracking System is designed to track multiple cars in the same city and provide their geolocation data to a user acting as the controller. This system is implemented using a SOAP (Simple Object Access Protocol) client-server architecture.*

#### Download

**pysimplesoap Library**: To create a SOAP client and server, you need to download the `pysimplesoap` library from its GitHub repository. You can find it here: [pysimplesoap GitHub Repository](https://github.com/pysimplesoap/pysimplesoap/).
Note : Delete unneccesary files and keep only pysimplesoap folder.

#### Usage
### 1. Running the geo-locators(servers)
Run three geo-locators for cars on different ports. You can specify the city name, latitude, longitude, and port number for each geo-locator. Here's an example of how to run them:

```bash
python3 server.py \
    --city "city" \
    --latitude latitude \
    --longitude longitude \
    --hostname localhost \
    --port 8000
python3 server.py --city "city1" --latitude latitude --longitude longitude --hostname localhost --port 8001
python3 server.py --city "city2" --latitude latitude --longitude longitude --hostname localhost --port 8002
python3 server.py --city "city3" --latitude latitude --longitude longitude --hostname localhost --port 8003
```

### 2. Running the controller
Start the controller by running the `controller.py` script using the following command:
```bash
python3 controller.py \
    --user_city city \
    --url "http://localhost:8000/" \
    --url "http://localhost:8001/" \
    --url "http://localhost:8002/"
```

### 3. Transferring Files to Remote Servers
Run ssh command: 
```bash
SSH_USER=test
SERVER_IP=1.2.3.4
PORT=8000
ssh ${SSH_USER}@${SERVER_IP} -p ${PORT}
```

If you need to transfer files from the local server to remote servers, you can use the scp (secure copy) command. You can use it for both individual files and folders containing multiple files. Examples:
- To copy a single zip folder (e.g., a zip folder) to a remote server:
```bash
scp -P ${PORT} ${SOURCE_FILE} ${SSH_USER}@${SERVER_IP}:${DESTINATION_PATH}
```

- To copy a folder with multiple files to a remote server:
```bash
scp -r -P ${PORT} ${SOURCE_PATH} ${SSH_USER}@${SERVER_IP}:${DESTINATION_PATH}
```
Example: `scp -r -P 22 * test@1.2.3.4:~/tracking`

### 4. Using Curl
- Run steps 1 and 2.
- To interact with the SOAP service using the curl command, you can create a test.xml file in the folder with the following content:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/geolocation">
   <soapenv:Header/>
   <soapenv:Body>
      <tns:getCity>
         <tns:city>city</tns:city>
      </tns:getCity>
   </soapenv:Body>
</soapenv:Envelope>
```

You can then use the curl command to send a SOAP request to the local server. Example: `curl --header "Content-Type: text/xml;charset=UTF-8" --header "SOAPAction:Get" --data @test.xml http://localhost:8000/`
