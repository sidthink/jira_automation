
from jirafunctions import *
import logger
import csv




def run():
    log = logger.setup_applevel_logger(file_name= 'jira_debug.log')
   
    #parse the command line arguments
    args = argparser()

    csvfile1 = open(args.csv1, 'r')
    reader1 = csv.DictReader(csvfile1, delimiter=',')
    for row in reader1:
        featurekey = create_feature(args.domain_name, args.email, args.api_t, row['issuetype'], row['featurename'], row['summary'], row['description'], row['assignee'], row['labels'],row['reporterID'], row['key'], row['priority'])
        csvfile2 = open(args.csv2, 'r')
        reader2 = csv.DictReader(csvfile2, delimiter=',')
        for row in reader2:
            create_story(args.domain_name, args.email, args.api_t, row['issuetype'], row['project'], row['reporterID'], row['labels'], row['priority'], row['assignee'], featurekey, row['summary'], row['description'])

if __name__ == '__main__':
    run()




    