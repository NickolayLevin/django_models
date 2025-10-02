from django import template

register = template.Library()


BAD_WORDS = ["плохое", "ругательство", "цензура"]

@register.filter(name="censor")
def censor(value):
    if not isinstance(value, str):
        return value

    for bad_word in BAD_WORDS:
        word_lower = bad_word.lower()
        value = value.replace(
            bad_word, 
            bad_word[0] + "*" * (len(bad_word) - 1)
        )
        value = value.replace(
            bad_word.capitalize(), 
            bad_word[0].upper() + "*" * (len(bad_word) - 1)
        )

    return value