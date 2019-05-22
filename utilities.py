import re

# Filtering is removing characters
# Filtering is done immediately upon receiving the data before sending it
# to the database
# To filter generic input we can create a filter_input function using the
# the strip() function which removes empty space before and after data
# The re.sub() method which can be used to remove unwanted characters
def filter_input(string, special_characters):
    strip_space = string.strip()
    strip_tags = re.sub(r"(<[^>]*?>)", "", strip_space)
    strip_chars = re.sub(special_characters, "", strip_tags)
    return strip_chars

# To filter and format names specifically we would probably want to remove
# anything other than letters
# We can also format names with capital first letters and the rest lowercase
def format_name(name):
    filtered = filter_input(name, r"([^a-zA-Z0-9 ]+)")
    formatted = filtered.lower().title()
    return formatted

# Converting characters from symbols into code which inserts those symbols,
# also known as "escape characters" is known as escaping
# Escaping should be done AFTER retreiving the data from the database
# once you are displying it in final format such as HTML
def escape_html(string):
	neutralize_amp = string.replace("&", "&amp;")
	neutralize_quote = neutralize_amp.replace('"', "&quot;")
	neutralize_lt = neutralize_quote.replace("<", "&lt;")
	neutralize_gt = neutralize_lt.replace(">", "&gt;")
	return neutralize_gt;
