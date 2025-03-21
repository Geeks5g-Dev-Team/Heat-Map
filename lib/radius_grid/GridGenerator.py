import requests
from math import pi, cos, radians, sqrt, atan2, sin, degrees
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
from services.scraping.main import ScrapeGoogleMapsSearch
import numpy as np


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

    def generate_grid(self, lat, lng, radius_km, step_km, is_square=False):
        grid = [(lat, lng)]  # Include the main coordinate

        if is_square:
            # Square Grid (Same as before, but structured properly)
            lat_step = step_km / self.R * (180 / pi)
            lng_step = step_km / (self.R * cos(radians(lat))) * (180 / pi)
            num_steps = int(radius_km / step_km)

            for i in range(-num_steps, num_steps + 1):
                for j in range(-num_steps, num_steps + 1):
                    new_lat = lat + (i * lat_step)
                    new_lng = lng + (j * lng_step)
                    if self._haversine_distance(lat, lng, new_lat, new_lng) <= radius_km:
                        grid.append((new_lat, new_lng))
        else:
            # True Circular Grid using Polar Coordinates
            num_rings = int(radius_km / step_km)
            for r in range(1, num_rings + 1):
                radius = r * step_km
                # Ensure a minimum of 6 points per ring
                num_points = max(6, int(2 * pi * radius / step_km))
                for theta in np.linspace(0, 2 * pi, num_points, endpoint=False):
                    new_lat = lat + degrees(radius / self.R) * sin(theta)
                    new_lng = lng + \
                        degrees(radius / (self.R * cos(radians(lat)))
                                ) * cos(theta)
                    grid.append((new_lat, new_lng))

        return grid

    def generate_grid_by_count(self, grid_points, grid_spacing_km, lat, lng, is_square=False):
        grid = [(lat, lng)]  # Include the main coordinate

        if is_square:
            num_steps = int((grid_points ** 0.5) // 2)
            lat_step = grid_spacing_km / self.R * (180 / pi)
            lng_step = grid_spacing_km / \
                (self.R * cos(radians(lat))) * (180 / pi)

            for i in range(-num_steps, num_steps + 1):
                for j in range(-num_steps, num_steps + 1):
                    new_lat = lat + (i * lat_step)
                    new_lng = lng + (j * lng_step)
                    grid.append((new_lat, new_lng))
        else:
            generated_count = 1
            ring = 0
            while generated_count < grid_points:
                ring += 1
                radius = ring * grid_spacing_km
                num_points = max(6, int(2 * pi * radius / grid_spacing_km))
                # Ensure we don't exceed count
                num_points = min(num_points, grid_points - generated_count)
                for theta in np.linspace(0, 2 * pi, num_points, endpoint=False):
                    new_lat = lat + degrees(radius / self.R) * sin(theta)
                    new_lng = lng + \
                        degrees(radius / (self.R * cos(radians(lat)))
                                ) * cos(theta)
                    grid.append((new_lat, new_lng))
                    generated_count += 1
                    if generated_count >= grid_points:
                        return grid

        return grid

    async def search_places(self, lat, lng, keywords, cid, search_by_scrapping=False, **kwargs):
        try:

            if search_by_scrapping:

                result = await self.ranking_by_scrapping_rules.analyze_ranking_by_keywords(
                    business_name=cid,
                    keywords=keywords,
                    lat=lat,
                    lng=lng,
                    **kwargs
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

    async def get_places_at_grid_row(self, keywords, lat, lng, cid, search_businesses_by_scrapping=False):

        grid_points = self.generate_grid_by_count(
            grid_points=self.grid_points,
            grid_spacing_km=self.grid_spacing,
            is_square=False,
            lat=lat,
            lng=lng
        )

        # pw_instance = await ScrapeGoogleMapsSearch.playwright_instance()

        thread_execution = await thread_handler_execution(
            arr=grid_points,
            callback=lambda chunk: asyncio.gather(
                *(self.search_places(ch[0], ch[1], keywords, cid, search_businesses_by_scrapping) for ch in chunk)
            ),
            max_workers=10,
            max_thread_pools=3
        )

        # tasks = [asyncio.to_thread(self.search_places,
        #                            grid_lat, grid_lng, keywords, cid, search_businesses_by_scrapping) for grid_lat, grid_lng in grid_points]
        # tasks = [await self.search_places(
        #     grid_lat, grid_lng, keywords, cid, search_businesses_by_scrapping) for grid_lat, grid_lng in grid_points]

        # searches = await asyncio.gather(*tasks)

        return thread_execution

    async def run(self, address, keywords, cid):

        lat, lng = 29.93605980242429, -95.49824496675434
        self.grid_spacing = 1
        self.grid_points = 130

        search_businesses_by_scrapping = True

        places = await self.get_places_at_grid_row(
            keywords=keywords,
            lat=lat,
            lng=lng,
            cid=cid,
            search_businesses_by_scrapping=search_businesses_by_scrapping
        )

        self.map.show_map(lat, lng, places, "philly")

        print(f"Length: {len(places)}")
        return places


"""

169 grid points will cost:

0.32 dollars will cost 20 request compared to 500 users
149 browser iterations

For 100 keywords each grid:

500 us = 8.450.000 api calls
500 by 20 calls = 1.000.000 = 45 dollars
"""
