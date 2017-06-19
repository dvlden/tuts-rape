### TutsRape
##### ScRape Tutsplus courses, so you can continue watching offline.

---

# Deprecated!
Tutsplus made few other changes that I recently discovered.
1. They disable login form and enable it with JS when page is fully loaded or after a short delay. This is fixable via Selenium WebDriver Wait package.
2. They no longer have `<source>` that contains the video link of the Wistia, but now instead contain `<video src="" />` direct embed. The issue here is not that minor change, but the `blob` url that cannot be converted back to original address. I don't have solution to this, so I am deprecating this repository. If I figure out the solution someday, I will update the README file as well.

[Tutsplus.com](https://tutsplus.com/) *(envato tuts+)* - is paid subscription service, that allows you to watch premium courses online. As you may have noticed, they do allow you to download LQ videos when you're on smartphone or tablet, but they do not allow you to download those HQ (720p HD) on your computer, for some reason...

**TutsRape** has been made to solve this, but also to automatize the process so that you can watch those videos offline later-on.

#### How to use TutsRape?
*Prerequisites*
- You must be subscribed to [Tutsplus.com](https://tutsplus.com/pricing)
- You must have Python 3 and pip installed

*Afterwards*
- Clone this repository
- Open Terminal and navigate to the folder of TutsRape
- Install dependencies: `pip install -r requirements.txt`
- Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your OS
- Open `config.yaml` and setup required configuration
- Run TutsRape: `python init.py`

**That's it. Do something else meanwhile or take a coffee break!**

__Please, do not use TutsRape to leak Tutsplus videos somewhere else for free... Private/Personal use only, if you must watch the videos offline for some reason.__
