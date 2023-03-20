from collections import deque


class Playlist:
	def __int__(self):
		self.play_queue = deque()
		self.play_history = deque()

	def __len__(self):
		return len(self.play_queue)


class Player:
	pass
