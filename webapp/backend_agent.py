import logging
import redis


class BackendAgent:

    def __init__(self):

        self.logger = logging.getLogger('backend')
        self.logger.info("Starting backend!")
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

        self.distance = None

    def get_last_aps(self):
        return self.redis.lpop("scan")

    def get_distance(self):
        return self.redis.lpop("distance")


