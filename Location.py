import settings
import requests
import json
import datetime

request_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&mode=walking&key={2}'

class Location:
    def __init__(self, loc):
        location = loc.split(' ')
        self.building = " ".join(location[:-1])
        self.room = location[-1]

    def get_time_between(self, other):
        if not isinstance(other, Location):
            raise TypeError("Other must be a Location")
        if self.building == 'TBA' or other.building == 'TBA':
            return datetime.timedelta(minutes=20)

        # edge case corrections
        if self.building == 'Energy Prod & Infrastructr Ctr': self.building = 'EPIC'
        if other.building == 'Energy Prod & Infrastructr Ctr': other.building = 'EPIC'

        origin = self.building.replace(' ','+') + ',+Charlotte,+NC+28223'
        destination = other.building.replace(' ','+') + ',+Charlotte,+NC+28223'
        response = requests.get(request_url.format(origin, destination, settings.API_KEY))

        directions = json.loads(response.text)
        time = directions['routes'][0]['legs'][0]['duration']['value']
        return datetime.timedelta(seconds=int(time))

    def __str__(self):
        return self.building +' '+ self.room

