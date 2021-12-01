#Written by Dan Scott Oct '21, Modified by Max Van Raden 11/05/21

#USAGE: [0]scriptname [1]infile [2]outfile [3]sub1 sub2 sub3 etc

import json
from os import write
import time
import sys
from datetime import datetime
import nltk

try:
    inFile = sys.argv[1] #first argument after script name must be present
    outFile = sys.argv[2] #second argument after script name must be present
    sub = sys.argv[3:] #must be at least one subreddit
except:
    print("Error. Not enough command line arguments.")
    exit()

def main():
    kept_comments = []
    kept_count = 0
    
    slur_list = get_slurs()
    #slur_count = 0
    
    read_count = 0
    write_count = 0
    
    #subreddit_comment_counts = {} #create empty dictionary
    subreddit_comment_counts = []
    
    for item in sub:
        #subreddit_comment_counts.update({item: 0}) #add object for every subreddit from sys.argv
        subreddit_comment_counts.append({'subreddit': item, 'comment_count': 0, 'slurs_found': 0})
        #print(subreddit_comment_counts)
    
    print("Scanning {} for comments from selected subreddits...\n".format(inFile))
    
    with open(inFile) as f_in:
        for line in f_in:
            comment = json.loads(line)
            read_count += 1
            for subreddit in sys.argv[3:]: #loop through the subreddits for each comment to check for a match
                subreddit_comments = 0
                slur_count = 0
                if comment['subreddit'] == subreddit.lower():
                    if comment['score'] >= 5: # at least a score of 5 to indicate community approval
                        spaceCount = 0
                        comment_tokens = nltk.word_tokenize(comment['body'])
                        #print(comment_tokens)
                        #for c in comment['body']:
                            #if c == ' ':
                                #spaceCount += 1
                        #if spaceCount >=5: # at least 6 words in the comment to indicate substance
                        if len(comment_tokens) > 6:
                            comment_scrub = {'subreddit': comment['subreddit'], 
                                             'score': comment['score'], 
                                             'body': comment['body'] 
                                             #'controversiality': comment['controversiality'], 
                                             #'stickied': comment['stickied']
                                             }
                            slur_count += slur_check(comment_tokens, slur_list)
                            #slur_count += slur_check(comment_scrub['body'], slur_list)
                            kept_comments.append(comment_scrub) 
                            subreddit_comments += 1
                for metadata in subreddit_comment_counts:
                    #print(metadata)
                    if metadata['subreddit'] == subreddit:
                        metadata['comment_count'] += subreddit_comments
                        metadata['slurs_found'] += slur_count
                #subreddit_comment_counts[subreddit] += subreddit_comments
                #subreddit_comment_counts[slurs_found] += slur_count
                #print('Subreddit comment count for {}: {}'.format(subreddit, subreddit_comment_counts))
                #print('Slur count for {}: {}'.format(subreddit, slur_count))
    f_in.close()

    with open(outFile, "w", encoding = 'utf-8') as f_out:
        for comment in kept_comments:
            f_out.write(json.dumps(comment) + '\n')
            write_count += 1
    f_out.close()
    
    metadata_file = 'sub_meta_data.json'
    
    with open(metadata_file, "w", encoding = 'utf-8') as meta_out:
        for item in subreddit_comment_counts:
            meta_out.write(json.dumps(item) + '\n')
            #meta_out.write(json.dumps({'subreddit': item,
                                       #'comments_read': subreddit_comment_counts[item],
                                       #'slurs_found': 'placeholder value'}) + '\n')
    meta_out.close()
    
# def write_meta(f_name, metadata):
    # with open(metadata_file, "w", encoding = 'utf-8') as meta_out:
        # for item in subreddit_comment_counts:
            # meta_out.write(json.dumps({'subreddit': item,
                                       # 'comments_read': subreddit_comment_counts[item],
                                       # 'slurs_found': 'placeholder value'}) + '\n')
    # meta_out.close()
    
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
    
def slur_check(words, slur_list):
    #slurs = get_slurs()
    slur_count = 0
    
    #tokens = nltk.word_tokenize(comment)
    
    for word in words:
        for slur in slur_list:
            #rint(word)
            #print(slur[0])
            if word == slur[0]:
                slur_count += 1
    #if slur_count > 0:
        #print(words)
        #print(slur_count)
    return slur_count
    
    
if __name__ == "__main__":
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)
    start_time = time.time()
    main()
    print("Completed scan in %s seconds" % (time.time() - start_time))