# -*- coding: utf-8 -*-

import web
import redis

web.config.debug = False

DB = web.database(dbn='mysql', db='test', user='root', pw='root')

REDIS = redis.Redis(connection_pool=redis.ConnectionPool(host='localhost'))

urls = (
    '/', 'user'
)

log = file('miss.log','w+')

class user:
    def _get_user_from_redis(self, id):
        name = REDIS.get('user:'+id)
        if not name:
            log.write("Miss\n")
            log.flush()
            name = self._get_user_from_db(id)
            if name:
                REDIS.setex('user:'+id,name,3600)
                return name
            else:
                return None
        else:
            return name


    def _get_user_from_db(self, id):
        users = list(DB.select('user', where='id=$id', vars={'id': id}))
        if users:
            return users[0].name
        else:
            return None

    def GET(self):
        id = web.input().get('u', 1)
        name = self._get_user_from_redis(id)
        # name = self._get_user_from_db(id)

        if name:
            return name
        else:
            return "No such user"


app = web.application(urls, globals())
app.internalerror = web.debugerror

if __name__ == '__main__':
    app.run()

application = app.wsgifunc()

# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
