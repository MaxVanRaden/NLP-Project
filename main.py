#Written by Dan Scott Oct '21, Modified by Max Van Raden 11/05/21

#USAGE: [0]scriptname [1]infile [2]outfile [3]sub1 sub2 sub3 etc

import json
from os import write
import time
import sys
from datetime import datetime


#move this to a command line argument at some point?
sub_count = 0

try:
    inFile = sys.argv[1] #first argument after script name must be present
    outFile = sys.argv[2] #second argument after script name must be present
    sub = sys.argv[3] #must be at least one subreddit
except:
    print("Error. Not enough command line arguments.")
    exit()



class Comment:
    def __init__(self, subreddit, body):
        self.subreddit = subreddit
        self.body = body
        #we can add more class variables as we need

def main():
    #sname = input("Enter a subreddit: ")
    #outFile = sname + 'Comments.txt'
    comments = []
    read_count = 0
    write_count = 0
    subreddit_comment_counts = []
    
    print("Scanning {} for comments from selected subreddits...\n".format(inFile, sname))
    
    with open(inFile) as f_in:
        for line in f_in:
            comment = json.loads(line)
            read_count += 1
            for i in sys.argv[3:]: #loop through the subreddits for each comment to check for a match
                subreddit_comments = 0
                if comment['subreddit'] == sys.argv[i].lower(): #maybe use regular expression of sname here to account for casing issues?
                    if comment['score'] >= 5: # at least a score of 5 to indicate community approval
                        spaceCount = 0
                        for c in comment['body']:
                            if c == ' ':
                                spaceCount += 1
                        if spaceCount >=5: # at least 6 words in the comment to indicate substance
                            json.dump(comment, outFile)
                            subreddit_comments += 1
                            write_count += 1
                subreddit_comment_counts.append((sys.argv[i], subreddit_comments))


                 #comments.append(Comment(comment['subreddit'], comment['body']))
    f_in.close()

#    with open(outFile, "w", encoding = 'utf-8') as f_out:
#        for comment in comments:
#            f_out.write("Subreddit: {}\nComment: {}\n".format(comment.subreddit, comment.body))
#            write_count += 1
#    f_out.close()
    print("Success! Subreddit {} has {} comments out of {} total\n".format(sname, write_count, read_count))
    
if __name__ == "__main__":
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)
    start_time = time.time()
    main()
    print("Completed scan in %s seconds" % (time.time() - start_time))