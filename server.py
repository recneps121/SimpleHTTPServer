import mimetypes
import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class CS2610Assn1(BaseHTTPRequestHandler):

    def redirect(self, desired_location):
        self.send_response(301)
        self.send_header("Location", desired_location)
        self.send_header("Connection", "close")
        self.end_headers()

    def do_GET(self):

        path = self.path[1:]
        path_without_extension = path + ".html"

        if os.access(path, os.F_OK):
            file_to_send = open(path, "rb")
            full_content = file_to_send.read()
            file_to_send.close()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(self.path[1:])[0])
            self.send_header("Content-Length", str(len(full_content)))
            self.send_header("Cache-Control", "max-age=3")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(full_content)
        elif os.access(path_without_extension, os.F_OK):
            self.redirect("/" + path_without_extension)
        elif self.path == "/":
            self.redirect("/index.html")
        elif self.path.startswith("/bio"):
            self.redirect("/about.html")
        elif self.path == "/help":
            self.redirect("/tips.html")
        elif self.path == "/teapot":
            self.send_response(418)
            self.end_headers()
            self.wfile.write(bytes(f"""
                <!DOCTYPE html>

                <html lang="en">
                    <head>
                        <meta charset="utf-8"/>
                        <link rel="stylesheet" href="style.css" type="text/css"/>
                        <title>418 I'M A TEAPOT</title>
                    </head>
                    <body>
                        <p><h1>I'm a teapot. Sorry, no coffee here. Use this link to go back home: </h1></p>
                        <p><a href="index.html"> HOME </a></p>
                    </body>
                </html>
            """, "utf_8"))
        elif self.path == "/debugging":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(bytes(f"""
                Servers version String: {self.version_string()}\n
                Servers current date/time: {self.date_time_string()}\n
                Clients IP: {self.address_string()}\n
                Path Requested: {self.path}\n
                HTTP request: {self.requestline}\n
                List of Headers:\n {self.headers}\n
            """, "utf_8"))
        elif self.path == "/forbidden":
            self.send_response(403)
            self.end_headers()
            self.wfile.write(bytes(f"""
                <!DOCTYPE html>

                <html lang="en">
                    <head>
                        <meta charset="utf-8"/>
                        <link rel="stylesheet" href="style.css" type="text/css"/>
                        <title>403 FORBIDDEN</title>
                    </head>
                    <body>
                        <p><h1>Invalid Access Rights. FORBIDDEN. 
                                Stop attempts or counterattacks will be initiated</h1></p>
                        <p><a href="index.html"> HOME </a></p>
                    </body>
                </html>
            """, "utf_8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(f"""
            <!DOCTYPE html>

            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <link rel="stylesheet" href="style.css" type="text/css"/>
                    <title>404 NOT FOUND</title>
                </head>
                <body>
                    <p><h1>I'm sorry, the page you are looking for does not exist. Use the link to go home or 
                        try again in the address bar.</h1></p>
                    <p><a href="index.html"> HOME </a></p>
                </body>
            </html>
            """, "utf_8"))


if __name__ == '__main__':
    server_address = ('localhost', 8000)
    print(f"Serving from http://{server_address[0]}:{server_address[1]}")
    print("Press Ctrl-C to quit\n")
    try:
        HTTPServer(server_address, CS2610Assn1).serve_forever()
    except KeyboardInterrupt:
        print(" Exiting")
        exit(0)
