import os.path
import os
import unittest
import json
import read_settings

class TestConfFile(unittest.TestCase):
    def test_settings(self):
        # Does the file exist?
        self.assertTrue(os.path.exists("settings.json"))
        with open("settings.json") as f:
            data = json.load(f)
        # Check if the keys are there
        tmp_keys = ['max_steps', 'temperature', 'ensemble',
            'friction', 'decimals']
        self.assertTrue(set(data.keys()).issubset(tmp_keys))

    def test_read_settings(self):
    # create empty json file
        with open("empty_test.json", "w+") as f:
            f.write("{\n    \"koko\": 1000 \n}")
        with open("empty_test.json") as f:
            data = json.load(f)
        with self.assertRaises(KeyError):
            data["temperatur"]

        # Now test read_settings_file function
        data = read_settings.read_settings_file("empty_test.json")
        self.assertTrue(data["time_step"], 5)
        self.assertTrue(data["max_steps"], 200)
        self.assertTrue(data["temperature"], 300)
        self.assertTrue(data["ensemble"], "NVE")
        self.assertTrue(data["friction"], 0.001)
        self.assertTrue(data["decimals"], 5)
        os.remove("empty_test.json")


if __name__ == '__main__':
    unittest.main()
