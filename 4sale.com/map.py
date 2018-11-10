import googlemaps

class MapServices:
    def __init__(self):
        self.gmaps = googlemaps.Client(key='AIzaSyDRjavHrEvei0wuHLRYUEbEtRH3YMGcKpQ')
        self.place_types = ['hospital','bank','book_store','bus_station','school','clothing_store','restaurant','gym','gas_station','electronics_store','supermarket','beauty_salon','car_repair','cafe','bakery','dentist','hindu_temple','atm']
    
    def geocode_address(self,address):
        geocoding = self.gmaps.geocode(address)
        location = geocoding[0]['geometry']['location']
        self.lat = location['lat']
        self.long = location['lng']
        
    def set_coordinates(self,lat,long):
        self.lat = lat
        self.long = long
        
    def get_distance_metrics(self,origin,destination):
        distance_metrics = self.gmaps.distance_matrix([origin],[destination],mode='driving')['rows'][0]['elements'][0]
        return distance_metrics['distance']['text'], distance_metrics['duration']['text'], distance_metrics['distance']['value'], distance_metrics['duration']['value']
    
    def generate_top_two_closest_places(self):
        self.places = {}
        for place in self.place_types:
            places_result = self.gmaps.places_nearby(location=(self.lat,self.long),type=place,rank_by='distance')['results']
            self.places[place] = { place+'1': {'name':places_result[0]['name'], 'location': places_result[0]['geometry']['location'] } , place+'2': {'name':places_result[1]['name'], 'location': places_result[1]['geometry']['location'] } }
            
    def generate_distances(self):
        self.distances = {}
        for place in self.places:
            d1 = self.get_distance_metrics(self.places[place][place+'1']['location'],{'lat':self.lat,'lng':self.long})
            d2 = self.get_distance_metrics(self.places[place][place+'2']['location'],{'lat':self.lat,'lng':self.long})
            self.distances[place] = { place+'1': {'name':self.places[place][place+'1']['name'], 'distance': d1[2], 'time': d1[3], 'message': ' '.join([d1[0],d1[1]]) } , place+'2': {'name':self.places[place][place+'2']['name'], 'distance': d2[2], 'time': d2[3], 'message': ' '.join([d2[0],d2[1]]) } }
            