import requests
from datetime import datetime
import json
from tqdm import tqdm
import configparser




class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = vk_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.photo_profile_dict = {}

    def photos_profile(self, count=5):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': album,
                  'extended': 1,
                  'photo_sizes': 1,
                  'count': count}
        response = requests.get(url, params={**self.params, **params})
        result = response.json()

        for photo in tqdm(result['response']['items'], desc='Формирование списка'):
            sum_like = sum(photo['likes'].values())

            sizes_list = []
            for sizes in photo['sizes']:
                sizes_list += [sizes]

            max_sizes_dict = {'width': 0, 'height': 0}
            for sizes in sizes_list:
                if sizes['width'] == 0 or sizes['height'] == 0:
                    if sizes['type'] == 's':
                        sizes['width'] = 75
                        sizes['height'] = 75
                    if sizes['type'] == 'm' or sizes['type'] == 'o':
                        sizes['width'] = 130
                        sizes['height'] = 130
                    if sizes['type'] == 'p':
                        sizes['width'] = 200
                        sizes['height'] = 200
                    if sizes['type'] == 'q':
                        sizes['width'] = 320
                        sizes['height'] = 320
                    if sizes['type'] == 'r':
                        sizes['width'] = 510
                        sizes['height'] = 510
                    if sizes['type'] == 'x':
                        sizes['width'] = 604
                        sizes['height'] = 604
                    if sizes['type'] == 'y':
                        sizes['width'] = 807
                        sizes['height'] = 807
                    if sizes['type'] == 'z':
                        sizes['width'] = 1080
                        sizes['height'] = 1024
                    if sizes['type'] == 'w':
                        sizes['width'] = 2560
                        sizes['height'] = 2048

                if sizes['width'] > max_sizes_dict['width']:
                    max_sizes_dict = sizes

            if sum_like in self.photo_profile_dict.keys():
                real_date = datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d %H:%M:%S')[0:10]
                self.photo_profile_dict[f'{sum_like}, {real_date}'] = max_sizes_dict
            else:
                self.photo_profile_dict[sum_like] = max_sizes_dict

        return self.photo_profile_dict

    def get_json(self):
        json_list = []
        for like, data in self.photo_profile_dict.items():
            json_dict = {}
            json_dict['file_name'] = f'{like}.jpg'
            json_dict['size'] = data['type']
            json_list += [json_dict]
        with open('info.json', 'w') as f:
            json.dump(json_list, f, ensure_ascii=False, indent=2)
        return json_list

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return { 'Content-Type': 'application/json',
                 'Authorization': 'OAuth {}'.format(self.token)}


    def _get_upload_link(self, file_path):
        url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(url_upload, headers = headers, params=params)

        return response.json()


    def upload(self, file_link):
        result = self._get_upload_link(path_to_file)
        url = result['href']
        resource = requests.get(url= file_link)
        response = requests.post(url=url, files = {'file': resource.content })
        if response.status_code == 201:
            return
        else:
            return print(response.status_code)

    def create_folder(self, folder_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': folder_path}
        response = requests.put(url=url, params=params, headers=headers)
        if response.status_code == 201:
            return print('Папка успешно создана')
        else: return print(response.status_code,'\n',response.text)


# Я так добывал токены
# config = configparser.ConfigParser()
# config.read('settings.ini')
# vk_token = config['Tokens']['vk_token']
# ya_token = config['Tokens']['ya_token']

vk_token = input('Введите токен для VK')
ya_token = input('Введите токен Яндекс диска')
user_id = input('Введите id пользователя')
album = input('Введите wall для загрузки со стены или profile для загрузки с профиля')
try:
    number = int(input(('Введите количество фотографий')))
except ValueError:
    number = 5
folder_path = '/Папка для курсовоq'

if __name__ == '__main__':
    vk = VK(vk_token, user_id)
    ya = YaUploader(ya_token)

    vk.photos_profile(number)
    vk.get_json()
    ya.create_folder(folder_path)


    for like, data in tqdm(vk.photo_profile_dict.items(), ncols=80, desc='Загрузка'):
        tqdm.write(f'{like}')
        path_to_file = folder_path +'/'+ f'{like}'+'.jpg'
        ya = YaUploader(ya_token)
        ya.upload(data['url'])
        print('\n')
