import requests
from pprint import pprint
from datetime import datetime

class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def photos_profile(self, count):
       url = 'https://api.vk.com/method/photos.get'
       params = {'owner_id': self.id,
                 'album_id': 'profile',
                 'extended': 1,
                 'photo_sizes': 1,
                 'count': count}
       response = requests.get(url, params={**self.params, **params})
       result = response.json()

       sizes_list = []
       max_sizes_dict = {'type': 0}
       like_dict = {}

       for photo in result['response']['items']:
           sum_like = sum(photo['likes'].values())
           if sum_like in like_dict:
               like_dict[sum_like, photo['date']] = ''
           like_dict[sum_like] = ''

           for sizes in photo['sizes']:
               sizes_list += [sizes]

           for sizes in sizes_list:
               if sizes['type'] == 's': sizes['type'] = [75,'px']
               if sizes['type'] == 'm' or sizes['type'] == 'o': sizes['type'] = [130,'px']
               if sizes['type'] == 'p': sizes['type'] = [200, 'px']
               if sizes['type'] == 'q': sizes['type'] = [320,'px']
               if sizes['type'] == 'r': sizes['type'] = [510, 'px']
               if sizes['type'] == 'x': sizes['type'] = [604, 'px']
               if sizes['type'] == 'y': sizes['type'] = [807, 'px']
               if sizes['type'] == 'z': sizes['type'] = [1080, 1024]
               if sizes['type'] == 'w': sizes['type'] = [2560, 2048]

               if sizes['type'][0] > max_sizes_dict['type']:
                   like_dict[sum_like] = sizes
                   like_dict[sum_like, photo['date']] = sizes
                   # else:
                   #     like_dict[sum_like, photo['date']] = sizes




       # pprint(like_dict)



       return pprint(like_dict)


access_token = 'vk1.a.u86bRMTpTegR2qFIHxVsMgZnj5uXkp4UfU4m6kt0ijYxe9xLGt3KxA7VE32rVvIGvi30MlPNW37jxWcySbnJDu23UbTvdHXp1gifLxpR_N35sJpLrJ4kDc2UcSiz6qanxlNBHyqnvM7in8XZLb31tD39UVqn38QCnQlqSDjJJaAxM6bUMkMoKab0inRXfO5mdgJBYZn-LDSFQHG56skPZg'
user_id = '7788347'
vk = VK(access_token, user_id)
print(vk.photos_profile(5))



