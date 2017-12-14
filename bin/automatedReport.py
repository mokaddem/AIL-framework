#!/usr/bin/env python2
# -*-coding:UTF-8 -*
"""
"""

import time, datetime
import re
import os
from pubsublogger import publisher
from packages import Paste
from Helper import Process
import json

desc_mapping = {
        'credential': "This paste contains leaked credentials. A credentials is the combinaison of the username and the password related to a particular website or service requering authentication."
        }

def itemize(array):
    if len(array) > 0:
        print(type(array), array)
        print('\n'.join([ '\item[-] {}'.format(s) for s in array]))
        return '\n'.join([ '\item[-] {}'.format(s) for s in array])
    else:
        return '\item[] '

def generate_report(message):
    module_name, filepath, raw_info = message.split(';')
    info = json.loads(raw_info)
    paste = Paste.Paste(filepath)
    paste_name = paste.p_name
    content = paste.get_p_content().decode('utf8')
    date = datetime.datetime.now()
    today = str(date.year)+'/'+str(date.month)+'/'+str(date.day)

    with open('reports/report_template.tex', 'r') as f:
        latex_template = f.read().decode('utf8')

    if module_name == 'credential':
        latex_template = latex_template.replace('{time}', today)
        latex_template = latex_template.replace('{module}', module_name)
        latex_template = latex_template.replace('{paste}', paste_name)
        latex_template = latex_template.replace('{num}', str(info['num']))
        latex_template = latex_template.replace('{dup}', itemize(json.loads(paste._get_p_duplicate())))
        latex_template = latex_template.replace('{desc}', desc_mapping[module_name])
        latex_template = latex_template.replace('{sites}', itemize(info['sites']))
        latex_template = latex_template.replace('{content}', content)

    now = int(time.time())
    report_name = 'reports/{}:{}'.format(module_name,now)
    with open(report_name+'.tex', 'w') as f:
        f.write(latex_template.encode('utf8'))

    # compile latex
    os.system('pdflatex -output-directory reports/ {}'.format(report_name))
    # delete temp files
    os.system('rm {}'.format(report_name+'.aux'))
    os.system('rm {}'.format(report_name+'.log'))
    os.system('rm {}'.format(report_name+'.tex'))


if __name__ == '__main__':
    # If you wish to use an other port of channel, do not forget to run a subscriber accordingly (see launch_logs.sh)
    # Port of the redis instance used by pubsublogger
    publisher.port = 6380
    # Script is the default channel used for the modules.
    publisher.channel = 'Script'

    # Section name in bin/packages/modules.cfg
    config_section = 'automatedReport'

    # Setup the I/O queues
    p = Process(config_section)

    # Sent to the logging a description of the module
    publisher.info("automatedReport running")

    # Endless loop getting messages from the input queue
    while True:
        # Get one message from the input queue
        message = p.get_from_set()
        if message is None:
            publisher.debug("{} queue is empty, waiting".format(config_section))
            time.sleep(1)
            continue

        # Do something with the message from the queue
        genearte_report(message)

