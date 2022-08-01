INSTRUCTION TO PARSER
------------------------------------]
Parser - a program to automaticaly get some data from web-sites.
In the program(and prog. files) presented two kind of parsers. Each of them executes specific functions.I have 
writen the program, but i haven't write an interface, so i made a program control right in program files, exactly 'main.py' file.
To use parsing you need to come up with your own algorythm in code. The reason i'he done so, is the time user would spent on writing commands and a number of commands
should be writen to make an even a little-bit adequate parser). So, let me explain how to use the program.


0) !!!To use dynamic parsing you must download and and to path browser drivers. NECESSARILY visit Python Selenium 
   official page. If you ever want to rebuild your app it will be useful. 
   Also don't forget to set your "User-Agent" in config file!!!!!!!!! 
		
1) [STATIC PARSING] fast way to get data which are initially loaded with HTML page. Static items don't use JavaScript 
to show themselfes on web-page and you don't need to integrate delays to parse it.
	--)To parse statical item you can use writen user console interface(it's commented)
	--)Else you can write algorythm yourself using StaticItem, parse_static and other
	   functions which are discribed in program files.	

2) [DYNAMIC PARSING] slower way with bigger count of opportunities. Using dynamic parsing you can build algorythm 
with clicking buttons, login, waiting etc...Dynamic parsing can get all kinds of data which aren't in initial HTML
page.
	--) To parse dynamic item you need to indicate a sequence of actions you need to do. For exapmle: 
	you need to parse phone number, but it's covered by button item, so you can't parse phone until
	button's unclicked.
	--) To use dynamic parser you need a CHROME browser installed on your computer(other browsers are also 
	available, but you need to change code). Program will automaticaly install needed version of browser.

3) [PARAMETERS] You can change program setting in file 'config.py'. Everything about program parameters is already writen in program file by comments. 

4) [ACTION CHAIN] The chain of program actions will be displayed in console window(Including errors).

5) [HOW TO INDICATE AN ITEM] To indicate an item you want to parse, you need to do Right Mouse Click and "Inspect". This item will be 
StaticItem by default. If it doesn't parse, you can try to parse it dynamicly.

6) [EXEL | DATA TABLE] You could notice that in file 'config.py' there is parameter FILENAME with 'xlsx' resolution. That means 
EXEL file, where into parsed data will be loaded. For loading data you can use function 'insert_data' from file
'exel_utils.py'. To select data from specific column by it's name, use function 'get_data_fro_col' from that file.

7) [GROUPED PARSING | MULTITHREAD]  Program works using multithreading to decrease time of data parsing. Program works with a group of pages
   in each thread. I added an option to set count of pages in group. To explain a principle "in a nutshell": you have 10 pages and set 
   5 pages in group, so program will parse 1...5 pages and 6...10 in another(using 2 threads) and so. In one group program uses one proxy
   IP address. It gets proxies from proxie file and selects an amout of working proxies(count written in confin file). You can find free proxies
   in the Internet and check it there.

8) [LOGIN] Program also has an option to login into an account. But there is a risk to account to be banned or disabled(solvation could be
   to set big amount of pages in group). 

I hope i didn't forget anything and the program will be usefull for anybody who reads this. Good luck:)


 
 