import sys
import yaml
import json
import jsonschema
import screepsapi
from datetime import datetime
from rich import print
from envyaml import EnvYAML

class Spybot(object):
    """Experimental spy tool for Screeps"""

    def __init__(self):
        self.get_config()
        self.connect_api()

    def get_config(self):
        self.config_file = 'config.yaml'
        with open(self.config_file) as config_file:
            config = yaml.safe_load(config_file)
        with open('config.schema.yaml') as schema_file:
            schema = yaml.safe_load(schema_file)
        try:
            jsonschema.validate(instance=config, schema=schema)
        except (jsonschema.ValidationError, jsonschema.SchemaError) as error:
            print('Config fatal error:', error.args[0])
            sys.exit(0)
        self.config = EnvYAML(self.config_file)

    def connect_api(self):
        self.api = screepsapi.API(
            host=self.config['api_host'],
            prefix=self.config['api_prefix'],
            token=self.config['api_token'] if self.config['api_token'] else None,
            u=self.config['api_username'] if self.config['api_username'] else None,
            p=self.config['api_password'] if self.config['api_password'] else None,
            secure=self.config['api_secure'] if self.config['api_secure'] else None
        )

    def log(self, *args, **kwargs):
        use_sep = ('sep' in kwargs and kwargs['sep'] == '')
        spacer = ' ' if use_sep else ''
        time = datetime.now().strftime('[%H:%M:%S]' + spacer)
        print(time, *args, **kwargs)
    
    def utf8_len(self, s):
        return len(s.encode('utf-8'))

    def get_room_link(self, shard, room):
        return '[link=https://%s%s/#!/room/%s/%s]%s[/link]' % (
            self.config['api_host'], 
            self.config['api_prefix'],
            shard,
            room,
            room
        )

    def get_user_id(self, username):
        res = self.api.user_find(username=username)
        if 'user' in res and '_id' in res['user']:
            return res['user']['_id']
        else:
            self.log('Player', username, 'was not found')
            return None

    def get_user_rooms(self, user_id, shard):
        res = self.api.user_rooms(user_id=user_id, shard=shard)
        return res['shards'][shard]

    def get_room_rcl(self, room_objects):
        for room_object in room_objects:
            if room_object['type'] == 'controller':
                return room_object['level']
        return 0

    def get_room_resources(self, room_objects):
        total = {}
        for room_object in room_objects:
            if room_object['type'] in self.config['spy_structures']:
                if 'mineralType' in room_object:
                    total = self.update_total(total, room_object['mineralType'], room_object['mineralAmount'])
                elif 'store' in room_object:
                    for resource, amount in room_object['store'].items():
                        total = self.update_total(total, resource, amount)
        return total

    def update_total(self, total, resource, amount):
        if amount == 0:
            return total
        if resource in total:
            total[resource] += amount
        else:
            total[resource] = amount
        return total

    def update_grand_total(self, grand_total, room_total):
        for resource, amount in room_total.items():
            grand_total = self.update_total(grand_total, resource, amount)
        return grand_total

    def run(self):
        shard = self.config['target_shard']
        data = {
            'rooms': {},
            'players': {}
        }

        # spy on targeted players
        for username in self.config['target_players']:
            if (not self.config['spy_resources'] and
                not self.config['spy_market'] and
                not self.config['spy_rcl']):
                self.log('No spy tasks...')
                sys.exit(0)
            self.log('Gathering intel on ', username, ' in ', shard, '...', sep='')
            user_id = self.get_user_id(username)
            spy_room = (self.config['spy_resources'] or self.config['spy_rcl'])
            if user_id and spy_room:
                total_resources = {}
                rooms = self.get_user_rooms(user_id, shard)
                data['players'][username] = {
                    'rooms': len(rooms)
                }
                for room in rooms:
                    self.log('Scanning room ', self.get_room_link(shard, room), '...', sep='')
                    data['rooms'][room] = {
                        'owner': username
                    }
                    res = self.api.room_objects(room=room, shard=shard)
                    if self.config['spy_resources']:
                        room_resources = self.get_room_resources(res['objects'])
                        if room in self.config['target_rooms']:
                            data['rooms'][room]['resources'] = room_resources
                        total_resources = self.update_grand_total(total_resources, room_resources)
                        data['players'][username]['resources'] = total_resources
                    if self.config['spy_rcl']:
                        rcl = self.get_room_rcl(res['objects'])
                        data['rooms'][room]['rcl'] = rcl

        # get current Game.tick
        tick = self.api.time(shard)
        if tick:
            data['updated'] = tick

        # display results on screen
        if self.config['results_output']:
            self.log('Results:\n', json.dumps(data, indent=4, sort_keys=True))

        # save data to segment
        if self.config['results_segment']:
            segment = self.config['results_segment_target']
            data_json = json.dumps(data, separators=(',', ':'))
            data_size = self.utf8_len(data_json)
            self.api.set_segment(segment, data_json, shard)
            self.log('Uploaded data (size ', data_size, ') to segment ', segment, ' on ', shard, sep='')


if __name__ == "__main__":
    spybot = Spybot()
    spybot.run()