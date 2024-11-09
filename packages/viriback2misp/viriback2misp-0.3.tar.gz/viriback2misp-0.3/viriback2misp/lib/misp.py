from .viriback import C2

from pymisp import PyMISP
from pymisp import MISPEvent, MISPObject
from datetime import datetime as dt
import urllib3

urllib3.disable_warnings()

class Mispao():
    def __init__(self, misp_url:str, misp_api_key:str, distribution:int=0) -> None:
        try:
            self.misp = PyMISP(misp_url, misp_api_key, False, True) 
            month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            
            data = C2().get_C2()
            for date, values in data.items():
                month_str = date.split('-')[-1]
                currentMonth = month[int(month_str) -1]
                year = date.split('-')[0]
                family = C2().split_by_family(values)
                for family_name, items in family.items():
                    info = f'{family_name} C2 Tracker - {currentMonth}/{year}'
                    event_id = self.event_exists(info)
                    if not event_id:
                        event_id = self.create_event(info, distribution)
                    if event_id:
                        for item in items:
                            if self.attribute_exists(event_id, item.get('url')):
                                print(f"{item.get('url')} exist in event {event_id}")
                                continue
                            port = ''
                            url = item.get('url').split('.')[-1]
                            if ':' in url:
                                if '/' in url:
                                    url = url.split('/')[0]
                                port = url.split(':')[-1] if len(url.split(':')[-1]) > 1 else ''                   
                            if port:
                                self.add_obj_to_event(event_id, item.get('ip'), item.get('url'), item.get('firstseen'), port)
                            else:
                                self.add_obj_to_event(event_id, item.get('ip'), item.get('url'), item.get('firstseen'))
        except Exception as err:
            print(f"Error: {err}")

    def event_exists(self, info):
        try:
            search_results = self.misp.search(eventinfo=info)
            
            if search_results:
                return search_results[0].get('Event').get('id')
            else:
                return None
        except Exception as err:
            print(f'Event_exists error: {err}')

    def attribute_exists(self, event_id, value):
        search_results = []
        search_results = self.misp.search(eventid=event_id, value=value)
        return search_results

    def create_event(self, info:str, distribution:int=0):
        event_obj = MISPEvent()
        event_obj.info = info
        event_obj.distribution = distribution
        event_obj.threat_level_id = 3
        event_obj.analysis = 1
        event_obj.add_tag('tlp:ambar')
        event = self.misp.add_event(event_obj, pythonify=True)
        if event:
            print(f"Event {event.id} created")
            return event.id
        return None

    def add_obj_to_event(self, event_id, ip:str, url:str, date:str, port=None):
        event = self.misp.get_event(event_id, pythonify=True)  

        new_object = MISPObject('url')
        new_object = event.add_object(new_object)

        new_object.add_attribute('url', value=url, type='url')
        new_object.add_attribute('first-seen', value=date, type='datetime')
        new_object.add_attribute('ip', value=ip, type='ip-dst')
        
        if port:
            new_object.add_attribute('port', value=port, type='port')
        self.misp.update_event(event=event)
        print(f"Object created in event {event_id}")