# -*- coding: utf-8 -*-  
import tornado.web
import json
import tornado.gen
import sys

sys.path.insert(0, "..")
from config import settings
from error_code import ERROR_CODE
from pymongo import Connection
from hmako.lookup import TemplateLookup
from config import debug as DEBUG
from os.path import abspath, dirname, join
from config import PREFIX

RENDER_PATH = join(PREFIX, 'views/src/html')

template_lookup = TemplateLookup(
    directories=[RENDER_PATH],
    disable_unicode=True,
    encoding_errors='ignore',
    default_filters=['str', 'h'],
    filesystem_checks=DEBUG,
    input_encoding='utf-8',
    output_encoding='',
    module_directory=join(PREFIX, '_html'),
)


def render(htm, **kwds):
    mytemplate = template_lookup.get_template(htm)
    return mytemplate.render(**kwds)

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.conn = None
        self.mongo_con = None
        self.mongo_db = None

   
    def render(self, template_name=None, **kwds):
        kwds['request'] = self.request
        kwds['this'] = self
        self.finish(render(template_name, **kwds))

    @tornado.gen.coroutine
    def creat_mongo_con(self, database):
        if self.mongo_con:
            pass
        else:
            try:
                self.mongo_con = Connection(host=settings["mongo_ip"], port=settings["mongo_port"])
                self.mongo_db = self.mongo_con[database]
            except Exception, e:
                raise tornado.gen.Return(e.message)
        raise tornado.gen.Return(self.mongo_db)


    @tornado.gen.coroutine
    def save_recond(self, collection, recond):

        raise tornado.gen.Return(self.mongo_db[collection].save(recond))

    @tornado.gen.coroutine
    def del_reconds(self, collection, condition):
        raise tornado.gen.Return(self.mongo_db[collection].remove(condition))

    @tornado.gen.coroutine
    def update_recond(self, collection, condition, datas):
        raise tornado.gen.Return(self.mongo_db[collection].update(condition, datas))

    @tornado.gen.coroutine
    def query_mongo_all(self, collection, **kwargs):
        skip = kwargs.get("skip", 0)
        condition = kwargs.get("condition", {})
        if self.mongo_db:
            raise tornado.gen.Return(self.mongo_db[collection].find(condition).skip(skip))
        else:
            raise tornado.gen.Return("error")

    @tornado.gen.coroutine
    def query_mongo_sort(self, collection, sort, **kwargs):
        condition = kwargs.get("condition", {})
        skip = kwargs.get("skip", 0)
        cfilter = kwargs.get("cfilter", {})
        if self.mongo_db:
            raise tornado.gen.Return(self.mongo_db[collection].find(condition, cfilter).sort(sort).skip(skip))
        else:
            raise tornado.gen.Return("error")

    @tornado.gen.coroutine
    def query_mongo_limit(self, collection, limit, **kwargs):
        condition = kwargs.get("condition", {})
        skip = kwargs.get("skip", 0)
        if self.mongo_db:
            raise tornado.gen.Return(self.mongo_db[collection].find(condition).limit(limit).skip(skip))
        else:
            raise tornado.gen.Return("error")

    @tornado.gen.coroutine
    def query_mongo_sort_limit(self, collection, limit, rsort, **kwargs):
        condition = kwargs.get("condition", {})
        skip = kwargs.get("skip", 0)
        if self.mongo_db:
            raise tornado.gen.Return(self.mongo_db[collection].find(condition).sort(rsort).limit(limit).skip(skip))
        else:
            raise tornado.gen.Return("error")

    @tornado.gen.coroutine
    def query_one(self, collection, **kwargs):
        condition = kwargs.get("condition", {})
        cfilter = kwargs.get("cfilter", {})
        if self.mongo_db:
            raise tornado.gen.Return(self.mongo_db[collection].find_one(condition, cfilter))
        else:
            raise tornado.gen.Return("error")

    @tornado.gen.coroutine
    def close_mongo_conn(self):
        if self.mongo_con:
            self.mongo_con.close()
        else:
            pass


    @tornado.gen.coroutine
    def response_error(self, error_name, status_code=0):
        """
        write error message
        :param error_name:
        :param status_code
        """
        if status_code == 0:
            self.set_header("Content-Type", 'text/html; charset="utf-8"')
            self.write(json.dumps(ERROR_CODE[error_name]))
            raise tornado.web.Finish()
        else:
            raise tornado.web.HTTPError(status_code=status_code, log_message=error_name)
