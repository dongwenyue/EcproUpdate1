import yaml
import time
import json
import redis
import datetime
import requests


class ProxyManager:
    def __init__(self):
        self.config = self.read_config()
        self.redis_config = self.config['redis']
        self.client = redis.Redis(host=self.redis_config['host'],
                                  password=self.redis_config['password'],
                                  port=self.redis_config['port'])
        self.instance_dict = {}

    def read_config(self):
        with open('config.yaml') as f:
            config = yaml.safe_load(f.read())
            return config

    def read_ip(self):
        resp = requests.get(self.config['proxy']).text
        if '{' in resp:
            return []
        proxy_list = resp.split()
        return proxy_list

    def delete_ip(self, live_ips, pool_ips):
        ip_to_removed = set(pool_ips) - set(live_ips)
        if ip_to_removed:
            print('ip to be removed:', ip_to_removed)
            self.client.hdel(self.redis_config['key'], *list(ip_to_removed))

    def add_new_ips(self, live_ips, pool_ips):
        ip_to_add = set(live_ips) - set(pool_ips)
        if ip_to_add:
            print('ip to add:', ip_to_add)
            ips = {}
            for ip in ip_to_add:
                ips[ip] = json.dumps({'private_ip': ip,
                                      'ts': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            self.client.hset(self.redis_config['key'], mapping=ips)

    def run(self):
        while True:
            live_ips = self.read_ip()
            pool_ips = [x.decode() for x in self.client.hgetall(self.redis_config['key'])]
            self.delete_ip(live_ips, pool_ips)
            self.add_new_ips(live_ips, pool_ips)
            time.sleep(40)


if __name__ == '__main__':
    manager = ProxyManager()
    manager.run()

