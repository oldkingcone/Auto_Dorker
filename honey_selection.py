import random
import sqlite3
from tqdm import tqdm
from time import sleep
from termcolor import cprint
from urllib3 import PoolManager
from urllib3 import exceptions
from bs4 import BeautifulSoup
import re
import os

sql_stmt = '''CREATE TABLE IF NOT EXISTS dork_bin(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, full_url TEXT, honey_pot TEXT, is_alive TEXT, cms TEXT, shodan_url TEXT, pot_or_not_url TEXT, type_query TEXT, no_touch INTEGER)'''
insert = "INSERT INTO dork_bin(full_url, honey_pot) VALUES (?, ?)"
alive_check = 'UPDATE dork_bin SET is_alive = ? WHERE full_url = ?'
honeypot = []
in_db = []
processed = []
already_crawled = []
c = sqlite3.connect("./dork_bin.sqlite")
x = c.cursor()
x.execute(sql_stmt)
select = x.execute("SELECT full_url FROM dork_bin WHERE honey_pot LIKE 'True' AND is_alive IS NULL")
c.commit()
data_path = ''
fin_dir = ''
header = {'User-Agent': "honey-bot-1.0 AKA HoneyBee"}


def progress_bar(duration):
	for i in tqdm(range(int(duration))):
		sleep(1)
		continue

def crawl_for_honey(url):
	try:
		print(f'\nStarting crawl on {url}\n')
		to_search = ['div', '---', '!', 'h1']
		req = PoolManager(num_pools=5)
		http = req.urlopen('GET', url, timeout=10, headers=header)
		soup = BeautifulSoup(http.data, "html.parser")
		for item in to_search:
			print(f'Selecting: {item}')
			for item in soup.findAll(item):
				cprint(f"{item}", "blue", "on_white", attrs=["bold"])
			x.execute(alive_check, ('Alive', url))
			c.commit()
		http.close()
	except (exceptions.ConnectionError, exceptions.ConnectTimeoutError,exceptions.MaxRetryError,
	        exceptions.ReadTimeoutError, timeout) as e:
		cprint(f"\n{e}", "red", "on_white", attrs=["bold", "underline", "dark"])
		cprint(f"\nAppears to be a dead url: {url}", "red", "on_white", attrs=["bold", "underline", "dark"])
		x.execute(alive_check, ('Dead', url))
		c.commit()
		pass


def open_file(files):
	with open(files) as to_read:
		for line in to_read.readlines():
			if line not in in_db:
				if find_honeys(lines=line):
					in_db.append(line)
					x.execute(insert, (line.strip('\n'), "True"))
				else:
					in_db.append(line)
					x.execute(insert, (line.strip('\n'), "False"))


def find_honeys(lines):
	honey_pot = re.findall(
		r'(http|ftp|https)\:\/\/(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\/?',
		lines)
	for lines in honey_pot:
		honeypot.append(lines)
	if lines in honey_pot:
		return True
	else:
		return False


def main():
	init_mtime = os.stat(data_path).st_mtime
	while True:
		now_mtime = os.stat(data_path).st_mtime
		if init_mtime != now_mtime:
			for file in os.listdir(data_path):
				if file.endswith(".dorked"):
					cprint(f'Found: {file}!', "blue", "on_white", attrs=['bold','dark'])
					open_file(file)
					os.system(f'mv {file} {fin_dir}')
		for row in select.fetchall():
			if row not in already_crawled:
				if row == '':
					continue
				else:
					already_crawled.append(row)
					crawl_for_honey(row[0])
		length = random.randint(5, 10)
		progress_bar(length)


if __name__ == "__main__":
	os.chdir(data_path)
	main()
