from cortex import Cortex

class LiveAdvance():
	def __init__(self):
		self.c = Cortex(user, debug_mode=True)
		self.c.do_prepare_steps()

	def live(self, profile_name):
		print('begin live mode ----------------------------------')
		self.c.setup_profile(profile_name=profile_name, status='load')
		self.c.sub_request(stream=['com'])

	def get_sensitivity(self, profile_name):
		self.c.get_mental_command_action_sensitivity(profile_name)

	def set_sensitivity(self, profile_name, values):
		self.c.set_mental_command_action_sensitivity(profile_name, values)

# -----------------------------------------------------------
user = {
	"license" : "d5b584b8-883e-421f-8bf5-cbe4bcb0ac72",
	"client_id" : "BN6wnwY8b9ZKYAQmTUCJLHBx0UVQ1VE52QN4I9Ha",
	"client_secret" : "WSdbaAxrMqkNvqRvMYW8ZsLXWNuNb3XJGk4cnxXebQb3A43bl7L21AEvr7aiQqOepIo01K74ixfDSKPb1QBhUPPX9EOewegV4kYZCJceDiGBZFfAKrSN5MIpTQroOhg6",
	"debit" : 100
}

l = LiveAdvance()

profile_name = 'Andrew Paul Mayer'

l.get_sensitivity(profile_name)

values = [7,7,7,7]
l.set_sensitivity(profile_name, values)

l.live(profile_name)
# -----------------------------------------------------------
