#!/usr/bin/env python2
# -*-coding:UTF-8 -*
"""
This module is consuming the Redis-list created by the ZMQ_Sub_Curve_Q Module.

This modules update a .csv file used to draw curves representing selected
words and their occurency per day.

..note:: The channel will have the name of the file created.

..note:: Module ZMQ_Something_Q and ZMQ_Something are closely bound, always put
the same Subscriber name in both of them.


This Module is also used for term frequency.

/!\ Top set management is done in the module Curve_manage_top_set


Requirements
------------

*Need running Redis instances. (Redis)
*Categories files of words in /files/ need to be created
*Need the ZMQ_PubSub_Tokenize_Q Module running to be able to work properly.

"""
import redis
import time
from pubsublogger import publisher
from packages import lib_words
import os
import datetime
import calendar

from Helper import Process

# Config Variables
BlackListTermsSet_Name = "BlackListSetTermSet"
TrackedTermsSet_Name = "TrackedSetTermSet"
top_term_freq_max_set_cardinality = 20 # Max cardinality of the terms frequences set
oneDay = 60*60*24
top_termFreq_setName_day = ["TopTermFreq_set_day_", 1]
top_termFreq_setName_week = ["TopTermFreq_set_week", 7]
top_termFreq_setName_month = ["TopTermFreq_set_month", 31]
top_termFreq_set_array = [top_termFreq_setName_day,top_termFreq_setName_week, top_termFreq_setName_month]


def check_if_tracked_term(term, path):
    if term in server_term.smembers(TrackedTermsSet_Name):
        #add_paste to tracked_word_set
        set_name = "tracked_" + term
        server_term.sadd(set_name, path)
        print term, 'addded', set_name, '->', path
        p.populate_set_out("New Term added", 'CurveManageTopSets')


def getValueOverRange(word, startDate, num_day):
    to_return = 0
    for timestamp in range(startDate, startDate - num_day*oneDay, -oneDay):
        value = server_term.hget(timestamp, word)
        to_return += int(value) if value is not None else 0
    return to_return



if __name__ == "__main__":
    publisher.port = 6380
    publisher.channel = "Script"

    config_section = 'Curve'
    p = Process(config_section)

    # REDIS #
    r_serv1 = redis.StrictRedis(
        host=p.config.get("Redis_Level_DB_Curve", "host"),
        port=p.config.get("Redis_Level_DB_Curve", "port"),
        db=p.config.get("Redis_Level_DB_Curve", "db"))

    server_term = redis.StrictRedis(
        host=p.config.get("Redis_Level_DB_TermFreq", "host"),
        port=p.config.get("Redis_Level_DB_TermFreq", "port"),
        db=p.config.get("Redis_Level_DB_TermFreq", "db"))

    # FUNCTIONS #
    publisher.info("Script Curve started")

    # FILE CURVE SECTION #
    csv_path = os.path.join(os.environ['AIL_HOME'],
                            p.config.get("Directories", "wordtrending_csv"))
    wordfile_path = os.path.join(os.environ['AIL_HOME'],
                                 p.config.get("Directories", "wordsfile"))

    message = p.get_from_set()
    prec_filename = None
    generate_new_graph = False

    # Term Frequency
    top_termFreq_setName_day = ["TopTermFreq_set_day_", 1]
    top_termFreq_setName_week = ["TopTermFreq_set_week", 7]
    top_termFreq_setName_month = ["TopTermFreq_set_month", 31]

    # TTL on key
    word_ttl = p.config.getint("Module_Curve", "ttl_word") # days
    word_ttl = word_ttl*24*60*60 # sec
    zrank_ttl = p.config.getint("Module_Curve", "ttl_zrank") # days
    zrank_ttl = zrank_ttl*24*60*60 # sec

    while True:

        if message is not None:
            generate_new_graph = True

            filename, word, score = message.split()
            temp = filename.split('/')
            date = temp[-4] + temp[-3] + temp[-2]
            timestamp = calendar.timegm((int(temp[-4]), int(temp[-3]), int(temp[-2]), 0, 0, 0))
            curr_set = top_termFreq_setName_day[0] + str(timestamp)


            low_word = word.lower()
            #Old curve with words in file
            #r_serv1.hincrby(low_word, date, int(score))

            # Update redis
            #consider the num of occurence of this term
            server_term.hincrby(timestamp, low_word, int(score))
            #1 term per paste
            server_term.hincrby("per_paste_" + str(timestamp), low_word, int(1))

            # Add in set only if term is not in the blacklist
            if low_word not in server_term.smembers(BlackListTermsSet_Name):
                #consider the num of occurence of this term
                server_term.zincrby(curr_set, low_word, float(score))
                #1 term per paste
                server_term.zincrby("per_paste_" + curr_set, low_word, float(1))
             
            #Add more info for tracked terms
            check_if_tracked_term(low_word, filename)

            # set expire
            if word_ttl > 0:
                server_term.expire(timestamp, word_ttl)
                server_term.expire("per_paste_" + str(timestamp), word_ttl)
            if zrank_ttl > 0:
                server_term.expire(curr_set, zrank_ttl)
                server_term.expire("per_paste_" + curr_set, zrank_ttl)

            #send to RegexForTermsFrequency
            to_send = "{} {} {}".format(filename, timestamp, word)
            p.populate_set_out(to_send, 'RegexForTermsFrequency')

        else:

            if generate_new_graph:
                generate_new_graph = False
                print 'Building graph'
                today = datetime.date.today()
                year = today.year
                month = today.month
                lib_words.create_curve_with_word_file(r_serv1, csv_path,
                                                      wordfile_path, year,
                                                      month)

            publisher.debug("Script Curve is Idling")
            print "sleeping"
            time.sleep(10)
        message = p.get_from_set()
