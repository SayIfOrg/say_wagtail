from gevent import monkey
from psycogreen.gevent import patch_psycopg


worker_class = "gevent"


def post_fork(server, worker):
    # patch calls for gevent workers #
    monkey.patch_all()
    patch_psycopg()
    worker.log.info("Made Psycopg2 Green")
    #       #       #       #       #
