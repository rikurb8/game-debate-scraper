#!/usr/bin/env python
#-*- coding:UTF-8 -*-

#rikujjs


from bs4 import BeautifulSoup
import requests
from time import sleep


class Scraper:

    #make the parsed soup in to a variable called "soup"
    def __init__(self, url):

        #include possible spoofed header, and get the page
        header = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=header)

        #make some soup
        self.soup = BeautifulSoup(r.text.encode('utf-8', 'ignore'))







    #member variables
    soup = None



if __name__ == "__main__":

    #insert the base of the url's we're going to scare
    baseurl = "http://www.game-debate.com/games/index.php?g_id="

    #modifie the starting id if you need the restart the program from a different location. eg. after a crash
    starting_id = '4'

    #the file we are gonna write the gotten info, the file has the starting_id in it, in case starting
    #from somewhere else than the begining.
    output_file = "game-debate_starting_from{0}.csv".format(starting_id)
    output = open(output_file, 'w')

    #loop the games from starting_id to end.
    for i in range(Number(starting_id), 7350)

        #get the page, BS it, and get the pageinfo
        page_to_get = Scraper(baseurl+starting_id)
        page_info = page_to_get.get_pageinfo()

        #write the info to a outputfile
        output.write(page_info)
        output.write("\n")

        #be nice
        sleep(1)











