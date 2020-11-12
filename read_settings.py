import json

def read_settings_file():
    with open("settings.json") as f:
        data = json.load(f)

        # 'Default' value for parameter: try to find it in settings
        # file, otherwise default it
        try:
            data['step_number']
        except Exception as e:
            data['step_number'] = 200
            
        return data

if __name__ == "__main__":
    settings = read_settings_file()
    print(settings)
