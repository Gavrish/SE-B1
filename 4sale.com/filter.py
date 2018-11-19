from utils import *
import map

# A class to carry out property filtering tasks
class Filter:
    # Initialize with special types of filtering metrics
    def __init__(self):
        self.l = ['min_price','max_price','min_area','max_area']
        
    # A Level 1 function to carry out all the basic filering based on basic attributes like noOfBedrooms,etc. If there are other types of attributes given for filterings, this function calls another function to perform that type of filering
    def basic_filter(self,data,db):
        # A dictionary to store all the basic filtering attributes
        d = {}
        # A list to store all the extra conditions for mincost,maxcost,minarea and maxarea
        extra_conditions = []
        # A list to store all the tags based on which properties have to be filtered
        tags = []
        # A list to store all the advanced filter attributes like distance to hospital,etc
        advanced_filter_items = []
        # Iterate over all the data obtained from the filter form
        for key,value in data.items():
            # Store the data accordingly
            if(data[key]):
                if(key.startswith('tag')):
                    tags.append(key.split('_')[1])
                elif(key.startswith('distance')):
                    advanced_filter_items.append([key,value])
                elif(key.startswith('time')):
                    advanced_filter_items.append([key,value])
                elif(key=='greencover'):
                    advanced_filter_items.append([key,value])
                elif(key.startswith('place')):
                    advanced_filter_items.append([key,value])
                elif(key not in self.l):
                    if(key != 'type' or (key == 'type' and value!='Any')):
                        d[key] = value
                else:
                    if(key=='min_price'):
                        extra_conditions.append(" cost " + ">=" + value)
                    elif(key=='max_price'):
                        extra_conditions.append(" cost " + "<=" + value)
                    elif(key=='min_area'):
                        extra_conditions.append(" area " + ">=" + value)
                    elif(key=='max_area'):
                        extra_conditions.append(" area " + "<=" + value)
        # Generate the query string
        query_string = db.query_string_from_dict('properties',d)
        if('where' not in query_string.split() and len(extra_conditions) > 0):
            if(len(extra_conditions)==1):
                query_string += " where " + extra_conditions[0]
            else:    
                query_string += " where " + " and ".join(extra_conditions)
        elif(len(extra_conditions) > 0):
            if(len(extra_conditions)==1):
                query_string +=  " and " + extra_conditions[0]
            else:    
                query_string += " and " + " and ".join(extra_conditions)
        print(query_string)
        # If there are no tags
        if(len(tags)==0):
            # Execute if there are no advanced filtering items
            if(len(advanced_filter_items)==0):
                return db.execute_query_string(query_string)
            # Call advanced_filters to filter furthur
            else:
                return self.advanced_filters(db.execute_query_string(query_string),advanced_filter_items,db)
        # If there are tags
        else:
            return self.checkTags(db.execute_query_string(query_string),tags,db)
     
    # A function to shortlist properties from a given list of properties. A property is shortlisted if it has all the given tags 
    def checkTags(self,property_items,input_tags,db):
        items = []
        for property_item in property_items:
            tags = db.query('tags',pid=property_item['pid'],cols=['tag'])
            tags_list = generate_tag_list(tags)
            print(tags_list)
            if(all(i in tags_list for i in input_tags)):
                items.append(property_item)
        return items
    
    # A Level 2 function to shortlist properties from a given list of properties based on attributes like distance and time to nearest hospitals,gyms,etc and greencover. If traffic based filtering is still needed, it calls another function to test traffic metrics and shortlist accordingly
    def advanced_filters(self,property_items,advanced_filter_items,db):
        items = []
        for property_item in property_items:
            property_analytics = db.query('property_analytics',pid=property_item['pid'])[0]
            numberOfPasses = 0
            place_attributes = {}
            # Check for every advanced_filter_items metric
            for key,value in advanced_filter_items:
                if(key.startswith('distance')):
                    if(float(property_analytics[key+'1'])/1000 <= float(value) or float(property_analytics[key+'2'])/1000 <= float(value)):
                        numberOfPasses += 1
                elif(key.startswith('time')):
                    if(float(property_analytics[key+'1'])/60 <= float(value) or float(property_analytics[key+'2'])/60 <= float(value)):
                        numberOfPasses += 1
                elif(key=='greencover'):
                    if(float(property_analytics['green_cover']) >= float(value)):
                        numberOfPasses += 1
                elif(key.startswith('place')):
                    place_attributes[key] = value
            # If it passes all metrics
            if(numberOfPasses==len(advanced_filter_items)):
                items.append(property_item)
            # If traffic filtering is needed
            elif(len(place_attributes) > 0 and numberOfPasses == len(advanced_filter_items)-len(place_attributes)):
            	distance = float(place_attributes['place_distance']) if 'place_distance' in place_attributes else None
            	time = float(place_attributes['place_time']) if 'place_time' in place_attributes else None
                # Check if it passes traffic based filtering
            	if(self.traffic_filter(property_item,place_attributes['place']+' '+place_attributes['place_locality'],distance=distance,time=time)):
            		items.append(property_item)
        print(items)
        return items
    
    # A function that takes a property, place, distance and time and returns True if one can reach property to place in the given distance/time else returns False  
    def traffic_filter(self,property_item,place,distance=None,time=None):
        map_services = map.MapServices()
        property_coordinates = {'lat':property_item['latitude'],'lng':property_item['longitude']}
        result = map_services.get_distance_metrics(property_coordinates,place)
        if(distance and not(time)):
        	if(result[2]/1000 <= distance):
        		return True
        	else:
        		return False
        elif(not(distance) and time):
        	if(result[3]/60 <= time):
        		return True
        	else:
        		return False
        elif(distance and time):
        	if(result[2]/1000<=distance and result[3]/60<=time):
        		return True
        	else:
        		return False
        else:
        	return False
