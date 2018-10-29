"""Welcome to our junk drawer"""
def emoji_parser(text):
    # check to see if the text starts with : and ends with :
    if text.startswith(':') and text.endswith(':'):
        return (text.split(':')[1])
    else:
        return text

