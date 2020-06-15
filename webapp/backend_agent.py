import logging
import redis
import json

class BackendAgent:

    def __init__(self):

        self.logger = logging.getLogger('backend')
        self.logger.info("Starting backend!")
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

        self.distance = None

    def get_last_aps(self):
        return self.redis.hgetall("scanner")

    def get_distance(self):
        return self.redis.lpop("distance")

    def record_location(self, location):
        aps = self.get_last_aps()
        if self.redis.set('location', json.dumps(location)):
            return True
        return False

