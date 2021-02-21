# Mat Lockhart
# Python 3.7

import sys

verbose = True

def main():
    file_list = []
    new_file = "combined.csv"
    count = 0

    with open(new_file, 'w') as new_fl:
        for arg in sys.argv:
            if ".csv" in arg:
                count += 1
                with open(arg, 'r') as fl:
                    for i, line in enumerate(fl):
                        line = line.strip()
                        if i == 0 and count == 1:
                            print(f"Player,{line}", file=new_fl)
                        elif i == 0:
                            continue
                        else:
                            print(f"{arg[:-4]},{line}", file=new_fl)

            else:
                if verbose:
                    print(f"Argument {arg} does not appear to be a csv file")



    

main()