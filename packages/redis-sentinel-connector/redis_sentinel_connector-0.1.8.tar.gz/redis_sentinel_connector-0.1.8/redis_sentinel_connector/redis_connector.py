from os import getenv
import redis
import fakeredis
from redis.sentinel import Sentinel

TYPE = getenv('TYPE')
REDIS_URL = getenv('REDIS_URL').replace(' ', '') if getenv('REDIS_URL') else None


class Singleton(type):
    _instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisConnector(metaclass=Singleton):

    def __init__(self, socket_timeout=0.1):
        self.type = TYPE
        self.redis_url = REDIS_URL
        self.socket_timeout = socket_timeout

    def connect(self, redis_url=None):

        if self.type == 'DEV':
            return redis.Redis()
        if self.type == 'TEST':
            return fakeredis.FakeStrictRedis(server=fakeredis.FakeServer())

        if redis_url:
            self.redis_url = redis_url

        if not self.redis_url:
            raise Exception('You need to set REDIS_URL environment or set TYPE environment to [DEV || TEST] or '
                            'set the parameter redis_url in connect function.')

        hosts = self.get_hosts_from_redis_url()

        return Sentinel(
            [(host.split(':')[0], self.extract_port_from_host(host)) for host in hosts],
            socket_timeout=self.socket_timeout).master_for(self.get_service_name(), password=self.get_password(),
                                                           socket_timeout=self.socket_timeout)

    def get_hosts_from_redis_url(self):
        return self.redis_url.split('@')[-1].split('/')[0].split(',')

    @staticmethod
    def extract_port_from_host(host):
        return host.split(':')[1]

    def get_service_name(self):
        return self.redis_url.split("/")[-1].split(':')[1]

    def get_password(self):
        return self.redis_url.split('@')[0].split('//:')[1]
