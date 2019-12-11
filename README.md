# Auto_Dorker
Pure python based google auto dorker, it works dynamically(meaning that you can drop a new file holding the dorks into the directory and the program will add it to the into the rotation of files to be used, in the event you want to seperate the dorks between category.)

## Honey pot linting
Is done through honey_bot, this assumes that any "website" that does not have a FQDN(fully qualified domain name) is a honey pot, calculated through a regex. Once the honey pot has been identified, it is then saved in the database with a true or false value. The crawler then tries to crawl the suspected honey pot looking for specific tags (that can be specified by the user) to test whether or not the honeypot is alive or not. Decision tree for that, is attempt to open the supplied URL, if there is a `timeout error`, `maxretries error`, or an error based upon the connection, the url is then marked as dead and can be tested further to see if it is alive or not later.

- In order to get the full effect of this script, you need to run both scripts seperately.

## Install

`pip3 install -r requirements.txt`

---


## Up coming features.
~~I will be adding in a regex to detect and eliminate honeypots from entering the results.~~
  - Thank you murph.
  ---
  
  If you have seen this User Agent in your logs:
 
 `User Agent: HoneyBot-1.0(https://github.com/oldkingcone/Auto_Dorker)/I am doing research this is not malicious.` 
 
 And are wondering how I came across your website, feel free to open an issue and I will try to respond in a timely manner, letting you know how your site was discovered/what resource made it into my database. This was most likely from my java version of this.
  
---
Currently working on a C++ version of this with Cmake.
