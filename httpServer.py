import socket
import os
import json

class httpServer:
    def __init__(self,ip: str, port: int):
        self.response_status = ''
        self.response_header = ''
        self.soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.soc.bind((ip,port))

    def run(self):
        print("start running")
        while(True):
            self.soc.listen(5)
            conn,addr = self.soc.accept()
            request = str(conn.recv(1024), encoding = "utf-8")
            print(request)
            request = self.parseRequest(request,addr)
            print("Body:" + request["body"])
            if(not request):
                print("request error")
                conn.close()
            # url_type = request['url'].split('.')[-1]
            # try:
            file_type = "application/json"

            response = bytes('HTTP/1.1 200 OK' + os.linesep + 'Content-Type:%s'% file_type + os.linesep + os.linesep, encoding="utf-8")

            data = {
                "status" : "1",
                "msg" : "hello"
            }
            print("Response: " + json.dumps(data))
            response += bytes(json.dumps(data),encoding="utf-8")
            conn.sendall(response)
            conn.close()
            # except:
            #     print("Unknow error")
            #     response = bytes("HTTP/1.1 404 Not Found" + os.linesep, encoding="utf-8")
            #     conn.sendall(response)
            #     conn.close()

    def parseRequest(self,request,addr):
        request_split = request.split('\r\n')
        method, url, version = request_split[0].split(' ')

        requestHead = dict()

        for i in range(1, len(request_split)):
            if (request_split[i] == ''):
                break
            key, value = request_split[i].split(': ')
            requestHead[key] = value

        requestBody = []
        for i in range(2 + len(requestHead), len(request_split)):
            requestBody.append(request_split[i])
        requestBody = '\r\n'.join(requestBody)

        ans = {
            'addr': addr,
            'method': method,
            'url': url,
            'http_version': version,
            'head': requestHead,
            'body': requestBody
        }
        return ans
