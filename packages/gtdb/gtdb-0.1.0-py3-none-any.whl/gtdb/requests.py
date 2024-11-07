from gtdb.database import Gtdb

import json

class Request:
	def __init__(self, db_name: str):
		self.db_name = db_name
		
	def load_data(self) -> dict:
		"""
		Загружает данных из JSON-файла.
		"""
		try:
			with open(self.db_name, "r") as file:
				return json.load(file)
		except FileNotFoundError:
			return {}
	
	def save_data(self, data: dict) -> None:
		"""
		Сохроняет данные в JSON-файл.
		"""
		with open(self.db_name, "w") as file:
			json.dump(data, file, indent=4)
	
	def get(self) -> dict:
		"""
		Функция которая возвращает данные из JSON-файл.
		
		Returns:
			dict: Данные из json-файла.
		"""
		return self.load_data()		
	
	def update(self, update_data: dict, id_key: str = None) -> None:
		"""
		Функция для обновления данных.
		
		Parameters:
			update_data (dict): Новый данные.
			id_key (str): Обновлять по идентификаторо.
		"""
		data = self.load_data()
		if id_key is None:
			data.update(update_data)
			self.save_data(data)
			return
		if id_key in data:
			data[id_key].update(update_data)
			self.save_data(data)
		else:
			print(f"[{self.db_name}] Идентификатор {id_key} не найден.")