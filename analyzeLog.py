# Analyzing elab logs for logins/submits using different IP during test
#  by Sethavidh Gertphol
#  18 Oct 2016
#  to do: 1. log file from command line
#         2. move into functions, refactor

import datetime
from operator import itemgetter

def parse_log(log_file):
    logins = []
    submits = []
    for line in open(log_file,'r'):
        log_line = []
        fields = line.split()
        if len(fields) == 5: #logins
            time_str = fields[2] + ' ' + fields[3]
            time_str = time_str.rstrip(']').lstrip('[')
            time_fmt = '%Y-%m-%d %H:%M:%S'
            time = datetime.datetime.strptime(time_str, time_fmt)
            if not (start_time < time < end_time): continue
            id_ip = fields[4].split('/')
            id = id_ip[0].lstrip('(')
            log_line.append(id)
            log_line.append(fields[0])
            log_line.append(time_str)
            log_line.append('LOGIN')
            logins.append(log_line)
        elif len(fields) == 11: # submits
            time_str = fields[8] + ' ' + fields[9]
            time_str = time_str.rstrip(']').lstrip('[')
            time_fmt = '%Y-%m-%d %H:%M:%S'
            time = datetime.datetime.strptime(time_str, time_fmt)
            if not (start_time < time < end_time): continue
            id_ip = fields[10].split('/')
            id = id_ip[0].lstrip('(')
            log_line.append(id)
            log_line.append(fields[0])
            log_line.append(time_str)
            log_line.append('SUBMIT')
            log_line.append(fields[7]) #sec
            log_line.append(fields[5].rstrip(',')) #problem number
            submits.append(log_line)
    return logins, submits 
    
log1 = r'log.section497.txt'
log2 = r'log.section498.txt'

start_time = datetime.datetime(2016,10,9,9,00)
end_time = datetime.datetime(2016,10,9,12,10)

logins, submits = parse_log(log1)
logins2, submits2 = parse_log(log2)
logins.extend(logins2)
submits.extend(submits2)

d = {}
for i in logins:
    id = i[0]
    if id not in d:
        d[id] = []
    d[id].append(i)

for i in submits:
    id = i[0]
    if id not in d:
        d[id] = []
    d[id].append(i)
    
for i in d: #sort by time and analyze diff ip
    d[i].sort(key=itemgetter(2))
    ip_ls = []
    for x in d[i]:
        ip = x[1]
        if ip not in ip_ls:
            ip_ls.append(ip)
    if len(ip_ls) > 1:
        print(i, ': ')
        for x in d[i]:
            print(x)

while (1):
    id = input('\nEnter Student ID to check: ')
    if id == '': break
    if id not in d:
        print('No ID in DB')
    else:
        for x in d[id]:
            print(x)        