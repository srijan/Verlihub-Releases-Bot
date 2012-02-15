#!/usr/bin/env python2
# Created by Srijan Choudhary

import vh
import string

head = "==================== Release BOT ===================="
foot = "====================================================="
endl = "\r\n"

def header(text):
    return endl + endl + head + endl + text

def footer(text):
    return text + endl + foot + endl


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

def downloaderDeleteReleaseById(nick,idno):
    query = "DELETE FROM `pi_releases` WHERE `id`='"+idno+"' AND `added_by`='"+nick+"' LIMIT 1"
    res = vh.SQL(query)
    if res:
        return True
    else:
        return False

def adminDeleteReleaseById(idno):
    query = "DELETE FROM `pi_releases` WHERE `id`='"+idno+"' LIMIT 1"
    res = vh.SQL(query)
    if res:
        return True
    else:
        return False

categories = getCategoriesList()

help = """

================================================================
                         %[HUB]
                Release BOT Commands
================================================================

For users:
    +relhelp                    : Show this help
    +rel all                    : Show all releases
    +rel <category_name>        : Show releases for particular category


For downloaders:
    +reladd <category_name> <text>      : Adds new release.
    +reldelete <release_idno>           : Deletes a release.

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
    if data == "+uploads" or data == "+rel" or data == "+relhelp":
        vh.usermc(help,nick)
        return 0

    if data == "+help":
        vh.usermc(help,nick)
        return 1

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
        if vh.GetUserClass(nick) < 3:
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

    if data[:11] == "+reldelete ":
        userClass = vh.GetUserClass(nick)
        if userClass < 3:
            msg = "You need to have a downloader account to use this function."+endl+"Contact the hub owner with proof for getting a downloader account."
            vh.usermc(footer(header(msg)),nick)
            return 0
        idno = data[11:]
        if userClass < 4:
            res = downloaderDeleteReleaseById(nick,idno)
            if res:
                msg = "Release deleted successfully!"
            else:
                msg = "Either the release was not found, or you don't have sufficient privileges to delete some one else's release."
            vh.usermc(footer(header(msg)),nick)
            return 0
        res = adminDeleteReleaseById(idno)
        if res:
            msg = "Release deleted successfully!"
        else:
            msg = "The release #"+idno+" was not found."
        vh.usermc(footer(header(msg)),nick)
        return 0

    return 1
