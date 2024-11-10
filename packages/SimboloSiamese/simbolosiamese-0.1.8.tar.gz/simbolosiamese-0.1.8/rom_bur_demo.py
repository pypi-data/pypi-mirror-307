import re
import streamlit as st

burmese_to_roman = {
    'က': 'k', 'ခ': 'K', 'ဂ': 'g', 'ဃ': 'G', 'င': 'c', "၏": "E", "၍": "rx", "၌": "Nx", "င်္": "f",
    'စ': 's', 'ဆ': 'S', 'ဇ': 'z', 'ဈ': 'Z', "ဉ": "q", 'ည': 'Q', "ဋ": "tx", "ဌ": "Tx", "ဍ": "dx", "ဎ": "Dx", "ဏ": "nx",
    "ရ": "r", "ဓ": "D", "တ": "t", "ထ": "T", "ဒ": "d", "န": "n", "ပ": "p", "ဖ": "P", "ဗ": "b", "ဘ": "B", "မ": "m",
    "ယ": "y", "ဝ": "w", "သ": "j", "ဟ": "h", "အ": "a", 'လ': 'l', "ဠ": "lx", "ဣ": "ix", "ဤ": "Ix", "်":"F"
}

burmese_to_roman.update({
    "၊": "/", "။": "//", "ဥ": "Ux", "ဦ": "OO", "ဧ": "ax", "ဩ": "O", "ဪ": "OR", "ါ": "A", "ာ": "A", "ိ": "i", "ီ": "I","ေ": "e",
    "ု": "u", "ူ": "U", "ဲ": "L", "ံ": "N", "့": ".", "း": ":", "ျ": "Y", "ြ": "R", "ွ": "W", "ှ": "H","၎":"4",
    "ဿ": "jx"
})

roman_to_burmese = {v: k for k, v in burmese_to_roman.items()}

def process_burmese_text(text):
    # Step 1: Define special word transformation rules
    reverse_rules = [
        (re.compile(r"q'm "), 'ကျွန် မ '),
        (re.compile(r"q't "), 'ကျွန် တော် '),
        (re.compile(r'Q" '), 'ကျွန်ပ် '),
    ]

    # Initialize the result
    output_text = ""

    # Process each word in the text
    for word in text.split(" "):
        # Apply special word transformations
        for rule in reverse_rules:
            word = rule[0].sub(rule[1], word)

        # Convert Romanized text to Burmese
        for burmese_char, roman_char in sorted(roman_to_burmese.items(), key=lambda x: len(x[0]), reverse=True):
            word = word.replace(burmese_char, roman_char)

        # Additional transformations for accurate Burmese script formation
        word = re.sub(r"([ခဂငဒဝပ]ေ*)ာ", r"\1ါ", word)  # Replace 'ော' with 'ါ' for specific syllables
        word = re.sub(r"([က-အ])(.*)([က-အ])", r"\1\2\3်", word)  # Add '်' for syllable formation

        # Append processed word to output
        output_text += word

    return output_text

text_input = st.text_input("Romanization to Burmese")
st.write("Burmese output: ", process_burmese_text(text_input))
