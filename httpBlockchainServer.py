from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

class CustomHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.broadcast_transaction_function = kwargs.pop('broadcast_transaction_function', None)
        
        self.source_id = kwargs.pop('source_id', None)
        self.blockchain_file_path = kwargs.pop('blockchain_file_path', None)
        
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/blockchain':
            try:
                with open(self.blockchain_file_path, 'r') as file:
                    blockchain_data = json.load(file)
                    response = json.dumps(blockchain_data)
                self.send_response(200)
            except FileNotFoundError:
                self.send_response(404)
                response = "File not found"
            
            # Add CORS headers here
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes(response, "utf8"))

        elif self.path.startswith('/input'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Parse the query parameters
            query_string = urllib.parse.urlsplit(self.path).query
            params = urllib.parse.parse_qs(query_string)

            # Call the broadcast function with parsed data
            # Adding mock source_id for demonstration; replace with actual data as needed
            if all(key in params for key in ['dest_id', 'product_id', 'product_sn']):
                self.broadcast_transaction_function(
                    params['dest_id'][0],
                    self.source_id ,
                    params['product_id'][0],
                    params['product_sn'][0]
                )
                response = json.dumps({"message": "Transaction broadcasted successfully"})
            else:
                response = json.dumps({"error": "Missing required parameters"})

            self.wfile.write(response.encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("Not Found", "utf8"))
            
class Httpd:
    def __init__(self, broadcast_transaction_function, source_id, blockchain_file_path, log_function, port, listening_host):
        self.port = port
        self.listening_host = listening_host
        self.log_function = log_function
        self.handler = self.create_custom_handler(broadcast_transaction_function, source_id,blockchain_file_path)
        self.server = HTTPServer((self.listening_host, self.port), self.handler)

    def create_custom_handler(self, broadcast_transaction_function, source_id, blockchain_file_path):
        def handler(*args, **kwargs):
            return CustomHandler(*args, broadcast_transaction_function=broadcast_transaction_function, source_id = source_id,blockchain_file_path=blockchain_file_path, **kwargs)
        return handler

    def run_server(self):
        self.log_function(f"Web Server Server started. Listening on {self.listening_host}:{self.port}")
        try:
            while True:  # Keep the main thread alive to handle graceful shutdown or other commands
                self.server.serve_forever()
        except :
            self.log_function("Shutting down server...")
            self.server.shutdown()
            self.server.server_close()
