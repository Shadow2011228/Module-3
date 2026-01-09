import  s_taper
from s_taper.consts import *

scheme = {
    "user_id": INT + KEY,
    "name": TEXT,
    "age": INT

}

users = s_taper.Taper('users', 'db.db').create_table(scheme)

user_list = users.read('name', "Муслим")
print(user_list[1])
user_list1 = users.read('name', "Рамазан")
print(user_list1[1])
user_list2 = users.read('name', "Икрам")
print(user_list2[1])
user_list3 = users.read('name', "Мухаммад")
print(user_list3[1])
user_list4 = users.read('name', "Хаким")
print(user_list4[1])