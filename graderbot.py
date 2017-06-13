import praw
import signal, os, sys, marshal
from textstat.textstat import textstat

reddit = praw.Reddit("bot1")

subreddit = reddit.subreddit("pythonforengineers")

posts_replied_to = None

def signal_handler(signal, frame):
	if not posts_replied_to is None:
		with open("posts_replied_to.txt", "wb") as f:
			marshal.dump(posts_replied_to, f)
		print("Finished writing, now exiting")
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
	if not os.path.isfile("posts_replied_to.txt"):
		posts_replied_to = []
	else:
		with open("posts_replied_to.txt", "rb") as f:
			posts_replied_to = marshal.load(f)
	for comment in subreddit.stream.comments():
		if comment.body.lower() == "graderbot":
			if comment.id not in posts_replied_to:
				parent = comment.parent()
				parent_body = ""
				if type(parent) is praw.models.Submission:
					parent_body = parent.selftext
				else:
					parent_body = parent.body
				reply = "Grade Level of Writing is: " + textstat.text_standard(parent_body) + "\n\n"
				reply += "Number of characters: " + str(len(parent_body)) + "\n\n"
				words = parent_body.split(" ")
				reply += "Number of words: " + str(len(words)) + "\n\n"
				frequencies = {}
				for word in words:
					if word in frequencies:
						frequencies[word] += 1
					else:
						frequencies[word] = 1
				max = 0
				max_word = ""
				for word in frequencies:
					if frequencies[word] > max:
						max = frequencies[word]
						max_word = word
				reply += "Most common word: " + max_word
			
				comment.reply(reply)
				posts_replied_to.append(comment.id)

if __name__ == "__main__": main()





    
