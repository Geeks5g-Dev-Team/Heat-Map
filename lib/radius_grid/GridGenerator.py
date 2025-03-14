import requests
from math import pi, cos, radians, sqrt, atan2, sin
import asyncio
import folium
import googlemaps
import time
import pandas as pd
from lib.radius_grid_rules.KeywordRankingRule import KeywordRankingRule
import threading
from lib.radius_grid_rules.KeywordRankingRule import AnalyzeRankingWithKeywordsReturnParams
from lib.radius_grid.ShowMap import ShowMap


class GridGenerator ():

    R = 6371
    API_KEY = "AIzaSyCQCXzX0yOAUaIUELv3aI1mIvjPtN8hgZ8"

    def __init__(self):
        self.keyword_ranking_rules = KeywordRankingRule()
        self.map = ShowMap()

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
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def get_places_at_grid_row(self, keywords, lat, lng, radius_km, step_km, main_business_cid):

        grid_points = self.generate_grid(lat, lng, radius_km, step_km)

        half_grid = grid_points[0:(len(grid_points) - 1) // 2]
        final_half_grid = grid_points[(
            (len(grid_points) - 1) // 2) + 1:len(grid_points) - 1]

        thread_1 = [
            asyncio.to_thread(self.search_places, g_lat,
                              g_lng, keywords, main_business_cid)
            for g_lat, g_lng in half_grid
        ]

        thread_2 = [
            asyncio.to_thread(self.search_places, g_lat,
                              g_lng, keywords, main_business_cid)
            for g_lat, g_lng in final_half_grid
        ]
        # tasks = [asyncio.to_thread(self.search_places,
        #                            grid_lat, grid_lng, keywords, main_business_cid) for grid_lat, grid_lng in grid_points]

        searches = await asyncio.gather(*[*thread_1, *thread_2])

        return searches

    async def run(self, address, keywords, cid, radius_km, step_km):

        lat, lng = 29.9357285, -95.49863359999999

        places = await self.get_places_at_grid_row(
            keywords=keywords,
            lat=lat,
            lng=lng,
            main_business_cid=cid,
            radius_km=radius_km,
            step_km=step_km,
        )

        self.map.show_map(lat, lng, places, "Bemmel")

        return places
