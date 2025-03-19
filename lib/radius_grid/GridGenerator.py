import requests
from math import pi, cos, radians, sqrt, atan2, sin
import asyncio
import folium
import googlemaps
import time
import pandas as pd
# from lib.radius_grid_rules.KeywordRankingRule import KeywordRankingRule
from lib.radius_grid_rules.KeywordRankingRuleByScrapping import KeywordRankingRuleByScrapping
import threading
# from lib.radius_grid_rules.KeywordRankingRule import AnalyzeRankingWithKeywordsReturnParams
from lib.radius_grid.ShowMap import ShowMap
from lib.utilities.thread_handler_execution import thread_handler_execution


class GridGenerator ():

    R = 6371
    API_KEY = "AIzaSyCQCXzX0yOAUaIUELv3aI1mIvjPtN8hgZ8"

    def __init__(self):
        # self.keyword_ranking_rules = KeywordRankingRule()
        self.ranking_by_scrapping_rules = KeywordRankingRuleByScrapping()
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

    async def search_places(self, lat, lng, keywords, cid, search_by_scrapping=False):
        try:

            if search_by_scrapping:
                result = await self.ranking_by_scrapping_rules.analyze_ranking_by_keywords(
                    business_name=cid,
                    keywords=keywords,
                    lat=lat,
                    lng=lng
                )
            else:
                pass
                # google_maps_url = f"https://maps.google.com/?cid={cid}"
                # result = self.keyword_ranking_rules.analyze_ranking_by_keywords(
                #     lat, lng, keywords, google_maps_url)

            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def get_places_at_grid_row(self, keywords, lat, lng, radius_km, step_km, cid, search_businesses_by_scrapping=False):

        grid_points = self.generate_grid(lat, lng, radius_km, step_km)

        thread_execution = await thread_handler_execution(
            arr=grid_points,
            callback=lambda chunk: asyncio.gather(
                *(self.search_places(ch[0], ch[1], keywords, cid, search_businesses_by_scrapping) for ch in chunk)
            ),
            max_workers=5,
            max_thread_pools=10
        )

        # tasks = [asyncio.to_thread(self.search_places,
        #                            grid_lat, grid_lng, keywords, cid, search_businesses_by_scrapping) for grid_lat, grid_lng in grid_points]
        # tasks = [await self.search_places(
        #     grid_lat, grid_lng, keywords, cid, search_businesses_by_scrapping) for grid_lat, grid_lng in grid_points]

        # searches = await asyncio.gather(*tasks)

        return thread_execution

    async def run(self, address, keywords, cid, radius_km, step_km):

        lat, lng = 29.93605980242429, -95.49824496675434
        search_businesses_by_scrapping = True

        places = await self.get_places_at_grid_row(
            keywords=keywords,
            lat=lat,
            lng=lng,
            cid=cid,
            radius_km=radius_km,
            step_km=step_km,
            search_businesses_by_scrapping=search_businesses_by_scrapping
        )

        self.map.show_map(lat, lng, places, "philly")

        return places
