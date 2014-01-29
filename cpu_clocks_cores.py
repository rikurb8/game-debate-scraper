#!/usr/bin/env python
#-*- coding:UTF-8 -*-

#rikujjs


#some aftermath operations that had to be done to the data to make it more analysable. separating clocks and cores etc.
#more data editing scripts to come.




column_headers = ["ID", "Title", "EUrelease", "USrelease", "AUrelease", "Genre", "Theme", #6 täs rivillä
                  "INTELCPU1CLK","INTELCPU1CORES","INTELCPU1", "AMDCPU1CLK","AMDCPU1CORE","AMDCPU1", "NVIDIAGPU1","NVIDIAGPU1MEMORY", "AMDGPU1","AMDGPU1MEMORY", "RAM1", "OS1", "DX1", "HDD1",
                  "INTELCPU2CLK","INTELCPU2CORES","INTELCPU2", "AMDCPU2CLK","AMDCPU2CORE","AMDCPU2", "NVIDIAGPU2","NVIDIAGPU2MEMORY", "AMDGPU2","AMDGPU2MEMORY", "RAM2", "OS2", "DX2", "HDD2",
                  "INTELCPU3CLK","INTELCPU3CORES","INTELCPU3", "AMDCPU3CLK","AMDCPU3CORE","AMDCPU3", "NVIDIAGPU3","NVIDIAGPU3MEMORY", "AMDGPU3","AMDGPU3MEMORY", "RAM3", "OS3", "DX3", "HDD3"]

def edit(game):

    return game


if __name__ == "__main__":

    input_f = "game-debate_jee.csv"
    source = open(input_f, 'r')
    destination = open("game-debate_jee2.csv", 'w')

    skip = 0
    column = 13 #10 = intel cpu1, #22 = intel cpu2, #34 = intel cpu3
    counter = 0

    speed = '-'


    for line in source:


        if skip < 2:
            skip += 1
            destination.write(line)
            continue

        game = line.split(';')

        #nvidia1 memory
        if "MB" in game[column]:
            words = game[column].split(" ")
            for word in words:
                if "MB" in word:
                    game[column+1] = word.replace("MB", "").strip()

        #amd1 memory
        if "MB" in game[column+2]:
            words = game[column+2].split(" ")
            for word in words:
                if "MB" in word:
                    game[column+3] = word.replace("MB", "").strip()


        #nvidia2
        if "MB" in game[27]:
            words = game[27].split(" ")
            for word in words:
                if "MB" in word:
                    game[28] = word.replace("MB", "").strip()


        #amd2
        if "MB" in game[29]:
            words = game[29].split(" ")
            for word in words:
                if "MB" in word:
                    game[30] = word.replace("MB", "").strip()



                #nvidia2
        if "MB" in game[41]:
            words = game[41].split(" ")
            for word in words:
                if "MB" in word:
                    game[42] = word.replace("MB", "").strip()

        #amd2
        if "MB" in game[43]:
            words = game[43].split(" ")
            for word in words:
                if "MB" in word:
                    game[44] = word.replace("MB", "").strip()



#------------------- remove possible other platform products
        if "Blackberry" in game[1] and "[PC]" not in game[1]:
            counter += 1
            continue
            print line


#-------------------------------no edits after this line, writing back to file-----------------------------------------
        out_text = ""
        for line in game:
            out_text += ';'
            out_text += line.strip()

        out_text = out_text.replace(";", "", 1)
        out_text += '\n'

        destination.write(out_text)

        speed = '-'

    print counter
