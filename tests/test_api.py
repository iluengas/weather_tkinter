import unittest
from scripts.get_weather import make_weather_api_request


class TestApiRequest(unittest.TestCase):
    """Test Class for API requests"""

    def test_api_status_code(self):
        """
        Tests that a status code of 200 is returned

        Parameters: 
        None


        Returns:
        None
        """
        response = make_weather_api_request("ventura")
        response_data = response.json()
        self.assertEqual(response_data.get("cod"), 200)


if __name__ == '__main__':
    unittest.main()
