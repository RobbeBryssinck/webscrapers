from bs4 import BeautifulSoup
from google import google
import requests


def get_lyrics(song, artists):
	try:
		num_page = 1
		search_results = google.search(f"site:azlyrics.com {song} {artists}", num_page)
		lyricslink = search_results[0].link
	except Exception as e:
		print("Something went wrong gathering the lyrics.")
		print("Check if you have a working internet connection.")
		return

	source = requests.get(lyricslink).text
	soup = BeautifulSoup(source, 'lxml')

	lyricsdiv = soup.find('div', class_="col-xs-12 col-lg-8 text-center")
	lyrics = lyricsdiv.find('div', class_=None).text

	lyrics_available = does_song_have_lyrics(lyrics)

	if lyrics_available:
		return "Lyrics:\n" + lyrics
	else:
		return "This song doesn't have any lyrics!"


def does_song_have_lyrics(lyrics):
	'''
	AZLyrics.com still has pages up for songs without lyrics.
	These pages list the related album for other songs.
	Therefore, if the scraper finds that the scraped content contains the word
	'album' at in the first 6 characters, the program returns "no lyrics".
	'''

	i = 0
	lyricsbuffer = ""
	while i < 6:
		lyricsbuffer += lyrics[i]
		i += 1
	
	
	if 'album' in lyricsbuffer.lower():
		return False
	else:
		return True


def main():
	print("Lyrics scrapper 1.1")

	print("Song name:")
	song = input('> ')
	print("Artist(s):")
	artists = input('> ')

	lyrics = get_lyrics(song, artists)

	print(lyrics)


if __name__ == '__main__':
	main()
