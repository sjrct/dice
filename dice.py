import random, re
from halibot import CommandModule, HalConfigurer

die_re = re.compile("(\d+)[dD](\d+)")

MAX_COUNT = 10
MAX_SIDES = 10000

class DiceModule(CommandModule):

	class Configurer(HalConfigurer):
		def configure(self):
			self.optionInt("max-count", prompt="Max number of dice to roll at once", default=MAX_COUNT)
			self.optionInt("max-sides", prompt="Max number of sides per die", default=MAX_SIDES) 

	def init(self):
		self.commands = { "roll": self.roll_ }

	def _roll(self, roll):
		m = re.match(die_re, roll)

		if not m:
			return self._err()

		count = int(m.group(1))
		sides = int(m.group(2))

		if count == 0:
			return "0"
		if count < 0:
			# This shouldn't actually be possible as the regex doesn't match -
			return "You can't think of a way to roll a dice {} times.".format(count)
		if sides < 1:
			return "You find it difficult to roll a die with {} sides.".format(sides)

		if count > self.config.get("max-count", MAX_COUNT) or sides > self.config.get("max-sides", MAX_SIDES):
			return "No."

		total = 0
		response = ''

		for i in range(0, count):
			x = random.randint(1, sides)
			total += x 
			response += "{}/{}".format(x, sides)

			if i != count - 1:
				response += " + "

		response += " = {}".format(total)

		return response

	def _err(self):
		return "You make a motion as if to roll some dice, but as you open your hands to throw them, only air escapes."

	def roll_(self, string, msg=None):
		args = string.strip().split(" ")

		if len(args) == 0:
			self.reply(msg, body=self._err())
			return

		for r in args:
			response = self._roll(r)
			self.reply(msg, body=response)

