#!/usr/bin/env python3
try:
    from termcolor import cprint
    from googlesearch import search
    import os
    import urllib.error as error
    from time import sleep
    from random import randint
    from tqdm import tqdm as tqdm
except ImportError as e:
    print("{}".format(e))


already_queired = []
already_used_file= []
already_found = []


def progress_bar(duration):
    for i in tqdm(range(int(duration))):
        sleep(1)


data_dir = "" # directory where you store your dork lists.
write_dir = "" # directory where you want to write your dork results to.
current_file = ''
os.chdir(data_dir)
while True:
    os.system("clear")
    for file in os.listdir(data_dir):
        if file.endswith('.txt'):
            if file not in already_used_file:
                if file == '':
                    already_used_file.clear()
                    continue
                already_used_file.append(file)
                out_write = write_dir + file.strip('.txt') + "_results_of_dork.dorked"
                with open(file) as search_param:
                    for line in search_param.readlines():
                        if line is None:
                            cprint("Reached EOF, clearing already queried list.", "red", "on_white", attrs=["bold"])
                            already_queired.clear()
                        if line not in already_queired:
                            already_queired.append(line)
                            try:
                                query = str(line.strip('\n'))
                                os.system("clear")
                                cprint(f"Using: {str(file)} for search params.", "green", "on_white", attrs=["bold"])
                                cprint(f"Using: {query} for pull!", "green", "on_white", attrs=["bold"])
                                for j in search(query=line.strip("\n"), num=100, stop=100, pause=5):
                                    with open(out_write, 'a') as out_url:
                                        cprint(f"{j}", "blue", "on_white", attrs=["bold"])
                                        to_write = [str(j), '\n']
                                        out_url.writelines(''.join(to_write))
                                        continue
                            except error.HTTPError as e:
                                already_queired.remove(line)
                                os.system("clear")
                                leng = randint(100, 500)
                                cprint(f"{e}\nSleeping for: {leng} seconds", "red", "on_white",
                                       attrs=["underline", "dark"])
                                cprint(f"\nCurrently working in:\n{file}\n", "blue", attrs=["bold"])
                                cprint(f"\nAlready queried: {already_queired}\n", "green", attrs=["bold"])
                                cprint(f"Currently using: {line} for query.", "blue", attrs=["bold"])
                                progress_bar(leng)
                                continue
