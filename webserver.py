from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import json
import datetime


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('main.html', encoding='utf-8') as f:
                file = f.read()
            tasks = []
            self.read()
            html = '<div class="task-container">'
            for i, task in enumerate(self.tasks):
                tasks.append(f'\n\t<div class="task">'
                             f'\n\t\t<div class="task-title">'
                             f'\n\t\t\t<h2>{i + 1}</h2>'
                             f'\n\t\t\t<h3>{task["title"]}</h3>'
                             f'\n\t\t\t<h4>{task["time"]}</h4>'
                             f'\n\t\t</div>'
                             f'\n\t\t<div class="task-details">'
                             f'\n\t\t\t<p>{task["note"]}</p>'
                             f'\n\t\t</div>'
                             f'\n\t</div>')
            html += ''.join(tasks) + '\n</div>'
            file = file.replace('{tasks}', html)
            self.wfile.write(file.encode('utf-8'))
        if self.path == '/form':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('form.html') as f:
                file = f.read()
            self.wfile.write(file.encode())
        if self.path == '/remove':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('remove.html') as f:
                file = f.read()
            self.wfile.write(file.encode())
        if self.path == '/getTask':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('tasks.json') as f:
                length = len(json.load(f))
            self.wfile.write(str(length).encode())
        if self.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-Type', 'text/css')
            self.end_headers()
            with open('style.css') as f:
                file = f.read()
            self.wfile.write(file.encode())
        if self.path == '/script.js':
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript')
            self.end_headers()
            with open('script.js') as f:
                file = f.read()
            self.wfile.write(file.encode())
        if self.path == '/ico.png':
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            with open('ico.png', 'br') as f:
                file = f.read()
            self.wfile.write(file)

    def do_POST(self):
        if self.path == '/form':
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                self.read()
                self.tasks.append({
                    'title': fields.get('title')[0],
                    'time': datetime.datetime.now().strftime('%b %d, %H:%M'),
                    'note': fields.get('note')[0]
                })
            self.write(self.tasks)
            self.send_response(301)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Location', '/')
            self.end_headers()
        if self.path == '/remove':
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                self.read()
                index = int(fields.get('number')[0]) - 1
                self.tasks.pop(index)
            self.write(self.tasks)
            self.send_response(301)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Location', '/')
            self.end_headers()

    def read(self):
        with open('tasks.json', 'r', encoding='utf-8') as file:
            self.tasks = json.load(file)

    def write(self, obj):
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(obj, file, ensure_ascii=False)


def main():
    PORT = 8000
    server = HTTPServer(('', PORT), Handler)
    print(f'Server is running on port {PORT}...')
    server.serve_forever()


if __name__ == '__main__':
    main()
