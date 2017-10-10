#!/usr/local/bin/python
""" This autoTv program uses RSS feed to download new TV Series
from torrent sites. It is made for my system at home which includes
a NAS (FreeNAS) that this program should be run on. The FreeNAS also
has the transmission plugin installed for the actual download of
torrents.

For me the mounted TV disk (/mnt/TV) is used by XBMC to stream the
TV Series content. It is also in this folder that autoTv gets the
users 'subscribed' or favourite TV series. autoTv is only focusing
on scene releases meaning that there is a naming convention e.g.
Family.Guy.S11E05.HDTV.x264-LOL where the directory has to be
named "Family.Guy" and the season/episode (S11E05) in order for autoTv
to work."""

import feedparser
import os
import glob
import re
import urllib
import time
import datetime
import sys
import shutil

XBMC_TV_DIR              = "/mnt/TV/"
TRANSMISSION_TORRENT_DIR = "/mnt/Download/torrents/"
LOG_FILE                 = "/mnt/Download/scripts/autoTv/autotv.log"
WEB_SERVER_LOG           = "/usr/local/www/apache22/data/autotv.log"
TORRENT_SITE_RSS        = "insert info here"
SLEEP_TIME               = 60
BANNED                   = ("1080", "WEB", "NUKED")
DL_LIST                  = list()


# Functions
def getSeasonEpisode(filename):
	""" Regular expression to retrive Season + Episode from a release name. """
	return re.findall(r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})",
					  filename, re.I)
	
def isEpisodeThere(season_dir, season, episode):
	""" Checks a complete season directory of a specific TV Series if an episode
	exists. Returns boolean of the result. """
	episodes = glob.glob(season_dir+"/*")
	#print "EPISODES: " ,episodes
	#print episodes
	for this_episode in episodes:
		episode_match = getSeasonEpisode(this_episode)
		#print this_episode
		#print episode_match
		if season == episode_match[0][0] and episode == episode_match[0][1]:
			return True
	return False

def removeEpisodeFromDownloadList(tv_series, season, episode):
	""" Checks if a TV Series season and episode exists in the Download list,
	if it exists it is removed from the list, if not, nothing is done."""
	for ep_dict in DL_LIST:
		if isEpisodeInDownloadList(tv_series, season, episode):
			print tv_series + " " + "S"+season+"E"+episode+ " is Removed from list!"
			writeToLogFile(tv_series + " " + "S"+season+"E"+episode+ " is Removed from list!")
			DL_LIST.remove(ep_dict)

def addEpisodeToDownloadList(tv_series, torrent_name, season, episode):
	""" Checks if a TV Series season and episode exists in the Download list,
	if not, then it is added to the list. If it exists nothing is done. """
	for ep_dict in DL_LIST:
		if isEpisodeInDownloadList(tv_series, season, episode):
			return False
	print tv_series + " " + "S"+season+"E"+episode+ " is Added to the list!"
	writeToLogFile(tv_series + " " + "S"+season+"E"+episode+ " is Added to the list!")
	episode_dict = {'Torrent_Name': torrent_name, 'Series_Name': tv_series, 'Season': season, 'Episode': episode}
	DL_LIST.append(episode_dict)
	return True

def isEpisodeInDownloadList(tv_series, season, episode):
	""" Checks if a specific TV Series season and its episode exists
	in the Download list. Returns a boolean """
	for ep_dict in DL_LIST:
		if ep_dict['Series_Name'] == tv_series and ep_dict['Season'] == season and ep_dict['Episode'] == episode:
			#print tv_series + " " + "S"+season+"E"+episode+ " already added to list!"
			return True
	return False

def writeToLogFile(content):
	""" Writes content into a logfile for path defined in LOG_FILE
	It also copies this logfile to the webserver's path as defined in
	WEB_SERVER_LOGS """
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	fo = open(LOG_FILE, "a")
	fo.write( now + ": " + content + "\n" );
	# Close opened file
	fo.close()
	shutil.copyfile(LOG_FILE, WEB_SERVER_LOG)


while True:
	tv_dirs = glob.glob(XBMC_TV_DIR+"*")
	d2 = feedparser.parse(TORRENT_SITE_RSS)
	for dir in tv_dirs:
		for item in d2.entries:
			if any(s in item.title.upper() for s in BANNED):
				continue
			#print 'Title: '+item.title
			if item.title.startswith( dir.replace(XBMC_TV_DIR,"") ):
				season_episode = getSeasonEpisode(item.title)
				season  = str( season_episode[0][0] )
				episode = str( season_episode[0][1] )
				print "============================================================================"
				print "Title:   " + item.title
				#print "Season:  " + season
				#print "Episode: " + episode
				if os.path.isdir(dir+"/Season."+season) :
					print "Season exists!"					
					if isEpisodeThere(dir+"/Season."+season, season, episode):
						print "Episode exists!"
						removeEpisodeFromDownloadList(dir.replace(XBMC_TV_DIR,""), season, episode)
						continue
					else:
						print "Check if its being downloaded"
						if isEpisodeInDownloadList(dir.replace(XBMC_TV_DIR,""), season, episode):
							continue
						else:
							print "Download: " + item.title
							writeToLogFile("Download: " + item.title)
							url = item.link
							print url
							urllib.urlretrieve (url, TRANSMISSION_TORRENT_DIR+item.title+".torrent")
				else:
					print "Download: " + item.title
					writeToLogFile("Download: " + item.title)
					url = item.link
					urllib.urlretrieve (url, TRANSMISSION_TORRENT_DIR+item.title+".torrent")
				addEpisodeToDownloadList(dir.replace(XBMC_TV_DIR,""), str(item.title), season, episode)

	print "===DL LIST========"
	print DL_LIST
	print "==================\n"
	time.sleep(SLEEP_TIME)


