#!/usr/bin/env python2
# Created by Srijan Choudhary

head = "==================== Release BOT ===================="
foot = "====================================================="
endl = "\r\n"

import vh

def header(text):
    return endl + endl + head + endl + text

def footer(text):
    return text + endl + foot + endl

help = """



"""

def getCategoriesList():
    query = "SELECT `name` FROM `pi_rel_categories`"
    res, rows = vh.SQL(query)
    if res:
        return rows
    else:
        return None

def getReleasesByCategory(cat):
    query = "SELECT `added_at`,`text`,`added_by` FROM `pi_releases` WHERE `category`='"+cat[0]+"' ORDER BY `added_at`"
    res, rows = vh.SQL(query)
    if res:
        return rows
    else:
        return None

def addRelease(cat,text,user):
    query = "INSERT INTO `pi_releases` (`category`, `text`, `added_by`) VALUES ('"+cat+"','"+text+"','"+user+"')"
    res = vh.SQL(query)
    if res:
        return True
    else:
        return False

def OnUserCommand(nick,data):
    if data == "+uploads" or data == "+rel":
        vh.pm(footer(header("Under Construction")),nick)
        return 0

    if data[:5] == "+rel ":
        arg = data[5:].upper()
        categories = getCategoriesList()

        if arg == "ALL":
            msg = ""
            for cat in categories:
                rels = getReleasesByCategory(cat)
                if rels != None:
                    msg += endl+cat[0]+":"+endl
                    for rel in rels:
                        msg += rel[0]+" : "+rel[1]+" (By "+rel[2]+")"+endl
            vh.pm(footer(header(msg)),nick)
            return 0

        for cat in categories:
            if arg == cat[0]:
                msg = endl+cat[0]+":"+endl
                rels = getReleasesByCategory(cat)
                if rels != None:
                    for rel in rels:
                        msg += rel[0]+" : "+rel[1]+" (By "+rel[2]+")"+endl
                else:
                    msg += "No releases in this category"+endl
                vh.pm(footer(header(msg)),nick)
                return 0

        msg = endl+"Usage:"+endl+endl+"+rel <category_name>"+endl+endl+"Where <category_name> is one of:"+endl+endl
        for cat in categories:
            msg += cat[0]+endl
        vh.pm(footer(header(msg)),nick)
        return 0

    #if data[:8] == "+reladd ":
    return 0
