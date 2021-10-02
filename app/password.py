from xkcdpass import xkcd_password as xp

def generate():
    wordfile = xp.locate_wordfile()
    mywords = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8)
    return xp.generate_xkcdpassword(mywords,numwords=4,delimiter='-')