#! /usr/bin/python
import acquisition, ctypes, hand, sdl2, utils


# Handle eventual events and return True if the application needs to continue running
def handleEvent(event, data):
	while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
		if event.type == sdl2.SDL_QUIT:
			return False
			break
		elif event.type == sdl2.SDL_KEYDOWN:
			return keyboard(event, data)
	return True

# Handle all keyboard events
def keyboard(event, data):
	if event.key.keysym.sym == sdl2.SDLK_ESCAPE :
		return False
	elif event.key.keysym.sym == sdl2.SDLK_RETURN :
		# Record the current set of data
		record(data)
	return True

# Record a set of data
def record(data):
	# Write the json encoded version to a file
	utils.dumpJsonToFile(data.to_JSON(), "../dataset/test2.json")
	print "Dataset recorded"