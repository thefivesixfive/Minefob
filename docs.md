# Welcome to the Minefob documentation.  
Here you will learn how to use Minefob.

## Initialization
```import Minefob
m = Minefob("foorbar@example.domain", "password", "my_server")
```
Initializing a new Minefob class instance requires 3 arguments:
* Email associated with Minehut account
* Password of the aforementioned account
* and the server name

will return `RunTimeError` if server name is misspelled.

## Post Commands

### Say
```
m.say("Hey there")
```
Will print the desired message to the chat.  Appears like this
`[Server] Hey there`

### Title
```
m.title("Big text", subwords="little text", fadeIn=0, hold=20, fadeOut=0)
```
Will summon a title. 
The big text title is the first argument and the subtitle as the second argument.  Subtitle is not required.
I have a feeling the `fadeIn`, `hold`, and `fadeOut` are self-explanatory,
however you must know that the time is in Minecraft ticks (20 ticks = 1 sec.)

### Kick
```
m.kick("@a", "because i wanted to")
```
Will kick the selected player(s).  Use the second argument to provide a reason, if wanted.

### Command
```
m.command("/give @r minecraft:diamonds 64")
```
Will run the desired command.

### Save
```
m.save()
```
Saves server.

### Awaken
```
m.awaken()
```
Wakes server from hibernation.

### Slumber
```
m.slumber(17)
```
Will kick players, save server, and put it into hibernation AFTER a countdown.
Length of countdown is determined by the only argument passed into this function.
Leave at 0 to skip countdown and shut down instantly.

## Properties
### Players
```
>>> m.players
3
```
Returns the number of active players on the server.

### Online
```
>>> m.online
False
```
Returns whether the server is online or not.

### Status
```
>>> m.status
'SERVER-DOWNLOADING'
```
Returns the current status of the server, basically
a more detailed version of `m.online`

### Started
```
>>> m.started
[09, 34, 55]
```
Returns the time the server was started as a list
in this format: `[HH:MM:SS]`

### Stopped
```
>>> m.stopped
[10, 16, 37]
```
Returns the time the server was stopped as a list
in this format: `[HH:MM:SS]`

