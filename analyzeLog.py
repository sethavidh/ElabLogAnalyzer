# Analyzing elab logs for logins/submits using different IP during test
#  by Sethavidh Gertphol
#  23 Oct 2019
#  to do: 1. list all IP subnets

from operator import itemgetter
import sys, os

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
            #time = datetime.datetime.strptime(time_str, time_fmt)
            if not (start_time < time_str < end_time): continue
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
            #time = datetime.datetime.strptime(time_str, time_fmt)
            if not (start_time < time_str < end_time): continue
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

def insert_db(db, logs):
    for i in logs:
        id = i[0]
        if id not in db:
            db[id] = []
        db[id].append(i)    

def insert_ip(ipdb, subnetdb, logs):
    for rec in logs:
        id = rec[0]
        ip = rec[1]
        if ip not in ipdb:
            ipdb[ip] = []
        if id not in ipdb[ip]:
            ipdb[ip].append(id)
        ip_subnet = rec[1].rpartition(".")[0]
        if ip_subnet not in subnetdb:
            subnetdb[ip_subnet] = []
        if id not in subnetdb[ip_subnet]:
            subnetdb[ip_subnet].append(id)

def showMultiIPSubmit(db):
    print("Submission from multiple IPs")
    for i in db: #sort by time and analyze diff ip
        db[i].sort(key=itemgetter(2))
        ip_ls = []
        for x in db[i]:
            ip = x[1]
            if ip not in ip_ls:
                ip_ls.append(ip)
        if len(ip_ls) > 1:
            print(i)

def showIPSubnets():
    print("%-11s %s" % ("IP Subnets", "Clients"))
    for elem in sorted(subnet.items()):
        print("%-11s % 7d" % (elem[0], len(elem[1])))
    print("")

def showMultiIDfromIP(ip_db):
    for ip in ip_db:
        if len(ip_db[ip]) > 1:
            print("%s: " % (ip), end='')
            for id in ip_db[ip]:
                print("%s " % id, end='')
            print('')

def clear(): 
  
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear')

log1 = sys.argv[1]
log2 = sys.argv[2]
start_time = sys.argv[3]
end_time = sys.argv[4]

logins, submits = parse_log(log1)
logins2, submits2 = parse_log(log2)
logins.extend(logins2)
submits.extend(submits2)

d = {}
subnet = {}
ip_db = {}
insert_db(d,logins)
insert_db(d,submits)
insert_ip(ip_db, subnet, logins)
insert_ip(ip_db, subnet, submits)

while (1):
    clear()
    showIPSubnets()
    showMultiIPSubmit()
    showMultiIDfromIP(ip_db)

    id = input('\nEnter choice:\n1) List IPs in Subnet\n2) Check Student Submission\n3) Show ID from IP\n0) Exit\n')
    if id == '0': break
    if id == '2':
        while 1:
            showMultiIPSubmit()
            stu_id = input("Enter Student ID (0 to backup): ")
            if stu_id == '0':
                break
            if stu_id not in d:
                print('No ID in DB')
            else:
                for x in d[stu_id]:
                    print(x)
    elif id == '1':
        showIPSubnets()
        while 1:
            subnet_id = input("Enter Subnet (0 to backup): ")
            if subnet_id == '0':
                break
            if subnet_id not in ips:
                print('No Subnet ID in DB')
            else:
                for x in sorted(ips[subnet_id]):
                    print(x)
    elif id == '3':
        for ip in ip_db:
            print("%s: " % (ip), end='')
            for id in ip_db[ip]:
                print("%s " % id, end='')
            print('')