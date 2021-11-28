#Written by Dan Scott Oct '21, Modified by Max Van Raden 11/05/21

#USAGE: [0]scriptname [1]infile [2]outfile [3]sub1 sub2 sub3 etc

import json
from os import write
import time
import sys
from datetime import datetime

try:
    inFile = sys.argv[1] #first argument after script name must be present
    outFile = sys.argv[2] #second argument after script name must be present
    sub = sys.argv[3:] #must be at least one subreddit
except:
    print("Error. Not enough command line arguments.")
    exit()

def main():
    kept_comments = []
    slurs = get_slurs()
    read_count = 0
    write_count = 0
    subreddit_comment_counts = {}
    slur_counts = {}
    for item in sub:
        subreddit_comment_counts.update({item: 0})
    
    print("Scanning {} for comments from selected subreddits...\n".format(inFile))
    
    #should slur check be performed on data as it's being read? or on resulting comment file?
    #total subreddit comments vs qualified comments
    
    with open(inFile) as f_in:
        for line in f_in:
            comment = json.loads(line)
            read_count += 1
            for subreddit in sys.argv[3:]: #loop through the subreddits for each comment to check for a match
                subreddit_comments = 0
                if comment['subreddit'] == subreddit.lower():
                    if comment['score'] >= 5: # at least a score of 5 to indicate community approval
                        spaceCount = 0
                        for c in comment['body']:
                            if c == ' ':
                                spaceCount += 1
                        if spaceCount >=5: # at least 6 words in the comment to indicate substance
                            comment_scrub = {'subreddit': comment['subreddit'], 
                                             'score': comment['score'], 
                                             'body': comment['body'] 
                                             #'controversiality': comment['controversiality'], 
                                             #'stickied': comment['stickied']
                                             }
                            kept_comments.append(comment_scrub) 
                            subreddit_comments += 1
                subreddit_comment_counts[subreddit] += subreddit_comments
    f_in.close()

    with open(outFile, "w", encoding = 'utf-8') as f_out:
        for comment in kept_comments:
            f_out.write(json.dumps(comment) + '\n')
            write_count += 1
    f_out.close()
    
    metadata_file = 'sub_meta_data.txt'
    
    with open(metadata_file, "w", encoding = 'utf-8') as meta_out:
        for item in subreddit_comment_counts:
            meta_out.write(json.dumps({item: subreddit_comment_counts[item]}) + '\n')
    meta_out.close()
    
def get_slurs():
    slur_file = 'slurs.txt' #incorporate as command line argument?
    slur_list = []

    with open(slur_file) as slur_data:
        for line in slur_data:
            str = line.strip('\n()')
            str = str.split(',')
            slur_list.append(str)
    slur_data.close()
    return slur_list
    
    
if __name__ == "__main__":
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)
    start_time = time.time()
    main()
    print("Completed scan in %s seconds" % (time.time() - start_time))