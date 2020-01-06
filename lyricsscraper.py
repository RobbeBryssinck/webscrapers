from bs4 import BeautifulSoup
from google import google
import requests


def get_lyrics(song, artists):
	num_page = 1
	search_results = google.search(f"site:azlyrics.com {song} {artists}", num_page)
	lyricslink = search_results[0].link

	source = requests.get(lyricslink).text
	soup = BeautifulSoup(source, 'lxml')

	lyricsdiv = soup.find('div', class_="col-xs-12 col-lg-8 text-center")
	lyrics = lyricsdiv.find('div', class_=None).text

	i = 0
	lyricsbuffer = ""
	while i < 6:
		lyricsbuffer += lyrics[i]
		i += 1
	
	# AZLyrics.com still has pages up for songs without lyrics.
	# These pages list the related album for other songs.
	# Therefore, if the scraper finds that the scraped content contains the word
	# 'album' at in the first 6 characters, the program returns "no lyrics".
	if 'album' in lyricsbuffer.lower():
		return "This song doesn't have any lyrics!"

	return "Lyrics:\n" + lyrics


def main():
	print("Lyrics scrapper 1.0")

	print("Song name:")
	song = input('> ')
	print("Artist(s):")
	artists = input('> ')

	lyrics = get_lyrics(song, artists)

	print(lyrics)


if __name__ == '__main__':
	main()
