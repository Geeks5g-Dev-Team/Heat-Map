import requests
from math import pi, cos, radians, sqrt, atan2, sin
import asyncio
import folium
import googlemaps
import time
import pandas as pd
from lib.radius_grid_rules.KeywordRankingRule import KeywordRankingRule


class GridGenerator ():

    R = 6371
    API_KEY = "AIzaSyCQCXzX0yOAUaIUELv3aI1mIvjPtN8hgZ8"

    def __init__(self):
        self.gmaps = googlemaps.Client(key=self.API_KEY)
        self.keyword_ranking_rules = KeywordRankingRule()

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * \
            cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return self.R * c

    def generate_grid(self, lat, lng, radius_km, step_km):
        grid = []

        lat_step = step_km / self.R * (180 / pi)
        lng_step = step_km / (self.R * cos(radians(lat))) * (180 / pi)

        num_steps = int(radius_km / step_km)

        for i in range(-num_steps, num_steps + 1):
            for j in range(-num_steps, num_steps + 1):
                new_lat = lat + (i * lat_step)
                new_lng = lng + (j * lng_step)

                if self._haversine_distance(lat, lng, new_lat, new_lng) <= radius_km:
                    grid.append((new_lat, new_lng))

        return grid

    def search_places(self, lat, lng, keywords, main_business_cid):
        try:

            google_maps_url = f"https://maps.google.com/?cid={main_business_cid}"
            result = self.keyword_ranking_rules.analyze_ranking_by_keywords(
                lat, lng, keywords, google_maps_url)

            return result
        except Exception:
            return []

    async def async_search(self, grid_points, keywords, main_business_cid):
        tasks = []
        for point in grid_points:
            lat, lng = point
            task = asyncio.to_thread(
                self.search_places, lat, lng, keywords, main_business_cid)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return [place for result in results for place in result]

    def show_map(self, lat, lng, rows):

        map_center = (lat, lng)
        m = folium.Map(location=map_center, zoom_start=14)

        for row in rows:
            folium.Marker(
                location=(row['lat'], row['lng']),
                popup=f"{row['name']} ({row['rating']})"
            ).add_to(m)

        m.save("map.html")

    def geocode(self, address):

        geocode_result = self.gmaps.geocode(address)[0]
        location = geocode_result["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]

        return lat, lng

    def get_places_at_grid_row(self, keywords, lat, lng, radius_km, step_km, main_business_cid):

        places = {}
        grid_points = self.generate_grid(lat, lng, radius_km, step_km)

        for point in grid_points:
            lat, lng = point
            places_at_point = self.search_places(
                lat, lng, keywords, main_business_cid)
            places[lat] = places_at_point
            time.sleep(1)

        return places

    def run(self, address, keywords, cid, radius_km):

        # lat, lng = self.geocode(address)
        lat, lng = 40.234265568726364, -74.27414284183483
#
#         df = self.get_places_at_grid_row(
#             "Clean carpet near me", lat, lng, 40, 4)

        # self.show_map(lat, lng, df.iterrows())

        places = self.get_places_at_grid_row(
            keywords=keywords,
            lat=lat,
            lng=lng,
            main_business_cid=cid,
            radius_km=radius_km,
            step_km=radius_km / 10,
        )

#         new_grid = [
#             {
#                 "lat":
#             }
#             for place in places
#         ]
#
#         new_grid = [{
#             "lat": lat,
#             "lng": lng,
#             "name": lat,
#             "rating": 5
#         } for lat, lng in grid]

        # self.show_map(lat, lng, new_grid)

        return places
