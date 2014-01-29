__author__ = 'r'


if __name__ == "__main__":


    source = open("game-debate-17-01-2014.csv", 'r')

    output = open("game-debate-all.csv", 'w')

    counter = 0

    for line in source:


        columns = line.strip().split(';')






        info_string = ""

        for header in columns:

            info_string += ';'
            if header.startswith("-") and header != "-":
                info_string += header.lstrip("-Release Period:")
            else:
                info_string += header
        #get rid of the first ;
        info_string = info_string.replace(";", "", 1)





        output.write(info_string)
        output.write('\n')


    print counter