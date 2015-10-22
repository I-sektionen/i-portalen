__author__ = 'jonathan'
import markdown as md
import re
def markdown_to_html(text):
    text = re.sub(r'([#]{2,})', '#', text)
    text = re.sub(r'([=]{3,})', '', text)
    text = re.sub(r'([-]{3,})', '', text)
    text = re.sub(r'([`])', '', text)
    text = md.markdown(text, safe_mode='escape', output_format='html5').replace("<hr>", "")
    return text