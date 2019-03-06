#!/usr/bin/env python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","hrapp.settings")
from .models import Link
def rank_all():
	for link in Link.votecount.all():
		link.set_rank()


import time

def show_all():

	print(("\n").join(%10s %0.2f %(l.title,l.rank_score,)for l in Link.votecount.all()))
	print("-----\n\n\n")

if __name__ == "__main__":
	while 1:
		print("---")
		rank.all()
		show.all()
		time.sleep(5)