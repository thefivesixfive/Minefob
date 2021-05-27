# Minefob
# by Caleb North a.k.a fivesixfive

# Imports
from requests import get, post
from json import loads
from time import sleep, time
from datetime import datetime as dt

# Minefob
class Minefob:

	#region Internal Junk.  Leave it alone.
	# Initalization
	def __init__(self, email:str, password:str, server:str):
		"""Initalization for a Minefob class instance.  Requires Minehut
		account email and password along with desired server for initalization."""
		# Convert Server Name to Server ID
		req = get(f"https://api.minehut.com/server/{server}?byName=true")
		if req.status_code != 200: # If not oki-doki
			raise RuntimeError("Unable to find server by that name.  Could it be misspelled?")
		else: # if oki doki
			servId = loads(req.text)["server"]["_id"]

		# Important Constants
		self.MAIL = email
		self.PASS = password
		self.HOST = "https://api.minehut.com"
		self.AUTH = self.HOST + "/users/login"
		self.SERV = self.HOST + "/server/" + servId

		# Important Vars
		self.lastAuth = 0
		self.auth = None

	# Auth
	def _auth(self): #
		"""Internal command.  Authorizes email and password combo"""
		# IF if has been a while since last authenification
		thisAuth = time()
		if thisAuth - self.lastAuth > 60:
			self.lastAuth = time()
			# Establish Combo
			combo = {"email":self.MAIL, "password":self.PASS}
			# Try to login
			req = post(self.AUTH, data=combo)
			# Handle Errors
			if req.status_code != 200:
				raise RuntimeError("Credentials could not be validated.")
			else:
				# Parse response to hash out important crap.
				reqText = loads(req.text) # Convert str to dict
				reAuth = {"x-session-id":reqText["sessionId"], "Authorization":reqText["token"]} # Create heads
				self.auth = reAuth # Set class var
				return reAuth
		# Otherwise
		else:
			return self.auth
		# By adding code to return the old auth most of the time, it will speed
		# up the process, espesially for things like the countdown that would normally
		# call the auth func multiple times in a sequence

	# Interal
	def _getStat(self):
		# Get token
		heads = self._auth()
		# Get return info
		req = get(self.SERV+"/status", headers=heads)
		rDict = loads(req.text)["status"]

		return rDict

	# Testing for whatever
	def _test(self):
		# Get token
		heads = self._auth()
		print(loads(get(self.SERV+"/status", headers=heads).text)["status"]["status"])
	#endregion

	#region Anything using POST
	# Send a message to chat
	def say(self, words:str):
		"""Speaks something to the chat. Takes a string as the argument."""
		# Get token
		heads = self._auth()
		# Say
		combo = {"command":f"/say {words}"}
		post(self.SERV+"/send_command", data=combo, headers=heads)

		return True

	# Trigger a title command
	def title(self, words:str, subwords:str="", fadeIn:int=0, hold:int=20, fadeOut:int=0):
		"""Triggers a title and optional subtitle.  Includes
		fadeIn, hold, and fadeOut variables."""
		# Get token
		heads = self._auth()
		# Establish Times
		combo = {"command":f"/title @a times {fadeIn} {hold} {fadeOut}"}
		post(self.SERV+"/send_command", data=combo, headers=heads)
		# Create Subtitle
		combo = {"command":f"/title @a subtitle \"{subwords}\""}
		post(self.SERV+"/send_command", data=combo, headers=heads)
		# Announce title
		combo = {"command":f"/title @a title \"{words}\""}
		post(self.SERV+"/send_command", data=combo, headers=heads)

		return True

	# Kick
	def kick(self, target:str="@r", reason:str="Kicked by server."):
		"""Kicks player(s) Accepts usernames and Minecraft target selectors.
		Default is @r.  Also has reason argument, which displays when kicked."""
		# Get token
		heads = self._auth()
		# Kick
		combo = {"command":f"/kick {target} {reason}"}
		post(self.SERV+"/send_command", data=combo, headers=heads)

		return True

	# General Command Function
	def command(self, command:str):
		"""Pass a Minecraft command into the command argument to run it.
		If command fails, no error message is returned."""
		# Get token
		heads = self._auth()
		# Run command
		combo = {"command":command}
		post(self.SERV+"/send_command", data=combo, headers=heads)

		return True

	# Save
	def save(self):
		"""Saves the server, instantly."""
		# Get Token
		heads = self._auth()
		post(self.SERV + "/save", headers=heads)

		return True

	# Start Server
	def awaken(self):
		"""Wakes up the server from hibernation"""
		# Get Token, pass it on to starting command
		heads = self._auth()
		post(self.SERV + "/start_service", headers=heads)

		return True

	# Hibernate Server
	def slumber(self, countdown:int=10):
		"""Stops the server after a countdown.  Leave countdown at 0 to instantly stop
		the server and put it into hibernation."""
		# Get token
		heads = self._auth()
		# Check to see if countdown is valid
		if countdown < 0:
			raise ValueError("Number must be positive.")
		# Countdown if not 0
		if countdown != 0:
			self.say(f"Shutting down in {countdown} second(s)!  Please leave the server or you will be kicked.")
			for _ in range(countdown, 0, -1):
				self.say(f"§c§l{_} seconds left.") # Announce
				sleep(1) # Wait

		# After that
		#self.kick("@a", "Server has been shut down.") # Kick players
		#self.save() # Save Server
		#post(self.SERV+"/destroy_service", headers=heads) # Shut down

		return True
	#endregion

	# region Anything using GET (usually properties)
	# Return player count
	@property
	def players(self):
		"""Returns int"""
		return self._getStat()["player_count"]

	# Return online or not
	@property
	def online(self):
		"""Returns bool"""
		return self._getStat()["service_online"]

	# Return server status as string (Starting, stopping, etc)
	@property
	def status(self):
		"""Returns string displaying server status"""
		return self._getStat()["status"]

	# Returns time server was started
	@property
	def started(self):
		"""Returns the time [hh, mm, ss] the server was started.
		Returns False is server is offline."""
		if self.online:
			properFormat = self._getStat()["started_at"] / 1e3 # Convert raw int time to proper int format
			rData = dt.fromtimestamp(properFormat).strftime("%I:%M:%S") # Get HOURS, MINUTES, SECONDS
			return str(rData).split(":") # Turn into list
		else:
			return False

	# Returns time server was stopped
	@property
	def stopped(self):
		"""Returns the time [hh, mm, ss] the server was stopped.
		Returns False if unable if something goes wrong."""
		if not self.online:
			return False
		else:
			properFormat = self._getStat()["stopped_at"] / 1e3
			rData = dt.fromtimestamp(properFormat).strftime("%I:%M:%S")
			return str(rData).split(":")
	#endregion