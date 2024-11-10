

class FHttps(object):

    DATA01 = {"p": "POST", "tv": "IGTV", "reel": "REELS", "stories": "STORIES"}

    DATA02 = r"^https://www\.instagram\.com/([A-Za-z0-9._]+/)?(p|tv|reel|stories)/([A-Za-z0-9\-_]*)"

class Okeys(object):

    DATA01 = "%(title,fulltitle,alt_title)s%(season_number& |)s%(season_number&S|)s%(season_number|)02d%(episode_number&E|)s%(episode_number|)02d.%(ext)s"
