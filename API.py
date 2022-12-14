# -*- coding: utf-8 -*

from http.server import CGIHTTPRequestHandler, HTTPServer
from os import remove

from json_API import *

HTML_FILE_NAME = 'alive'
PORT_NUMBER = 8080


# This class will handles any incoming request from the browser
class myHandler(CGIHTTPRequestHandler):
    def comfirm_request(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def make_response(self) -> None:
        if not "?" in self.path:
            req_dic = {
                "/alive": lambda: self.comfirm_request() or self.wfile.write(bytes(alive(), encoding="utf-8")),
                "/space": lambda: self.comfirm_request() or self.wfile.write(bytes(space(), encoding="utf-8")),
                "/restart": lambda: self.comfirm_request() or self.wfile.write(bytes(restart(), encoding="utf-8")),
                "/cpu_temp": lambda: self.comfirm_request() or self.wfile.write(bytes(cpu_temp(), encoding="utf-8")),
                "/log": lambda: self.comfirm_request() or self.wfile.write(bytes(serv_log(), encoding="utf-8")),
                "/stats_lib": lambda: self.comfirm_request() or self.wfile.write(bytes(stat_show(), encoding="utf-8")),
                "/check_dl": lambda: self.comfirm_request() or self.wfile.write(bytes(downloading(), encoding="utf-8"))

            }
            try:
                req_dic[self.path]()
            except KeyError:
                self.send_response(404, 'request means nothing: %s' % self.path)
        else:

            cgi_dic = {
                "/is_user": lambda: self.comfirm_request() or self.wfile.write(
                    bytes(is_user(self.path), encoding="utf-8")),
                "/dl": lambda: self.comfirm_request() or self.wfile.write(
                    bytes(dl(self.path), encoding="utf-8")),
                "/stop_dl" : lambda: self.comfirm_request() or self.wfile.write(
                    bytes(stop_dl(self.path), encoding="utf-8")),
                "/st_dl": lambda: self.comfirm_request() or self.wfile.write(
                    bytes(st_dl(self.path), encoding="utf-8")),
                "/rm_dl": lambda: self.comfirm_request() or self.wfile.write(
                    bytes(rm_dl(self.path), encoding="utf-8")),
            }
            try:
                print("/" + self.path.split("/")[1])
                cgi_dic["/" + self.path.split("/")[1]]()
            except KeyError:
                self.send_response(404, 'request means nothing: %s' % self.path)

    # Handler for the GET requests

    def do_GET(self):
        self.cgi_directories = ["/"]
        self.make_response()
        # if str(self.path)=="/":

        #     self.path = HTML_FILE_NAME

        # try:
        #     with open(curdir + sep + self.path, 'r',encoding="utf-8") as f:
        #         self.send_response(200)
        #         self.send_header('Content-type', 'text/html')
        #         self.end_headers()
        #         self.wfile.write(str(popen("python "+self.path).read()).encode('utf-8'))
        #     return
        # except IOError:
        #     self.send_error(404, 'File Not Found: %s' % self.path)


try:
    # Create a web server and define the handler to manage the incoming request

    print('Started httpserver on port %i.' % PORT_NUMBER)
    myHandler.cgi_directories = ["/"]
    # Wait forever for incoming http requests

    HTTPServer(('', PORT_NUMBER), myHandler).serve_forever()

except KeyboardInterrupt:
    print('Interrupted by the user - shutting down the web server.')
    remove(HTML_FILE_NAME)
