from django.shortcuts import render, redirect, reverse
from django.conf import settings
import googlemaps
from did_django_google_api_tutorial.mixins import Directions, fetch_distance, MinimizeTravel, Solution


'''
Basic view for entering Number of places
'''
def Number_of_places(request):
	return render(request, 'main/Number_of_places.html')


'''
Basic view for routing 
'''
def route(request):
	# # num = range(int(request.POST.get('number_of_places',2)))
	# num = range(7)
	# arr = []
	# for i in num:
	# 	arr.append(chr(i+ord('a')))
	
	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"base_country": settings.BASE_COUNTRY
	}
	return render(request, 'main/route.html', context)

'''
Basic view for displaying a map 
'''
def map(request):
	lat_a = request.GET.get("lat_a", None)
	long_a = request.GET.get("long_a", None)
	lat_b = request.GET.get("lat_b", None)
	long_b = request.GET.get("long_b", None)
	lat_c = request.GET.get("lat_c", None)
	long_c = request.GET.get("long_c", None)
	lat_d = request.GET.get("lat_d", None)
	long_d = request.GET.get("long_d", None)
	lat_e = request.GET.get("lat_e", None)
	long_e = request.GET.get("long_e", None)
	lat_f = request.GET.get("lat_f", None)
	long_f = request.GET.get("long_f", None)
	lat_g = request.GET.get("lat_g", None)
	long_g = request.GET.get("long_g", None)

	places = [(lat_a, long_a), (lat_b, long_b),(lat_c, long_c), (lat_d, long_d), (lat_e, long_e), (lat_f, long_f), (lat_g, long_g)]

	#only call API if all 7 addresses are added
	if lat_a and lat_b and lat_c and lat_d:
		new_places = MinimizeTravel(places)
		lat_a, long_a = new_places[0]
		lat_b, long_b = new_places[6]
		lat_c, long_c = new_places[1]
		lat_d, long_d = new_places[2]
		lat_e, long_e = new_places[3]
		lat_f, long_f = new_places[4]
		lat_g, long_g = new_places[5]
		directions = Directions(
			lat_a = lat_a,
			long_a=long_a,
			lat_b = lat_b,
			long_b=long_b,
			lat_c = lat_c,
			long_c=long_c,
			lat_d = lat_d,
			long_d=long_d,
			lat_e = lat_e,
			long_e=long_e,
			lat_f = lat_f,
			long_f=long_f,
			lat_g = lat_g,
			long_g=long_g
			)
	else:
		return redirect(reverse('main:route'))

	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"base_country": settings.BASE_COUNTRY,
	"lat_a": lat_a,
	"long_a": long_a,
	"lat_b": lat_b,
	"long_b": long_b,
	"lat_c": lat_c,
	"long_c": long_c,
	"lat_d": lat_d,
	"long_d": long_d,
	"lat_e": lat_e,
	"long_e": long_e,
	"lat_f": lat_f,
	"long_f": long_f,
	"lat_g": lat_g,
	"long_g": long_g,
	"origin": f'{lat_a}, {long_a}',
	"destination": f'{lat_b}, {long_b}',
	"directions": directions,

	}

	return render(request, 'main/map.html', context)


