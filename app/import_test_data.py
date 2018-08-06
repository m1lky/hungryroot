from models import pets, users
import sqlite3
import os
import random as rand
import bcrypt
def init_pets():
	pets_table = pets()
	images_count = 0

	names = ["barky", "pupper", "doggo", "dorito", "girl", "boy"]
	breeds = ["calico", "poodle", "tabby", "mutt"]
	species = ["cat", "rat", "dog"]
	ages = [1, 2, 3, 4, 5, 6]
	prices = [149.00, 99.99, 50.99, 75.00, 0]
	pictures = []
	for path, subdirs, files in os.walk('app/static/images'):
		for name in files:
			pictures.append(name)
			images_count += 1

	test_data = [names, pictures, species, breeds, ages, prices]
	for x in range(images_count):
		test_pet = []
		for test_vals in test_data:
			test_pet.append( test_vals[ rand.randint(0, len(test_vals) - 1) ])
		pets_table.insert(test_pet)

def init_users():
	users_table = users()
	fnames = ["Jill", "Jack", "Bob", "John"]
	lnames = ["Batman", "Robin", "Brown", "Something'Clever"]
	emails = ["asdf@gmail.com", "fdasdf@yahoo.com", "fdgsasfgdf@hotmail.com", "gadfgsdfg@aol.com"]
	address1s = ["12 hotdog ln", "44 basic road", "32 east 2nd st"]
	address2s = ["apartment 2", "apartment 3", "apartment 4"]
	cities = ["new york city", "boston", "atlanta", "portland"]
	states = ["new york", "massachussetts", "georgia", "oregon"]
	phones = ["999-999-9999", "222-222-2222", "333-333-3333", "444-444-4444"]
	passwords = ['1234', 'qwer', 'asdf', 'zxcv']
	passwords = [bcrypt.hashpw(x.encode('utf-8'), bcrypt.gensalt()) for x in passwords]
	test_data = [fnames, lnames, emails, address1s, address2s, cities, states, phones, passwords]
	for x in range(25):
		test_user = []
		for test_vals in test_data:
			test_user.append( test_vals[ rand.randint(0, len(test_vals) - 1) ])
		users_table.insert(test_user)
init_users()
init_pets()

