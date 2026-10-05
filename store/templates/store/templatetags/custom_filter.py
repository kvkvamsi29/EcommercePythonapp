from django import template
import re

register = template.Library()

@register.filter(name="highlight")
def highlight(text, search):
    if not text or not search:
        return text

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return pattern.sub(
        lambda match: f"<mark>{match.group()}</mark>",
        text
    )
