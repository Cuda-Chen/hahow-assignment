import unittest
import urllib.request
import json


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api_base_url = "https://swapi.info/api/"
        self.films = self.get_json_content(self.api_base_url + "films")

    # FIXME: pre-cache the character and species data
    def test_race_count_in_sixth_episode(self):
        expected_race_count = 9

        races = set()
        films = self.films
        episode = next((x for x in films if x["episode_id"] == 6), None)

        for character_url in episode["characters"]:
            character = self.get_json_content(character_url)
            species_url = character["species"]
            species = (
                self.get_json_content(species_url[0]) if len(species_url) > 0 else None
            )
            name = "Human" if species is None else species["name"]
            races.add(name)

        self.assertEqual(len(races), expected_race_count)

    def test_sorted_title(self):
        film_names = []
        expected_names_sorted = [
            [1, "The Phantom Menace"],
            [2, "Attack of the Clones"],
            [3, "Revenge of the Sith"],
            [4, "A New Hope"],
            [5, "The Empire Strikes Back"],
            [6, "Return of the Jedi"],
        ]
        for f in self.films:
            film_names.append([f["episode_id"], f["title"]])

        self.assertEqual(sorted(film_names, key=lambda x: x[0]), expected_names_sorted)

    def test_horsepower_count(self):
        vehicle_url = self.api_base_url + "vehicles"
        vehicles = self.get_json_content(vehicle_url)
        horsepower = 1000
        targets = set()
        expected_vehicles = {
            "T-16 skyhopper",
            "TIE/LN starfighter",
            "Storm IV Twin-Pod cloud car",
            "TIE/IN interceptor",
            "Vulture Droid",
            "Geonosian starfighter",
            "Droid tri-fighter",
        }

        for vehicle in vehicles:
            speed = vehicle["max_atmosphering_speed"]
            if self.is_int(speed) and int(speed) > horsepower:
                targets.add(vehicle["name"])

        self.assertEqual(targets, expected_vehicles)

    # helper of getting JSON content
    def get_json_content(self, url):
        with urllib.request.urlopen(url) as u:
            data = json.loads(u.read().decode())
            return data

    # check whether a string can be parsed as integer
    def is_int(self, s: any) -> bool:
        if s is None:
            return False
        try:
            int(s)
            return True
        except:
            return False


if __name__ == "__main__":
    unittest.main()
