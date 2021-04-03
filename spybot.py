import sys
import yaml
import json
import jsonschema
from datetime import datetime
from rich import print
from envyaml import EnvYAML
from screepsapi import ScreepsAPI

class Spybot(object):
    """
    Screeps intel gathering for wartime
    """

    def __init__(self):
        self.getConfig()
        self.startAPI()

    def getConfig(self):
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

    def startAPI(self):
        self.api = ScreepsAPI(
            host=self.config['api_host'],
            prefix=self.config['api_prefix'],
            token=self.config['api_token'],
            secure=True
        )

    def log(self, *args, **kwargs):
        use_sep = ('sep' in kwargs and kwargs['sep'] == '')
        spacer = ' ' if use_sep else ''
        time = datetime.now().strftime('[%H:%M:%S]' + spacer)
        print(time, *args, **kwargs)
    
    def utf8len(self, s):
        return len(s.encode('utf-8'))

    def getLinkToRoom(self, shard, room):
        return '[link=https://%s%s/#!/room/%s/%s]%s[/link]' % (
            self.config['api_host'], 
            self.config['api_prefix'],
            shard,
            room,
            room
        )

    def getScreepsUserId(self, username):
        res = self.api.user_find(username=username)
        if 'user' in res and '_id' in res['user']:
            return res['user']['_id']
        else:
            self.log('Player', username, 'was not found')
            return None

    def getUserRooms(self, user_id, shard):
        res = self.api.user_rooms(user_id=user_id, shard=shard)
        return res['shards'][shard]

    def getRoomRcl(self, room_objects):
        for room_object in room_objects:
            if room_object['type'] == 'controller':
                return room_object['level']
        return 0

    def getRoomResources(self, room_objects):
        total = {}
        for room_object in room_objects:
            if room_object['type'] in self.config['spy_structures']:
                if 'mineralType' in room_object:
                    total = self.updateTotal(total, room_object['mineralType'], room_object['mineralAmount'])
                elif 'store' in room_object:
                    for resource, amount in room_object['store'].items():
                        total = self.updateTotal(total, resource, amount)
        return total

    def updateTotal(self, total, resource, amount):
        if amount == 0:
            return total
        if resource in total:
            total[resource] += amount
        else:
            total[resource] = amount
        return total

    def updateGrandTotal(self, grand_total, room_total):
        for resource, amount in room_total.items():
            grand_total = self.updateTotal(grand_total, resource, amount)
        return grand_total

    def run(self):
        data = {
            'rooms': {},
            'players': {}
        }

        shard = self.config['target_shard']

        for username in self.config['target_players']:
            if (not self.config['spy_resources'] and
                not self.config['spy_market'] and
                not self.config['spy_rcl']):
                self.log('No spy tasks...')
                sys.exit(0)
            self.log('Gathering intel on ', username, ' in ', shard, '...', sep='')
            user_id = self.getScreepsUserId(username)
            # spy resources
            spy_room = (self.config['spy_resources'] or self.config['spy_rcl'])
            if user_id and spy_room:
                total_resources = {}
                rooms = self.getUserRooms(user_id, shard)
                data['players'][username] = {
                    'rooms': len(rooms)
                }
                for room in rooms:
                    self.log('Scanning room ', self.getLinkToRoom(shard, room), '...', sep='')
                    data['rooms'][room] = {
                        'owner': username
                    }
                    res = self.api.room_objects(room=room, shard=shard)
                    if self.config['spy_resources']:
                        room_resources = self.getRoomResources(res['objects'])
                        if room in self.config['spy_rooms']:
                            data['rooms'][room]['resources'] = room_resources
                        total_resources = self.updateGrandTotal(total_resources, room_resources)
                        data['players'][username]['resources'] = total_resources
                    if self.config['spy_rcl']:
                        rcl = self.getRoomRcl(res['objects'])
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
            data_size = self.utf8len(data_json)
            self.api.set_segment(segment, data_json, shard)
            self.log('Uploaded data (size ', data_size, ') to segment ', segment, ' on ', shard, sep='')

spybot = Spybot()
spybot.run()