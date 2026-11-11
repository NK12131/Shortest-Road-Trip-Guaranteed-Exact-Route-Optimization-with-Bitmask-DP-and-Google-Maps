from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
from humanfriendly import format_timespan
from django.http import JsonResponse
import googlemaps


def RedirectParams(**kwargs):
	'''
	Used to append url parameters when redirecting users
	'''
	url = kwargs.get("url")
	params = kwargs.get("params")
	response = redirect(url)
	if params:
		query_string = urlencode(params)
		response['Location'] += '?' + query_string
	return response


def Directions(*args, **kwargs):
	'''
	Handles directions from Google
	'''

	lat_a = kwargs.get("lat_a")
	long_a = kwargs.get("long_a")
	lat_b = kwargs.get("lat_b")
	long_b = kwargs.get("long_b")
	lat_c = kwargs.get("lat_c")
	long_c = kwargs.get("long_c")
	lat_d = kwargs.get("lat_d")
	long_d = kwargs.get("long_d")
	lat_e = kwargs.get("lat_e")
	long_e = kwargs.get("long_e")
	lat_f = kwargs.get("lat_f")
	long_f = kwargs.get("long_f")
	lat_g = kwargs.get("lat_g")
	long_g = kwargs.get("long_g")

	origin = f'{lat_a},{long_a}'
	destination = f'{lat_b},{long_b}'
	waypoints = f'{lat_c},{long_c}|{lat_d},{long_d}|{lat_e},{long_e}|{lat_f},{long_f}|{lat_g},{long_g}'

	result = requests.get(
		'https://maps.googleapis.com/maps/api/directions/json?',
		 params={
		 'origin': origin,
		 'destination': destination,
		 'waypoints': waypoints,
		 "key": settings.GOOGLE_API_KEY
		 })

	directions = result.json()

	if directions["status"] == "OK":

		routes = directions["routes"][0]["legs"]

		distance = 0
		duration = 0
		route_list = []

		for route in range(len(routes)):

			distance += int(routes[route]["distance"]["value"])
			duration += int(routes[route]["duration"]["value"])

			route_step = {
				'origin': routes[route]["start_address"],
				'destination': routes[route]["end_address"],
				'distance': routes[route]["distance"]["text"],
				'duration': routes[route]["duration"]["text"],

				'steps': [
					[
						s["distance"]["text"],
						s["duration"]["text"],
						s["html_instructions"],

					]
					for s in routes[route]["steps"]]
				}

			
			route_list.append(route_step)
			

	return {
		"origin": origin,
		"destination": destination,
		"distance": f"{round(distance/1000, 2)} Km",
		"duration": format_timespan(duration),
		"route": route_list
		}



class Solution:
    def __init__(self,number_of_places,distance_matrix):
        self.number_of_places = number_of_places
        self.distance_matrix = distance_matrix

        # if all places are visited
        self.visited_all = (1<<self.number_of_places) - 1
        self.dp = [[-1]*self.number_of_places for _ in range(2**self.number_of_places)]
        self.path_dp = {} 

    def tsp(self, mask, position, start_position):
        path = ''
        if mask == self.visited_all:
            return 0, str(position)
        if self.dp[mask][position]!= -1:
            return self.dp[mask][position],self.path_dp[(mask,position)]
		
        # Try to go to unvisited places
        ans = float('inf')
        for place in range(self.number_of_places):
            if mask&(1<<place) == 0:
                dist, new_path = self.tsp(mask|(1<<place), place, start_position)
                new_ans =  self.distance_matrix[position][place] + dist
                if ans > new_ans:
                    ans = new_ans
                    path = new_path
                    
        self.dp[mask][position] = ans		
        self.path_dp[(mask,position)] = f'{position}{path}'
        return self.dp[mask][position], f'{position}{path}'


def fetch_distance(lat1,lat2,lon1,lon2):
    api_key = settings.GOOGLE_API_KEY
    gmaps_client = googlemaps.Client(api_key)
    dist = gmaps_client.distance_matrix([str(lat1) + " " + str(lon1)], [str(lat2) + " " + str(lon2)], mode='driving')['rows'][0]['elements'][0]
    return dist['distance']['value']



def MinimizeTravel(places):
	distance_matrix = [[0]*7 for _ in range(7)]
	if not places:
		return []
	for i in range(7):
		for j in range(7):
			if i==j:
				distance_matrix[i][j] = 0
			distance_matrix[i][j] = fetch_distance(places[i][0],places[j][0],places[i][1],places[j][1])
	soln = Solution(7, distance_matrix)
	min_dist,min_path = float('inf'), '' #Mask and Position and start positions
	for i in range(7):
		dist,path = soln.tsp(1<<i, i , i)
		if dist < min_dist:
			min_dist = dist
			min_path = path
		
	x = list(min_path)
	res = [places[int(i)] for i in x]
	return res

    