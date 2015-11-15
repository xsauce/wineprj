from tornado.web import RequestHandler


class TestHandler(RequestHandler):
    def get(self):
        self.write("test")
        q = self.request.query_arguments
        print type(q)
        print q
