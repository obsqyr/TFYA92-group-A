import json

def read_settings_file():
    with open("settings.json") as f:
        data = json.load(f)

        # 'Default' value for parameter: try to find it in settings
        # file, otherwise default it
        try:
            data['time_step']
        except Exception as e:
            data['time_step'] = 5
        try:
            data['max_steps']
        except Exception as e:
            data['max_steps'] = 200
        try:
            data['temperature']
        except Exception as e:
            data['temperature'] = 300
        try:
            data['ensemble']
        except Exception as e:
            data['ensemble'] = "NVE"
        try:
            data['friction']
        except Exception as e:
            data['friction'] = "0.001"
        try:
            data['LJ_epsilon']
        except Exception as e:
            data['LJ_epsilon'] = 0.010323
        try:
            data['LJ_sigma']
        except Exception as e:
            data['LJ_sigma'] = 3.40
        try:
            data['LJ_rcutoff']
        except Exception as e:
            data['LJ_rcutoff'] = 6.625
        return data

if __name__ == "__main__":
    settings = read_settings_file()
    print(settings)
