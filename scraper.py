#!/usr/bin/env python
#-*- coding:UTF-8 -*-

#rikujjs


from bs4 import BeautifulSoup
import requests
from time import sleep

#column_headers array contains the names for the columns.
column_headers = ["ID", "Title", "EUrelease", "USrelease", "AUrelease", "OTHERrelease", "Genre", "Theme",
                  "INTELCPU1", "AMDCPU1", "NVIDIAGPU1", "AMDGPU1", "RAM1", "OS1", "DX1", "HDD1",
                  "INTELCPU2", "AMDCPU2", "NVIDIAGPU2", "AMDGPU2", "RAM2", "OS2", "DX2", "HDD2",
                  "INTELCPU3", "AMDCPU3", "NVIDIAGPU3", "AMDGPU3", "RAM3", "OS3", "DX3", "HDD3"]

spec_header = ["INTELCPU", "AMDCPU", "NVIDIAGPU", "AMDGPU", "RAM", "OS", "DX", "HDD"]


class Scraper:

    #make the parsed soup in to a variable called "soup"
    def __init__(self, url):

        self.url = url
        game_id = url.rsplit("=", 1)
        self.id = int(game_id[1])

        #initialize the datastorage[] dict
        for header in column_headers:
            self.datastorage[header] = '-'


        #store the id
        self.datastorage["ID"] = str(self.id)
        #include possible spoofed header, and get the page
        header = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=header)

        #make some soup
        self.soup = BeautifulSoup(r.text.encode('utf-8', 'ignore'))

    #we go thru the datastorage[] dict and write the info to a string, separated with ';'
    def info_to_string(self):

        info_string = ""

        #write the columns to a single string, place a ';' in between
        for header in column_headers:

            info_string += ';'
            info_string += self.datastorage[header].strip().encode('utf-8', 'ignore').replace(";", '')


        #get rid of the first ;
        info_string = info_string.replace(";", "", 1)

        return info_string

    def format_date(self, unformatted):

        #Mar-26-2010 eg. -> 26-03-2010
        months_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

        if unformatted.count('-') != 2 :
            return unformatted

        rel_date = unformatted.split('-')

        for month in months_dict:
            if month == rel_date[0]:
                formatted = ""
                formatted += rel_date[1]
                formatted += '-'
                formatted += str( months_dict[month] )
                formatted += '-'
                formatted += rel_date[2]

                return formatted




    def get_rel_dates(self):

        info_wrapper = self.soup.find("div", "g_wrapper")
        dates = info_wrapper.find("div", "gdate")
        titles = dates.findAll("div", "gdateTitle")
        datedatas = dates.findAll("div", "gdateData")

        counter = 0
        for title in titles:

            if "EU" in title.text:
                self.datastorage["EUrelease"] = self.format_date( datedatas[counter].text.strip() )
                if datedatas[counter].text.strip() == "":
                     self.datastorage["EUrelease"] = '-'

            elif "US" in title.text:
                self.datastorage["USrelease"] = self.format_date( datedatas[counter].text.strip() )
                if datedatas[counter].text.strip() == "":
                     self.datastorage["USrelease"] = '-'
            elif "AU" in title.text:
                self.datastorage["AUrelease"] = self.format_date( datedatas[counter].text.strip() )
                if datedatas[counter].text.strip() == "":
                     self.datastorage["AUrelease"] = '-'
            elif title.text.strip() != "":
                #this is just for testing. we store the year in USRelease, and the actual title in EURelease
                self.datastorage["OTHERrelease"] += self.format_date( title.text.strip() )
                self.datastorage["OTHERrelease"] += self.format_date( datedatas[counter].text.strip() )

            counter += 1


    def get_genre_theme(self):

        info_wrapper = self.soup.find("div", "g_wrapper")
        genre_divs = info_wrapper.findAll("div", "genre")

        try:
            self.datastorage["Genre"] = genre_divs[0].text.replace("Genre", "").strip()
        except AttributeError:
            #attribute errors are ok, there is the default value "-" already there
            pass

        try:
            self.datastorage["Theme"] = genre_divs[1].text.replace("Theme", "").strip()
        except AttributeError:
            pass



    def read_column(self, req_column):

        #we read the column title first to know what requirements we are dealing with (minimum, recommended, gd adj.)
        req_type = req_column.find("div", "systemRequirementsTitle")
        req_number = 0
        if "Minimum" in req_type.text:
            req_number = 1
        elif "Recommended" in req_type.text:
            req_number = 2
        elif "GD Adjusted" in req_type.text:
            req_number = 3
        else:
            print self.url


        rows = req_column.findAll("div", recursive=False)

        row_counter = 0
        for row in rows:

            #skip the first row (title row)
            if row_counter == 0:
                row_counter += 1
                continue


            #read the cpus
            if row_counter == 1:

                try:
                    top = row.find("div", "systemRequirementsLinkSubTop")
                    top = top.find('a').text
                    self.datastorage["INTELCPU"+str(req_number)] = top.strip()
                except AttributeError:
                    #not all have to top and bottom parts
                    pass
                try:
                    bottom = row.find("div", "systemRequirementsLinkSubBtm")
                    bottom = bottom.find('a').text
                    self.datastorage["AMDCPU"+str(req_number)] = bottom.strip()
                except AttributeError:
                    pass

            #gpus
            elif row_counter == 2:

                try:
                    top = row.find("div", "systemRequirementsLinkSubTop")
                    top = top.find('a').text
                    self.datastorage["NVIDIAGPU"+str(req_number)] = top.strip()

                except AttributeError:

                    #not all have to top and bottom parts
                    pass
                try:
                    bottom = row.find("div", "systemRequirementsLinkSubBtm")
                    bottom = bottom.find('a').text
                    self.datastorage["AMDGPU"+str(req_number)] = bottom.strip()
                except:
                    pass

            #ram
            elif row_counter == 3:



                try:
                    spec = row.find("div", "systemRequirementsRamContent")
                    spec = spec.find('span').text
                    self.datastorage["RAM"+str(req_number)] = spec.strip()
                except AttributeError:
                    #print spec.text
                    #print self.id
                    pass

            #os
            elif row_counter == 4:

                try:
                    spec = row.find("span").text
                    self.datastorage["OS"+str(req_number)] = spec.strip()

                except AttributeError:
                    pass

            elif row_counter == 5:

                try:
                    spec = row.find("span").text
                    self.datastorage["DX"+str(req_number)] = spec.strip()

                except AttributeError:
                    pass

            elif row_counter == 6:

                try:
                    spec = row.find("span").text
                    self.datastorage["HDD"+str(req_number)] = spec.strip()

                except AttributeError:
                    pass

            row_counter += 1





    def get_requirements(self):

        count = 0

        spec_box = self.soup.find("div", id="systemRequirementsOuterBox")

        #no specs found, lets go away
        if spec_box == None:
            return


        #check if the rows have the same title allways
        row_titles = spec_box.find("div", id="systemRequirementsSubheadWrap")
        row_title_count = row_titles.findAll("div", recursive=False)


        #since there was a OuterBox, we have atleast some sp
        req_columns = spec_box.findAll("div", "systemRequirementsWrapBox gameSystemRequirementsWrapBox")



        for req_column in req_columns:

            self.read_column(req_column)





    #do the actual scraping
    def get_pageinfo(self):

        #do the actual scraping here
        soup = self.soup

        #Title
        try:
            self.datastorage["Title"] = soup.find("div", id="art_g_title").text
        except AttributeError:
            print self.url
            return None

        #release dates
        self.get_rel_dates()

        #genre and theme
        self.get_genre_theme()

        #now the actual specs
        self.get_requirements()

        #after all the info is in the datastorage[] dictionary, we write it to a single string and return
        return self.info_to_string()

    #member variables
    soup = None
    datastorage = {}
    url = ""
    id = 0


if __name__ == "__main__":

    #insert the base of the url's we're going to scare
    baseurl = "http://www.game-debate.com/games/index.php?g_id="

    #modifie the starting id if you need the restart the program from a different location. eg. after a crash
    starting_id = 4

    #the file we are gonna write the gotten info, the file has the starting_id in it, in case starting
    #from somewhere else than the begining.
    output_file = "game-debate_starting_from{0}.csv".format(str(starting_id))
    output = open(output_file, 'w')

    #write the column header line in to the file if we are starting from the beggining
    #(starting_id = 4)
    if starting_id == 4:
        header_string = ""
        for header in column_headers:
            header_string += ';'
            header_string += header

        #get rid of the first ;
        header_string = header_string.replace(";", "", 1)

        output.write(header_string)
        output.write("\n")

    #loop the games from starting_id to end.
    for i in range(starting_id, 7350):

        #get the page, BS it, and get the pageinfo
        page_to_get = Scraper(baseurl+str(starting_id))
        page_info = page_to_get.get_pageinfo()

        #if we didnt get anything back (no info etc), we skip the writing
        if page_info == None:
            starting_id += 1
            continue

        #write the info to a outputfile
        output.write(page_info)
        output.write("\n")

        #be nice, the longer the better
        sleep(1)
        starting_id += 1










