#!/usr/bin/env python2
# Created by Srijan Choudhary

import vh
import string

# Config Variables. Change to suit your needs.

head = "==================== Release BOT ===================="
foot = "====================================================="
endl = "\r\n"
min_class_allow = 3                         # Minimum class allowed to add/delete releases
autocleaner_timer = 14400                   # Autocleaner runs every 14400 seconds
autocleaner_expire = '1 WEEK'               # How old entries to delete. Can be n DAY, n WEEK, n MONTH, n YEAR, etc..
show_debug_messages = True                  # Whether to show debug messages to Master

# End of Config Variables

def header(text):
    return endl + endl + head + endl + text

def footer(text):
    return text + endl + foot + endl

def report(msg):
    if show_debug_messages:
        vh.classmc('Release BOT: '+msg,10,10)

def getCategoriesList():
    query = "SELECT `name` FROM `pi_rel_categories`"
    res, rows = vh.SQL(query)
    if res:
        return rows
    else:
        return None

def getReleasesByCategory(cat):
    query = "SELECT `id`, `added_at`,`text`,`added_by` FROM `pi_releases` WHERE `category`='"+cat[0]+"' ORDER BY `added_at`"
    res, rows = vh.SQL(query)
    if res:
        return rows
    else:
        return None

def addRelease(cat,text,nick):
    query = "INSERT INTO `pi_releases` (`category`, `text`, `added_by`) VALUES ('"+cat[0]+"','"+text+"','"+nick+"')"
    res = vh.SQL(query)
    if res:
        return True
    else:
        return False

def getReleaseDownloader(idno):
    query = "SELECT `added_by` FROM `pi_releases` WHERE `id`="+idno+" LIMIT 1"
    res, rows = vh.SQL(query)
    if res:
        if rows != None:
            return rows[0]
        else:
            return None

def deleteReleaseById(idno):
    query = "DELETE FROM `pi_releases` WHERE `id`='"+idno+"' LIMIT 1"
    res = vh.SQL(query)
    if res:
        return True
    else:
        return False

def cleanOldReleases():
    query = "DELETE FROM `pi_releases` WHERE `added_at` < DATE_SUB(NOW(), INTERVAL "+autocleaner_expire+")"
    res = vh.SQL(query)
    if res:
        return True
    else:
        return False

def initSetupCheck():
    report('Running init check.')
    query = "SHOW TABLES LIKE 'pi_rel_categories'"
    res, rows = vh.SQL(query)
    if res:
        if rows == None:
            report("Release categories table not found. Creating default one.")
            query = """CREATE TABLE `pi_rel_categories` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `name` varchar(20) NOT NULL,
                        PRIMARY KEY (`id`)
                    )"""
            res = vh.SQL(query)
            if res:
                query = """INSERT INTO `pi_rel_categories` (`name`) VALUES
                            ('MOVIES'),
                            ('SERIES'),
                            ('MUSIC'),
                            ('GAMES'),
                            ('APPS'),
                            ('OTHERS')"""
                res = vh.SQL(query)
                if res:
                    report("Categories table created.")
        else:
            report("Categories table found.")
    query = "SHOW TABLES LIKE 'pi_releases'"
    res, rows = vh.SQL(query)
    if res:
        if rows == None:
            report("Releases table not found. Creating default one.")
            query = """CREATE TABLE `pi_releases` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `added_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        `category` varchar(20) NOT NULL,
                        `text` text,
                        `added_by` varchar(100) DEFAULT NULL,
                        PRIMARY KEY (`id`)
                    )"""
            res = vh.SQL(query)
            if res:
                    report("Releases table created.")
        else:
            report("Releases table found.")
    report("Loaded successfully. Type +relhelp for help.")

initSetupCheck()
categories = getCategoriesList()

help = """

================================================================
                         %[HUB]
                Release BOT Commands
================================================================

For downloaders:
    +reladd <category> <release>    : Adds new release.
                                    (Spaces allowed in release name)
    +reladdas <nick> <category> <release> : Add release as <nick>

    +relimport <category>           : Imports a list of releases.
    <release_1>                     : (release name cannot contain spaces)
    <release_2>
    ...

    +reldelete <release_idno>       : Deletes a release.

For users:
    +relhelp                    : Show this help
    +rel all                    : Show all releases
    +rel <category>             : Show releases for particular category

List of categories (case-insensitive):
""".replace("%[HUB]",vh.GetConfig("config", "hub_name"))
for cat in categories:
    help += endl+cat[0]
help += """

Anyone interested can view the source here: https://github.com/srijan/Verlihub-Releases-Bot
================================================================
"""


def OnUserCommand(nick,data):
    global categories
    if data == "+rel" or data == "+relhelp":
        vh.usermc(help,nick)
        return 0

    if data == "+help":
        vh.usermc(help,nick)
        return 1

    if data == "+uploads":
        msg = ""
        for cat in categories:
            rels = getReleasesByCategory(cat)
            if rels != None:
                msg += endl+cat[0]+":"+endl
                for rel in rels:
                    msg += rel[0]+".) "+rel[2]+" (By "+rel[3]+")"+endl
        vh.usermc(footer(header(msg)),nick)
        return 0

    if data[:5] == "+rel ":
        arg = data[5:].upper()

        if arg == "ALL":
            msg = ""
            for cat in categories:
                rels = getReleasesByCategory(cat)
                if rels != None:
                    msg += endl+cat[0]+":"+endl
                    for rel in rels:
                        msg += rel[0]+".) "+rel[2]+" (By "+rel[3]+")"+endl
            vh.usermc(footer(header(msg)),nick)
            return 0

        for cat in categories:
            if arg == cat[0]:
                msg = endl+cat[0]+":"+endl
                rels = getReleasesByCategory(cat)
                if rels != None:
                    for rel in rels:
                        msg += rel[0]+".) "+rel[2]+" (By "+rel[3]+")"+endl
                else:
                    msg += "No releases in this category"+endl
                vh.usermc(footer(header(msg)),nick)
                return 0

        msg = endl+"Usage:"+endl+endl+"+rel <category_name>"+endl+endl+"Where <category_name> is one of:"+endl+endl
        for cat in categories:
            msg += cat[0]+endl
        vh.usermc(footer(header(msg)),nick)
        return 0

    if data[:8] == "+reladd ":
        if vh.GetUserClass(nick) < min_class_allow:
            msg = "You need to have a downloader account to use this function."+endl+"Contact the hub owner with proof for getting a downloader account."
            vh.usermc(footer(header(msg)),nick)
            return 0
        args = data[8:].split()
        cat = [args[0].upper()]
        text = string.join(args[1:])
        if cat in categories:
            res = addRelease(cat,text,nick)
            if res:
                msg = "Release added successfully!"
            else:
                msg = "There was some error in adding the release."
            vh.usermc(footer(header(msg)),nick)
        else:
            msg = endl+"Usage:"+endl+endl+"+reladd <category_name> <text>"+endl+endl+"Where <category_name> is one of:"+endl+endl
            for cat in categories:
                msg += cat[0]+endl
            msg += endl+"And <text> can be any text (name, link, etc..)"+endl
            vh.usermc(footer(header(msg)),nick)
        return 0

    if data[:10] == "+reladdas ":
        if vh.GetUserClass(nick) < min_class_allow:
            msg = "You need to have a downloader account to use this function."+endl+"Contact the hub owner with proof for getting a downloader account."
            vh.usermc(footer(header(msg)),nick)
            return 0
        args = data[10:].split()
        newnick = args[0]
        cat = [args[1].upper()]
        text = string.join(args[2:])
        if cat in categories:
            res = addRelease(cat,text,newnick)
            if res:
                msg = "Release added successfully!"
            else:
                msg = "There was some error in adding the release."
            vh.usermc(footer(header(msg)),nick)
        else:
            msg = endl+"Usage:"+endl+endl+"+reladdas <nick> <category_name> <text>"+endl+endl+"Where <category_name> is one of:"+endl+endl
            for cat in categories:
                msg += cat[0]+endl
            msg += endl+"And <text> can be any text (name, link, etc..)"+endl
            vh.usermc(footer(header(msg)),nick)
        return 0

    if data[:11] == "+relimport ":
        if vh.GetUserClass(nick) < min_class_allow:
            msg = "You need to have a downloader account to use this function."+endl+"Contact the hub owner with proof for getting a downloader account."
            vh.usermc(footer(header(msg)),nick)
            return 0
        args = data[11:].split()
        cat = [args[0].upper()]
        relList = string.join(args[1:]).split()
        if cat in categories:
            msg = "Import Status:"+endl
            for rel in relList:
                res = addRelease(cat,rel,nick)
                if res:
                    msg += "Success: "
                else:
                    msg += "Fail: "
                msg += rel+endl
            vh.usermc(footer(header(msg)),nick)
        else:
            msg = endl+"Usage:"+endl+endl+"+relimport <category_name>"+endl+"<release 1>"+endl+"<release 2>"+endl+"..."+endl+endl+"Where <category_name> is one of:"+endl+endl
            for cat in categories:
                msg += cat[0]+endl
            msg += endl+"And <release n> can be any text (name, link, etc..) without spaces."+endl
            vh.usermc(footer(header(msg)),nick)
        return 0

    if data[:11] == "+reldelete ":
        userClass = vh.GetUserClass(nick)
        if userClass < min_class_allow:
            msg = "You need to have a downloader account to use this function."+endl+"Contact the hub owner with proof for getting a downloader account."
            vh.usermc(footer(header(msg)),nick)
            return 0

        idno = data[11:]
        downloader = getReleaseDownloader(idno)
        downloaderClass = vh.GetUserClass(downloader)

        if nick == downloader or userClass > downloaderClass:
            res = deleteReleaseById(idno)
            if res:
                msg = "Release deleted successfully!"
            else:
                msg = "The release #"+idno+" was not found."
        else:
            msg = "Cannot delete release #"+idno+endl+"Either it was not found, or was added by someone equal to or higher than you."
        vh.usermc(footer(header(msg)),nick)
        return 0
    return 1

timeCounter = 0
def OnTimer():
    global timeCounter
    if timeCounter == autocleaner_timer:
        report("Cleaning old releases")
        cleanOldReleases()
        timeCounter = 0
    else:
        timeCounter+=1
