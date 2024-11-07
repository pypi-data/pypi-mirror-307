import os
import yaml

local_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(local_path)


class Config:
    def __init__(self):
        self.file_path = os.path.join(root_path, 'running', 'conf.yml')

    def __getitem__(self, key):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        try:
            return yaml_data['common'][key]
        except:
            return None

    def __setitem__(self, key, value):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        # if key in yaml_data['common']:
        #     yaml_data['common'][key] = value
        # else:
        #     raise KeyError(f'{key} not in {yaml_data["common"]}')
        yaml_data['common'][key] = value
        with open(self.file_path, 'w', encoding="utf-8") as f:
            yaml.dump(yaml_data, f)

    def __len__(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return len(yaml_data['common'])

    def __repr__(self):  # 用于终端显示，与本博文关系不大
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return str(yaml_data['common'])

    def reset(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        yaml_data['common'] = {
            'base_url': None,
            'headers': None,
            'project': None,
            'web_url': None
        }
        with open(self.file_path, 'w', encoding="utf-8") as f:
            yaml.dump(yaml_data, f)


kconfig = Config()

if __name__ == '__main__':
    print(kconfig['project'])

