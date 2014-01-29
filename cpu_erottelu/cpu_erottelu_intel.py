#!/usr/bin/env python
#-*- coding:UTF-8 -*-

#rikujjs


if __name__ == "__main__":


    inputfile = open("game-debate_jee.csv", 'r')

    counter = 0
    headers = None

    for line in inputfile:

        if counter == 1:
            headers = line.strip().split(';')
            break
        counter += 1

    index = 0


    counter = 0
    for header in headers:

        #"INTELCPUMODEL"
        #"AMDCPUMODEL"
        if header == "INTELCPU2MODEL":
            index = counter+1
            print index
        counter += 1

    counter = 0
    change_counter = 0
    all_counter = 0
    for line in inputfile:

        if counter < 2:
            counter += 1
            continue

        specs = line.strip().split(';')
        if (specs[index] != '-'):

            all_counter += 1

            tmps = specs[index].split(' ')
            for tmp in tmps:
                if tmp.startswith('E') or (tmp.startswith('Q') and tmp.lower() != 'quad') :
                    print tmp
                    change_counter += 1
            #print specs[index]




    print change_counter, "/", all_counter