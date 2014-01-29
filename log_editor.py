

if __name__ == "__main__":

    input_file = open("log.txt", "r")
    output = open("log_final.txt", "w")


    for line in input_file:
        if "ID:" in line:
            continue
        else:
            output.write(line)
