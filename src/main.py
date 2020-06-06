import re
import json

regex_alias = re.compile('Alias Name: (?P<alias>.*)', re.IGNORECASE)
regex_subject = re.compile('Subject: (?P<subject>.*)', re.IGNORECASE)
regex_issuer = re.compile('Issuer: (?P<issuer>.*)', re.IGNORECASE)
regex_ldap = re.compile('(E|CN|OU|O|L|ST|C)=(?P<value>[^,]*)', re.IGNORECASE)
regex_end = re.compile('^\\*', re.IGNORECASE)

def is_year_included(value: str) -> bool:
    try:
        int(value[-4:])
        return True
    except ValueError:
        return False

with open("../certs.txt") as fp, open('results.csv',"w") as f:
    f.write('ClientID, Alias, Subject, E, CN, OU, O, L, ST, C, Issuer\n')
    for line in fp:
        alias = regex_alias.match(line)
        subject = regex_subject.match(line)
        issuer = regex_issuer.match(line)
        ldap = regex_ldap.findall(line)
        end = regex_end.match(line)
        if alias:
            if is_year_included(alias.group("alias")):
                f.write(alias.group("alias")[:-4] + ',')
            else:
                # if we cant find the year in the alias just leave it blank for now
                f.write(',')
            f.write(alias.group("alias") + ',')
        if subject:
            f.write('"' + subject.group("subject").replace('"','""') + '"' + ',')
            if ldap:
                test = json.dumps(dict(ldap))
                ldap_json = json.loads(test)
                if 'E' in ldap_json:
                    f.write('"' + ldap_json['E'].replace('\n','').replace('"','""') + '"' + ',')
                else:
                    f.write(',')
                if 'CN' in ldap_json:
                    f.write('"' + ldap_json['CN'].replace('\n','').replace('"','""') + '"' + ',')
                else:
                    f.write(',')
                if 'OU' in ldap_json:
                    f.write('"' + ldap_json['OU'].replace('\n','').replace('"','""') + '"' +',')
                else:
                    f.write(',')
                if 'O' in ldap_json:
                    f.write('"' + ldap_json['O'].replace('\n','').replace('"','""') + '"' + ',')
                else:
                    f.write(',')
                if 'L' in ldap_json:
                    f.write('"' + ldap_json['L'].replace('\n','').replace('"','""') + '"' + ',')
                else:
                    f.write(',')
                if 'ST' in ldap_json:
                    f.write('"' + ldap_json['ST'].replace('\n','').replace('"','""') + '"' + ',')
                else:
                    f.write(',')
                if 'C' in ldap_json:
                    f.write('"' + ldap_json['C'].replace('\n','').replace('"','""') + '"' + ',')
                else:
                    f.write(',')
        if issuer:
            f.write('"' + issuer.group("issuer").replace('"', '""') + '"')
        if end:
            f.write('\n')