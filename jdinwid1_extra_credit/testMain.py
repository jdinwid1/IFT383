#!/usr/bin/python
import sqlite3
####################################################################
#
# This script is to test the main script, script.py.  I included
# this purely for convience to test out every title in the database.
#
####################################################################


# Create Parent class Song to store main song information given from
# the tracks table in the database model.
class Song:
	# Define instance variables as protected
	__name = ""
	__composer = ""
	__price = 0
	__genre = ""
	__album = ""

	# Call constructor to instantiate variables.
	def __init__(self, name, composer, price, genre, album):
        	self.__name = name
        	self.__composer = composer
		self.__price = price
		self.__genre = genre
		self.__album = album
	# Call accessor to return protected variable album id.
	def get_album_id(self):
		return self.__album
	# Call accessor to return protected variable price.
	def get_price(self):
		return self.__price
	# Call accessor to return protected variable name of the song.
	def get_name(self):
		return self.__name
	# Call accessor to return protected variable genre of the song.
	def get_genre_id(self):
		return self.__genre
	# Call accessor to return protected variable composer of the song.
	def get_composer(self):
		return self.__composer

# Define class to handle the album table from the database model. Inherits from
# Song class.
class Album(Song):
	# Define variable instance as private.
	_title = ""

	# Constructor to instatiate inherited and class defined variables.
	def __init__(self, title, name, composer, price, genre, album):
		self._title = title
		self.__name = name
		self.__composer = composer
		self.__price = price
		self.__genre = genre
		self.__album = album

	# Accessor to return private title of the album.
	def get_title(self):
		return self._title
# Create genre class to handle the Genre table of the database.  Inherits from
# Song class.
class Genre(Song):
	# Define private instance variable genre name.
        _genre_name = ""

	# Constructor to instantiate inherited variables and title from this
	# this class.
        def __init__(self, genre_name, name, composer, price, genre, album):
                self._genre_name = genre_name
                self.__name = name
                self.__composer = composer
                self.__price = price
                self.__genre = genre
                self.__album = album
	# Call accessor to return the private genre name of the song.
        def get_genre(self):
                return self._genre_name

# Main program function.
def main():
	print("Welcome to the song information portal!")
	# Start while loop defined as false until the user is done, then
	# break_loop will be true.
	break_loop = False
	while not break_loop:
		# Display Menu
		print("\nEnter a number for the corrisponding option below:\n\nMenu:\n")
		print("1. Test Function")
		print("2. Quit\n")
		# Accept User input to determine what to do next.
		option = input()
		if option == 1:
			# If the second option is chosen, all the song titles
			# will be listed using the list_songs function.
			list_songs()
			yes_or_no = raw_input("\nWould you like to continue?(y/n)")
                        # User can break loop if they do not want to continue.
			if (yes_or_no.upper() == 'N'):
                                break_loop = True
		elif option == 2:
			# Option 2 will close the program.
			break_loop = True
		else:
			# Validation for wrong number.
			print("Please enter a number between 1-2")
# Define function that lists all the titles of the songs.
def list_songs():
        # Database connection setup code from: https://docs.python.org/2/library/sqlite3.html
        # Database file from: https://www.sqlitetutorial.net/sqlite-sample-database/
        # Connect to database file.
	conn = sqlite3.connect('media.db')
        # This function allows you to do various tasks inside the connection.
	c = conn.cursor()
	# Execute query inside database file.
        tracks_table = c.execute("SELECT * from tracks")
	# For loop to display data retrieved from database.
        for item in tracks_table:
                get_song_info(item[1])
# Define function to return song information.
def get_song_info(search_song):
	# Accept user input for song title.  Is case sensative and must be word
	# for word.
	# Database connection setup code from: https://docs.python.org/2/library/sqlite3.html
	# Database file from: https://www.sqlitetutorial.net/sqlite-sample-database/
	# Connect to database file.
	conn = sqlite3.connect('media.db')
	# This function allows you to do various tasks inside the connection.
	c = conn.cursor()
	# Execute query inside database table to find the name of the song
	# user requested.
	tracks_table = c.execute("SELECT * from tracks WHERE name = ?", (search_song,))
	# Define song_name variable as None in case title doesn't exist.
	song_name = None
	for item in tracks_table:
		# If song_name exists, assign the name of the song to the
		# song_name value.
		song_name = item[1]
		# Create Song object using data from database.
		song_info = Song(item[1], item[5], item[8], item[4], item[2])
	# If song name has no value, program prints that the song doesn't exist
	# in the database.
	if song_name != None:
		# If the title does exist, query the album table using albumid
		# for the album title.
		album_table = c.execute("SELECT * from albums WHERE Albumid = " + str(song_info.get_album_id()))
		# Loop through returned data from the database.
		for album in album_table:
			# Create Album object using returned data from
			# from the database.
			album_info = Album(album[1], song_info.get_name(), song_info.get_composer(), song_info.get_price(), song_info.get_genre_id, song_info.get_album_id)
		# Query genre table using genre id from song object.
		genre_table = c.execute("SELECT * from genres WHERE Genreid = " + str(song_info.get_genre_id()))
                # Loop through data returned from database.
		for genre in genre_table:
			# Create Genre object from returned database data.
                        genre_info = Genre(genre[1], song_info.get_name(), song_info.get_composer(), song_info.get_price(), song_info.get_genre_id, song_info.get_album_id)

		# Print results:
		print("\n\nTitle:\t\t" + song_info.get_name().encode('utf-8'))
		# Print None values or special non ASCII characters.
		if (song_info.get_composer() != None):
                        print("Composer:\t" + song_info.get_composer().encode('utf-8'))
                else:
                        print("Composer: \t" + str(song_info.get_composer()))
		print("Retail Price:\t${0:.2f}".format(song_info.get_price()))
		print("Genre:\t\t" + str(genre_info.get_genre()))
		print("Album:\t\t" + album_info.get_title().encode('utf-8'))
	else:
		print("Song not in list")
	# Close the connection to the database file.
	conn.close()

# Tell script to start on main() function.
if __name__ == "__main__":
    main()
