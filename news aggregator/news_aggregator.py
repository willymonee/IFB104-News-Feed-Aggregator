
#-----Assignment Description-----------------------------------------#
#
#  News Feed Aggregator
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application that allows the user to aggregate RSS news feeds.
#  See the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.
#
# NB: You may NOT use any Python modules that need to be downloaded
# and installed separately, such as "Beautiful Soup" or "Pillow".
# Only modules that are part of a standard Python 3 installation may
# be used. 

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.  You may import other widgets
# from the Tkinter module provided they are ones that come bundled
# with a standard Python 3 implementation and don't have to
# be downloaded and installed separately.)
from tkinter import *
from tkinter import ttk
# Import a special Tkinter widget we used in our demo
# solution.  (You do NOT need to use this particular widget
# in your solution.  You may import other such widgets from the
# Tkinter module provided they are ones that come bundled
# with a standard Python 3 implementation and don't have to
# be downloaded and installed separately.)
from tkinter.scrolledtext import ScrolledText
from tkinter import scrolledtext

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed one day).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----------------------------------------------------------
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document or RSS Feed.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will hide its identity
#      from the web server. This can be used to prevent the
#      server from blocking access to Python programs. However
#      we do NOT encourage using this option as it is both
#      unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'xhtml',
             save_file = True,
             char_set = 'UTF-8',
             lying = True,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#
#Create a Tk window and give it a title
window = Tk()
window.title('Gaming & Anime News Aggregator')

#Set font styles
title_font = ('TW Cen MT Condensed', 32)
heading_font = ('TW Cen MT Condensed', 24)
text_font = ('TW Cen MT Condensed', 20)



#Create label widget for the title
news_mixer_text = Label(window, text = 'Gaming & Anime News Mixer',
                        font = title_font, width = 10)
#Add image to GUI
anime_image = PhotoImage(file="gaminganime.png")
anime_image_label = Label(window, image = anime_image)
#Create Live News Feed Column
live_news_feed = Canvas(window, bg = 'light yellow', height = 500)
live_news_heading = Label(live_news_feed, text = 'Live News Feeds',
                          font = heading_font, bg = 'light yellow')
rps_feed = Label(live_news_feed, text = 'Rock Paper Shotgun', font = text_font,
                    bg = 'light yellow')
rps_select = ttk.Combobox(live_news_feed, values =
                                  ['0', '1', '2', '3',
                                   '4','5', '6', '7', '8', '9',
                                   '10', '11', '12'], font = text_font,
                                  state = 'readonly')
rps_select.current(0)#set default value as the 1st value
pcgamer_feed = Label(live_news_feed, text = 'PC Gamer', font = text_font,
                    bg = 'light yellow')
pcgamer_select = ttk.Combobox(live_news_feed, values =
                                  ['0', '1', '2', '3', '4'
                                   ,'5', '6', '7', '8', '9',
                                   '10', '11', '12'], font = text_font,
                                  state = 'readonly')
pcgamer_select.current(0)#set default value as the 1st value

#Create Past News Feed Column 
past_news_feed = Canvas(window, bg = 'azure')
past_news_heading = Label(past_news_feed, text = 'Past News Feeds',
                          font = heading_font, bg = 'azure')
crunchyroll_feed = Label(past_news_feed, text = 'Crunchyroll', font = text_font,
                    bg = 'azure')
crunchyroll_select = ttk.Combobox(past_news_feed, values = ['0', '1', '2', '3', '4'
                                                ,'5', '6', '7', '8', '9',
                                                '10', '11', '12'], font = text_font
                                                ,state = 'readonly')
crunchyroll_select.current(0)#set default value as the 1st value

kotaku_feed = Label(past_news_feed, text = 'Kotaku', font = text_font,
                    bg = 'azure')
kotaku_select = ttk.Combobox(past_news_feed, values = ['0', '1', '2', '3', '4'
                                                    ,'5', '6', '7', '8', '9',
                                                    '10', '11', '12'], font = text_font
                                                    ,state = 'readonly')
kotaku_select.current(0)#set default value as the 1st value


#Create title for stories selected section
stories_selected_title = Label(window, text = 'Stories Selected',
                               font = heading_font)

#Create stories selected output section
output_section = Frame(window)

#Create a text widget to display the results
text = scrolledtext.ScrolledText(master = output_section, wrap = 'word',
                                 width = 80, height = 11, font = text_font, state = 'normal')

                                 
#Open the past news feed files and read them, with exceptions if the file is not found
try:
    crunchyroll = open('crunchyroll.xhtml', encoding="utf8")
    crunchyroll_text = crunchyroll.read()
    crunchyroll.close()

except FileNotFoundError:
    print('The crunchyroll.xhtml file cannot be found, select stories from other sources \
    or add the file back into the directory folder')
    crunchyroll_select = ttk.Combobox(past_news_feed, values = ['0', '1', '2', '3', '4'
                                                ,'5', '6', '7', '8', '9',
                                                '10', '11', '12'], font = text_font
                                                ,state = 'disabled')
try:
    kotaku = open('kotaku.xml', encoding="utf8")
    kotaku_text = kotaku.read()
    kotaku.close()
except FileNotFoundError:
    print('The kotaku.xml file cannot be found, select stories from other sources or \
    add the file back into the directory folder')
    kotaku_select = ttk.Combobox(past_news_feed, values = ['0', '1', '2', '3', '4'
                                                ,'5', '6', '7', '8', '9',
                                                '10', '11', '12'], font = text_font
                                                ,state = 'disabled')

#Open the live news feeds and read them with exceptions if the URL is invalid 
try:
    rps = urlopen('https://www.rockpapershotgun.com/')
    rps_text = rps.read().decode("UTF-8")
    rps.close()
except OSError: #prints statement and disables the combobox
    print('Invalid URL is used when attempting to open Rock Paper Shotgun')
    rps_select = ttk.Combobox(live_news_feed, values = ['0', '1', '2', '3', '4'
                                                ,'5', '6', '7', '8', '9',
                                                '10', '11', '12'], font = text_font
                                                ,state = 'disabled')
except: 
    print('Could not reach Rock Paper Shotgun, it may be down or updating')
    rps_select = ttk.Combobox(live_news_feed, values = ['0', '1', '2', '3', '4'
                                                ,'5', '6', '7', '8', '9',
                                                '10', '11', '12'], font = text_font
                                                ,state = 'disabled')

try:
    pcgamer = urlopen('https://www.pcgamer.com/au/news/')
    pcgamer_text = pcgamer.read().decode("UTF-8")
    pcgamer.close()
except OSError:
    print('Invalid URL is used when attempting to open PC Gamer')
    pcgamer_select = ttk.Combobox(live_news_feed, values = ['0', '1', '2', '3', '4'
                                                ,'5', '6', '7', '8', '9',
                                                '10', '11', '12'], font = text_font
                                                ,state = 'disabled')
except:
    print('Could not reach PC Gamer, it may be down or updating')
    pcgamer_select = ttk.Combobox(live_news_feed, values = ['0', '1', '2', '3', '4'
                                                ,'5', '6', '7', '8', '9',
                                                '10', '11', '12'], font = text_font
                                                ,state = 'disabled')


##Create function when export button is pressed
def export():
    #get value selected by user for the news feeds converting them from string to int data format
    amount_crunchyroll_selected = int(crunchyroll_select.get())
    amount_kotaku_selected = int(kotaku_select.get())
    amount_rps_selected = int(rps_select.get())
    amount_pcgamer_selected = int(pcgamer_select.get())
    amount_selected = amount_crunchyroll_selected + amount_kotaku_selected \
    + amount_rps_selected  + amount_pcgamer_selected
      

    #Find and display the titles, dates and source of stories selected
    #from Crunchyroll
    crunchyroll_headline = findall('<title>(.*)</title>', crunchyroll_text)
    crunchyroll_date = findall('<pubDate>(.*)</pubDate>', crunchyroll_text)
    #find byline and text
    crunchyroll_byline =  findall('<description>(.*?)&lt;br/&gt;&lt;', crunchyroll_text)
    crunchyroll_paragraph =  findall('/&gt;&lt;br/&gt;&lt;br/&gt;&lt;p&gt;(.*?)</description>', crunchyroll_text)
    crunchyroll_image = findall('&lt;br/&gt;&lt;img src="(.*)"  /&gt;&lt;br/&gt;&lt;br/&gt;&lt;p&gt;', crunchyroll_text)
        
    #Find and display the titles, dates and source of stories selected
    #from Kotaku 
    kotaku_headline = findall('<title>(.*)</title>', kotaku_text)
    kotaku_date = findall('<pubDate>(.*)</pubDate>', kotaku_text)
    kotaku_image = findall('<img src="(.*)" />', kotaku_text)
    kotaku_paragraph = findall('<description>\n*.* /><p>(.*?)</p>', kotaku_text)
    kotaku_author = findall('<dc:creator>\n*-<!\[CDATA\[(.*)\]\]>', kotaku_text)
    #Find and display the titles, dates and source of stories selected from
    #rockpaper shotgun
    rps_headline = findall('<p class="title">\n*\s*<a href=".*">(.*)</a>\n*\s*</p>', rps_text)
    rps_date = findall('<span>&bull;</span>\n*\s*(.*?)<', rps_text)
    rps_author = findall('rel="author">(.*)</a>', rps_text)
    rps_image = findall('data-original="(.*)"', rps_text)
    rps_paragraph = findall('<div class="excerpt">\s*\n*\s*\n*<p>\n*(.*)</p>\n*.*\n*\s*</div>', rps_text)

    #Find and display the titles, dates and source of stories selected from
    #PC Gamer
    pcgamer_headline = findall('<h3 class="article-name">(.*)</h3>', pcgamer_text)
    pcgamer_date = findall('data-published-date="(.*)"></time>', pcgamer_text)
    pcgamer_author = findall('<span style="white-space:nowrap">\n(.*)</span>', pcgamer_text)
    pcgamer_paragraph = findall('<p class="synopsis">.*\n*(.*)\n*</p>', pcgamer_text)
    pcgamer_image = findall('<figure class="article-lead-image-wrap" data-original="(.*)">', pcgamer_text)
    #refresh current text displayed
    response.delete(1.0, END)
    text.delete(1.0, END)
    
    #create for loop to insert the selected amount of reports from crunchyroll
    #into text box in GUI
    next_value = 1 #value starts at 1 because 1st value is the not a headline
    try:
        for headlines in range(amount_crunchyroll_selected):
            text.insert('insert', '"'+ crunchyroll_headline[next_value] +'"' + ' - '
                       + crunchyroll_headline[0] + ' - ' + crunchyroll_date[next_value] + '\n' + '\n')
            next_value = next_value + 1
    except IndexError: #create exception if the amount selected from the combobox exceeds the \
         #amount of stories available in crunchyroll which would cause an Index Error
         print('There are not ' + str(amount_crunchyroll_selected) + ' stories available on Crunchyroll, \
         there are only ' + str(len(crunchyroll_paragraph)) +  ' stories available')
        

    #create for loop to insert the selected amount of reports from kotaku
    #into text box in GUI
    try:
        for headlines in range(amount_kotaku_selected):
            text.insert('insert', '"'+ kotaku_headline[next_value] +'"' + ' - '
                       + kotaku_headline[0] + ' - ' + kotaku_date[next_value] + '\n' + '\n')
            next_value = next_value + 1
    except IndexError:
        print('There are not ' + str(amount_kotaku_selected) + ' stories available on Kotaku, there are only ' \
              + str(len(kotaku_paragraph)) +  ' stories available')
   


    
    #create for loop to insert the selected amount of reports from RPS
    #into the GUI
    list_value = 0
    try:
        for headines in range(amount_rps_selected):
            text.insert('insert', '"'+ rps_headline[list_value] +'"' + ' - ' +
                       'Rock Paper Shotgun' + ' - ' + rps_date[list_value] + '\n' + '\n')
            list_value = list_value + 1
    except IndexError: #create exception if the amount selected from the combobox exceeds the amount of stories available in RPS which would cause an Index Error
        print('There are not ' + str(amount_rps_selected) + ' stories available on Rock Paper Shotgun, there are only: ' + str(len(rps_headline)) +  ' stories available')




    #Create for loop to insert the selected amount of reports from PC Gamer into GUI
    try:
        for headlines in range(amount_pcgamer_selected):
            text.insert('insert', '"' + pcgamer_headline[list_value] + '"' + ' - '
                        + 'PC Gamer' + ' - ' + pcgamer_date[list_value] + '\n' + '\n')
            list_value = list_value + 1
    except IndexError: #create exception if the amount selected from the combobox exceeds the amount of stories available in PC Gamer which would cause an Index Error
        print('There are not ' + str(amount_pcgamer_selected) + ' stories available on PC Gamer, there are only ' + str(len(pcgamer_headline)) +  ' stories available')

        
    if amount_selected > 0:
            response.insert('insert', ' Files Sucessfully Exported')
    else:
            response.insert('insert', 'No files selected')


    # Name of the exported news file. To simplify marking, your program
    # should produce its results using this file name.
    #Create exported file
    news_file_name = 'news.html'
    print('Creating HTML file: ', news_file_name)
    html_file = open(news_file_name, 'w', encoding = 'UTF-8')

    #write the HTML documentation
    html_file.write('''<!DOCTYPE html>
    <html>
        <head>
        <style>
            body {
              font-family: "Tw Cen MT Condensed", Arial, sans-serif;
            }
            #container{
                width: 70%;
                margin: auto;
                background-color:#F5F5F5;
            }

            h1 {
                font-size: 48px;
                text-align: center;
                color: white;
            }
            h2 {
                font-size: 38px;
                text-align: center;
                text-decoration: underline;
                margin-bottom: -10px;
            }
            h3{
                font-size: 32px;
                text-align: center;
                margin-top: 50px;
            }
            header {
                background-color:#111111;
                margin-bottom: -32px;
            }
            h4{
                font-size: 24px;
                font-weight: normal;
                text-align: center;
                margin-top: -5px;
            }
            p{
                font-size: 28px;
                width: 65%;
                margin-left: auto;
                margin-right: auto;
                display: block;
                text-align: center;
                line-height: 1.575;
            }
            .crunchyroll {
                height: 250px;
                width: 250px;

            }
            .kotaku_img{
                height: 350px;
                width: 575px;
            }
            img {
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            nav {
                padding-bottom:5px;
                padding-top:5px;
                font-size:28px;
                text-weight: bold;
                color: white;
                background-color:#B22222;
                position: sticky;
                position: -webkit-sticky;
                overflow: hidden;
                top:0;
            }
            nav a {
                color: white;
                padding-right:7.5%;
                padding-left:7.5%;

            }
            hr {
                border: 1px solid #B22222;
                border-radius: 3px;
            }
            p a {
                color: black;
            }
            p a:active {
                color: #B22222;
            }
            hr {
            width: 85%;
            }
        </style>
            <title>Gaming and Anime News</title>
        </head>
        <body>
        <div id = "container">
        <header>
        <h1>GAMING AND ANIME NEWS</h1>
        </header>
        <nav>
            <a href="#crunchyroll">CRUNCHYROLL</a> |
            <a href="#kotaku">KOTAKU</a> |
            <a href="#rps">ROCK PAPER SHOTGUN</a> |
            <a href="#pcgamer">PC GAMER</a>
        </nav>
    ''')
    #export crunchyroll news
    #convert html or remove it when exported 
    p_value = 0
    for paragraph in range (len(crunchyroll_paragraph)):
        crunchyroll_paragraph[p_value] = crunchyroll_paragraph[p_value].replace(r'&lt;','<')
        crunchyroll_paragraph[p_value] = crunchyroll_paragraph[p_value].replace(r'&gt;','>')
        crunchyroll_paragraph[p_value] = crunchyroll_paragraph[p_value].replace(r'&amp;nbsp;',' ')
        p_value = p_value + 1
 
 
    next_value = 1 #value starts at 1 because 1st value is the not a headline
    if amount_crunchyroll_selected > 0:
        html_file.write('<h2 id = "crunchyroll">News From Crunchyroll</h2>')
        for crunchyroll_content in range(amount_crunchyroll_selected):
            try:
                html_file.write('<h3>'+ crunchyroll_headline[next_value] +'</h3>')
            except IndexError: #exception if the findall pattern has returned no values (due to changes in the site)
                if len(crunchyroll_headline) == 0:
                    print('Could not find any headlines for Crunchyroll')
            try:
                html_file.write('<h4>'+ crunchyroll_date[next_value] +'</h4>')
            except IndexError:
                if len(crunchyroll_date) == 0:
                    print('Could not find any dates for Crunchyroll')
            try:
                html_file.write('<img class = "crunchyroll" src="' + crunchyroll_image[next_value - 1] + '">')
            except IndexError:
                if len(crunchyroll_image) == 0:
                    print('Could not find any images for Crunchyroll')
            try:
                html_file.write('<p>'+ crunchyroll_byline[next_value - 1] + '. ' + crunchyroll_paragraph[next_value - 1] +'</p>')
            except IndexError:
                if len(crunchyroll_byline) == 0:
                    print('Could not find any bylines for Crunchyroll')
                elif len(crunchyroll_paragraph) == 0:
                    print('Could not find any text for Crunchyroll')
            html_file.write('<hr>')
            next_value = next_value + 1
            
    #export kotaku news
    if amount_kotaku_selected > 0:
        html_file.write('<h2 id = "kotaku">News From Kotaku</h2>')
        try:
            for kotaku_content in range(amount_kotaku_selected):
                try:
                    html_file.write('<h3>'+ kotaku_headline[next_value] +'</h3>')
                except IndexError:
                    if len(kotaku_headline) == 0:
                        print('Could not find any headlines for Kotaku')
                try:
                    html_file.write('<h4>'+ kotaku_author[next_value - 1] + ' - ' + kotaku_date[next_value] +'</h4>')
                except IndexError:
                    if kotaku_author == 0:
                        print('Could not find any authors for Kotaku')
                    if len(kotaku_date) == 0:
                        print('Could not find any dates for Kotaku')
                try:
                    html_file.write('<img class = "kotaku_img" src="' + kotaku_image[next_value - 1] + '">')
                except IndexError:
                    if len(kotaku_image) == 0:
                        print('Could not find any images for Kotaku')                
                try:
                    html_file.write('<p>'+ kotaku_paragraph[next_value - 1] +'</p>')
                except IndexError:
                    if len(kotaku_paragraph) == 0:
                        print('Could not find any text for Kotaku')
                html_file.write('<hr>')
                next_value = next_value + 1
        except IndexError:
            if len(kotaku_headline) > 0:
                print('Exported: ' + str(len(kotaku_paragraph)) + ' files from Kotaku instead of ' + str(amount_kotaku_selected))

    #Export rock paper shotgun news
    list_value = 0
    if amount_rps_selected > 0:
        html_file.write('<h2 id = "rps">News From Rock Paper Shotgun</h2>')
        for rps_content in range(amount_rps_selected):
            try:
                html_file.write('<h3>'+ rps_headline[list_value + 3] +'</h3>')
            except IndexError:
                if len(rps_headline) == 0:
                    print('Could not find any headlines for Rock Paper Shotgun')
            try:
                html_file.write('<h4>'+ 'By:' + rps_author[list_value] + ' - ' + rps_date[list_value] +'</h4>')
            except IndexError:
                if len(rps_author) == 0:
                    print('Could not find any authors for Rock Paper Shotgun')
                elif len(rps_date) == 0:
                    print('Could not find any dates for Rock Paper Shotgun')
            try:
                html_file.write('<img class = "kotaku_img" src="' + rps_image[list_value] + '">')
            except IndexError:
                if len(rps_image) == 0:
                    print('Could not find any images for Rock Paper Shotgun')                
            try:
                html_file.write('<p>' + rps_paragraph[list_value] + '</p>')
            except IndexError:
                if len(rps_paragraph) == 0:
                     print('Could not find any paragraphs for Rock Paper Shotgun')                
            html_file.write('<hr>')
            list_value = list_value + 1


    #Export PC Gamer News
    if amount_pcgamer_selected > 0:
        html_file.write('<h2 id = "pcgamer">News From PC Gamer</h2>')
        for pcgamer_content in range(amount_pcgamer_selected):
            try:
                html_file.write('<h3>' + pcgamer_headline[list_value] +'</h3>')
            except IndexError:
                if pcgamer_headline == 0:
                    print('Could not find any headlines from PC Gamer')
            try:
                html_file.write('<h4>'+ 'By:' + pcgamer_author[list_value] + ' - ' + pcgamer_date[list_value]+ '</h4>')
            except IndexError:
                if len(pcgamer_date) == 0:
                    print('Could not find any dates for PC Gamer')
                elif len(pcgamer_author) == 0:
                    print('Could not find any authors')
            try:
                html_file.write('<img class = "kotaku_img" src="' + pcgamer_image[list_value] + '">')
            except IndexError:
                if len(pcgamer_image) == 0:
                    print('Could not find any images for PC Gamer')
            try: 
                html_file.write('<p>' + pcgamer_paragraph[list_value] + '</p>')
            except IndexError:
                if len(pcgamer_paragraph) == 0:
                    print('Could not find any text for PC Gamer')     
            html_file.write('<hr>')
            list_value = list_value + 1

    #Write List of Sources
    html_file.write('<h3>Sources</h3>')
    html_file.write('<p>Crunchyroll - <a href="http://feeds.feedburner.com/crunchyroll/animenews" target="_blank">http://feeds.feedburner.com/crunchyroll/animenews</a></p>')
    html_file.write('<p>Kotaku - <a href="https://www.kotaku.com.au/" target="_blank">https://www.kotaku.com.au/</a></p>')
    html_file.write('<p>Rock Paper Shotgun - <a href="https://www.rockpapershotgun.com/" target="_blank">https://www.rockpapershotgun.com/</a></p>')
    html_file.write('<p>PC Gamer - <a href="https://www.pcgamer.com/au/news/" target="_blank">https://www.pcgamer.com/au/news/</a></p>')
    

    #Write the end of the opening tags
    html_file.write('</div>')
    html_file.write('</body>')
    html_file.write('</html>')

    #Close the HTML file
    html_file.close()

def save(): #create function for save button to save selections to database
    #get value selected by user for the news feeds converting them from string to int data format
    amount_crunchyroll_selected = int(crunchyroll_select.get())
    amount_kotaku_selected = int(kotaku_select.get())
    amount_rps_selected = int(rps_select.get())
    amount_pcgamer_selected = int(pcgamer_select.get())
    amount_selected = amount_crunchyroll_selected + amount_kotaku_selected \
    + amount_rps_selected  + amount_pcgamer_selected
      

    #Find and display the titles, dates and source of stories selected
    #from Crunchyroll
    crunchyroll_headline = findall('<title>(.*)</title>', crunchyroll_text)
    crunchyroll_date = findall('<pubDate>(.*)</pubDate>', crunchyroll_text)
    #find byline and text
    crunchyroll_byline =  findall('<description>(.*?)&lt;br/&gt;&lt;', crunchyroll_text)
    crunchyroll_paragraph =  findall('/&gt;&lt;br/&gt;&lt;br/&gt;&lt;p&gt;(.*?)</description>', crunchyroll_text)
    crunchyroll_image = findall('&lt;br/&gt;&lt;img src="(.*)"  /&gt;&lt;br/&gt;&lt;br/&gt;&lt;p&gt;', crunchyroll_text)
        
    #Find and display the titles, dates and source of stories selected
    #from Kotaku 
    kotaku_headline = findall('<title>(.*)</title>', kotaku_text)
    kotaku_date = findall('<pubDate>(.*)</pubDate>', kotaku_text)
    kotaku_image = findall('<img src="(.*)" />', kotaku_text)
    kotaku_paragraph = findall('<description>\n*.* /><p>(.*?)</p>', kotaku_text)
    kotaku_author = findall('<dc:creator>\n*-<!\[CDATA\[(.*)\]\]>', kotaku_text)
    #Find and display the titles, dates and source of stories selected from
    #rockpaper shotgun
    rps_headline = findall('<p class="title">\n*\s*<a href=".*">(.*)</a>\n*\s*</p>', rps_text)
    rps_date = findall('<span>&bull;</span>\n*\s*(.*?)<', rps_text)
    rps_author = findall('rel="author">(.*)</a>', rps_text)
    rps_image = findall('data-original="(.*)"', rps_text)
    rps_paragraph = findall('<div class="excerpt">\s*\n*\s*\n*<p>\n*(.*)</p>\n*.*\n*\s*</div>', rps_text)

    #Find and display the titles, dates and source of stories selected from
    #PC Gamer
    pcgamer_headline = findall('<h3 class="article-name">(.*)</h3>', pcgamer_text)
    pcgamer_date = findall('data-published-date="(.*)"></time>', pcgamer_text)
    pcgamer_author = findall('<span style="white-space:nowrap">\n(.*)</span>', pcgamer_text)
    pcgamer_paragraph = findall('<p class="synopsis">.*\n*(.*)\n*</p>', pcgamer_text)
    pcgamer_image = findall('<figure class="article-lead-image-wrap" data-original="(.*)">', pcgamer_text)
    
    try:
        #make a connection to the database and get a cursor on it
        connection = connect(database = "news_log.db")
        saved_selections = connection.cursor()
        
        #delete previous selections saved
        delete = "DELETE FROM selected_stories"
        saved_selections.execute(delete)

        #insert new selections
        save_value = 0
        try:
            for selections in range(amount_crunchyroll_selected):
                save_value = save_value + 1
                saved_selections.execute("INSERT INTO selected_stories(headline,news_feed,publication_date) VALUES(?, ?, ?)",\
                                         (crunchyroll_headline[save_value],'Crunchyroll',crunchyroll_date[save_value]))
        except IndexError: #exception when more stories are selected than available
            print('You selected more stories from Crunchyroll than available')
                
        try:
            for selections in range(amount_kotaku_selected):
                save_value = save_value + 1
                saved_selections.execute("INSERT INTO selected_stories(headline,news_feed,publication_date) VALUES(?, ?, ?)",\
                                         (kotaku_headline[save_value],'Kotaku',kotaku_date[save_value]))
        except IndexError:
            print('You selected more stories from Kotaku than available')
        try:
            for selections in range(amount_pcgamer_selected):
                saved_selections.execute("INSERT INTO selected_stories(headline,news_feed,publication_date) VALUES(?, ?, ?)",\
                                         (pcgamer_headline[save_value],'PC Gamer',pcgamer_date[save_value]))
                save_value = save_value + 1
        except IndexError:
            print('You selected more stories from Kotaku than available')
           
        try:
            for selections in range(amount_rps_selected):
                saved_selections.execute("INSERT INTO selected_stories(headline,news_feed,publication_date) VALUES(?, ?, ?)",\
                                         (rps_headline[save_value],'Rock Paper Shotgun',rps_date[save_value]))
                save_value = save_value + 1
        except IndexError:
                print('You selected more stories from Kotaku than available')
    except OperationalError: #exception if connection could not be made with database or tables not present
        print('Could not connect to the database')
            
    #commit changes and close connections
    connection.commit()
    saved_selections.close()
    connection.close()

  
#Create button frames
button_frame = Frame(window)

#Create export selected button
export_button = Button(button_frame, text = 'Export Selected', font = heading_font,
                       borderwidth = 3, bg = 'white', command = export)

#Create save selections button
save_button = Button(button_frame, text = 'Save Selected', font = heading_font,
                     borderwidth = 3, bg = 'white', command = save)

#Create area for button response to appear
response = Text(window, font = text_font, width = 30, height = 1)
    

#Geometry manager to put widgets into main window
news_mixer_text.grid(pady = (10, 0), row = 1, column = 1
                     ,sticky=E+W+S+N)
anime_image_label.grid(pady = (10,0), row = 5, column = 2)
live_news_feed.grid(padx = 15, pady = 15, row = 2, column = 1)
past_news_feed.grid(padx = 15, pady = 15, row = 2, column = 2)
stories_selected_title.grid(row = 3, column = 1, pady = 5)
output_section.grid(row = 4, column = 1, columnspan = 2)
button_frame.grid(pady = 15, row = 5, column = 1)
export_button.pack(side = "left", padx = 10)
save_button.pack(side = "left", padx = 10)
response.grid(padx = 170, pady= (0, 20), row = 6, ipady = 5, ipadx= 5, column = 1)

#Geometry manager to put widgets into live news feed column
live_news_heading.grid(padx = 125, pady = 5, row = 1, column = 1, columnspan = 2)
rps_select.grid(pady = 5, padx= 5, row = 2, column = 2)
rps_feed.grid(pady = 5, padx= 5, row =  2, column = 1)
pcgamer_select.grid(pady = 5, padx= 5, row = 3, column = 2)
pcgamer_feed.grid(pady = (10, 20), row =  3, column = 1)

#Geometry manager to put widgets into past news feed column
past_news_heading.grid(padx = 125, pady = 5, row = 1, column = 1, columnspan = 2)
crunchyroll_select.grid(pady = 5, padx= 5, row = 2, column = 2)
crunchyroll_feed.grid(pady = 5, padx= 5, row =  2, column = 1)
kotaku_select.grid(pady = 5, row = 3, column = 2)
kotaku_feed.grid(pady = (10, 20), row =  3, column = 1)

#Geometry manager to put widgets into stories selected output section
text.grid(padx=20,pady=10)






   


pass
