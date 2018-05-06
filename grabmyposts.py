import json
import datetime
import re
import io

# I don't want any of my posts to groups to show up, because that feels more private
# and some of the groups I belong to are private/secret
def posted_to_group(entry):
    group_post = False
    if ('title' in entry):
        title = entry['title']
        if re.search('posted in', title):
            group_post = True
    return group_post

# I don't want any of my posts to other people's timelines to show up because
# those felt like personal direct messages before messenger existed.
def posted_to_another_timeline(entry):
    another_timeline = False
    if ('title' in entry):
        title = entry['title']
        if re.search('timeline', title):
            another_timeline = True
    return another_timeline

def is_birthday_post(post_text):
    birthday_post = False
    if re.search('birthday', post_text, re.IGNORECASE):
        birthday_post = True
    return birthday_post

#with open('your_posts.json', 'r', encoding="utf-8").read() as fp:
with io.open('your_posts.json', 'r', encoding="utf-8") as fp:
    json_dict = json.load(fp)
    for fb_element in json_dict:
        if not posted_to_group(fb_element) and not posted_to_another_timeline(fb_element):
            if 'data' in fb_element:
                data = fb_element['data'][0]
                if 'post' in data and not is_birthday_post(data['post']):
                    timeline_post = data['post']
                    print timeline_post.encode('utf-8')
                    print datetime.datetime.fromtimestamp(fb_element['timestamp'])

#prettydate = datetime.datetime.fromtimestamp(timestamp)

# 1) There's no indication when a post is on my own timeline or posted on another person's timeline.
#    yes there is, I have to look at the title of a post
# 2) How can I hide the posts I made to private groups?
#    ok.. just exclude data with titles including the phrase "posted in"
# 3) I'm going to exclude lines containing "birthday(s)" for now.
