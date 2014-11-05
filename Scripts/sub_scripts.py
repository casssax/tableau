import csv
import sys

def pie_tableau_db_file(db_file_name):
    with open(db_file_name, 'r') as db_file:
        print 'Creating PIE database append file'
        delim_type = ','
        data = csv.reader(db_file, delimiter=str(delim_type))
        data = [row for row in data]
        db_domains = {}
        db_header = data.pop(0)
        for line in data[1:]:
            domain = line[5]
            status = line[-1]
            # populate db_domains. dedupe by best record.
            if domain in db_domains:
                if db_domains[domain][-1] == 'Headquarter':
                    pass
                elif status == 'Headquarter':
                        db_domains[domain] = line
                else:
                    if db_domains[domain][-1] == '' and status != '':
                        db_domains[domain] = line
            else:                db_domains[domain] = line
        return (db_domains, db_header)

def append_tableau_file(input_file, out_file):
    # db_file_name will be the permanent name of file pulled from PIE database for Tableau.
    #     this name should always be the same and new files will overwrite the old file. 
    db_file_name = '\\\\192.168.1.179\\firmographics\\LSC-Firmagraphic-Database.csv'
    #db_file_name = 'LSC-Firmagraphic-Database.csv'
    # create the db_domains dictionary from PIE database file db_file_name. 
    db_domain_file, db_header = pie_tableau_db_file(db_file_name)
    print 'db_domain_file created'
    delim_type = ','
    data = csv.reader(input_file, delimiter=str(delim_type))
    #data = [row for row in data]
    #file_header = data.pop(0)
    header_flag = 1
    for csvdata in data:
        listdata = list(csvdata)
        if header_flag == 1:
            file_header = listdata
            new_line = ''
            for header_field in file_header:
                new_line = new_line + '"' + header_field + '"' + ','
            for db_header_field in db_header:
                new_line = new_line + '"' + db_header_field + '"' + ','
            out_file.write(new_line[:-1] + '\n')
            header_flag = 0
        else:
            new_line = ''
            domain = listdata[14]
            if domain in db_domain_file:
                for field in listdata:
                    new_line = new_line + '"' + field + '"' + ',' 
                for db_field in db_domain_file[domain]:
                    new_line = new_line + '"' + db_field + '"' + ',' 
                new_line = new_line[:-1] + '\n'
            else:
                for field in listdata:
                    new_line = new_line + '"' + field + '"' + ',' 
                #new_line = new_line + ",,,,,,,,,,,\n"
                new_line = new_line + '"","","","","","","","","","","",""\n'
                #print 'No Domain Found: ', domain
            out_file.write(new_line)

