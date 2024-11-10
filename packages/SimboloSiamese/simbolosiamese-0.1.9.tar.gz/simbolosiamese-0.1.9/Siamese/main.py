import re
from typing import Dict, Any

class BurmeseConverter:
    def __init__(self):
        self.font_dictionary = {
                    '္': '်', '်': 'ျ', 'ျ': 'ြ', 'ြ': 'ွ', 'ွ': 'ှ', 'ႆ': 'ဿ', 'ဳ': 'ု', 'ဴ': 'ူ', 'ဿ': 'ူ',
                    '၀': 'ဝ', '၎': '၎င်း', 'ၚ': 'ါ်', 'ၠ': '္က', 'ၡ': '္ခ', 'ၢ': '္ဂ', 'ၣ': '္ဃ', 'ၥ': '္စ',
                    'ၦ': '္ဆ', 'ၧ': '္ဆ', 'ၨ': '္ဇ', 'ၩ': '္ဈ', 'ၪ': 'ဉ', 'ၫ': 'ည', 'ၬ': '္ဋ', 'ၭ': '္ဌ',
                    'ၮ': 'ဍ္ဍ', 'ၯ': 'ဍ္ဎ', 'ၰ': '္ဏ', 'ၱ': '္တ', 'ၲ': '္တ', 'ၳ': '္ထ', 'ၴ': '္ထ', 'ၵ': '္ဒ',
                    'ၶ': '္ဓ', 'ၷ': '္န', 'ၸ': '္ပ', 'ၹ': '္ဖ', 'ၺ': '္ဗ', 'ၻ': '္ဘ', 'ၼ': '္မ', 'ၽ': 'ျ',
                    'ၾ': 'ြ', 'ၿ': 'ြ', 'ႀ': 'ြ', 'ႁ': 'ြ', 'ႂ': 'ြ', 'ႃ': 'ြ', 'ႄ': 'ြ', 'ႅ': '္လ', 'ႇ': 'ှ',
                    'ႈ': 'ှု', 'ႉ': 'ှူ', 'ႊ': 'ွှ', 'ႎ': 'ိံ', 'ႏ': 'န', '႐': 'ရ', '႑': 'ဏ္ဍ', '႒': 'ဋ္ဌ',
                    '႓': '္ဘ', '႔': '့', '႕': '့', '႖': '္တွ', '႗': 'ဋ္ဋ', 'ၤ': 'င်္'
                }

    def zawgyi_to_unicode(self, text):
        # Replace characters based on font dictionary
        char_list = list(text)
        for i, char in enumerate(char_list):
            if char in self.font_dictionary:
                char_list[i] = self.font_dictionary[char]

        # Join modified characters back into a string
        converted_text = "".join(char_list)

        # Regular expression pattern for ordering characters in Unicode
        uni_pattern = r"(ေ)?(ြ)?([က-ဩဿၐ-ၕၚ-ၝၡၥၦၮ-ၰၵ-ႁႎ႐-႙႞႟])(ွ)?(ှ)?(ျ)?(င်္)?(ွ)?(ှ)?(ာ)?(း)?(္[က-ဘမလ])?"

        # Reorder characters to match Unicode standard
        result = re.sub(uni_pattern, r"\7\3\12\2\6\8\4\9\5\1\10\11", converted_text)

        return result

    def syllable_tokenization(self, option: int, user_input: str) -> str:
        """
        Process Burmese text by tokenizing and normalizing it.
        
        :param option: Processing option, 1 to include virama mark, others without
        :param user_input: Text to be processed
        :return: Processed text with or without virama mark
        """
        try:
            if option == 1:
                processed_input = re.sub(r"([က-အ|ဥ|ဦ](င်္|[က-အ][ှ]*[့း]*[်]|([က-အ]္)|[ါ-ှႏꩻ][ꩻ]*){0,}|.)", r"\1 ", user_input)
                processed_input = re.sub(r"(([က-အ])္ ([က-အ]))", r"\2် \3", processed_input)
                return f"With the virama mark: {processed_input}"
            else:
                processed_input = re.sub(r"([က-အ|ဥ|ဦ](င်္|[က-အ][ှ]*[့း]*[်]|([က-အ]္)|[ါ-ှႏꩻ][ꩻ]*){0,}|.)", r"\1 ", user_input)
                return f"Without the virama mark: {processed_input}"
        except Exception as e:
            raise Exception(f"An error occurred during text processing: {e}")

    def burmese_to_romanization(self, text: str) -> str:
        """
        Convert Burmese text to Romanized form.
        
        :param text: Burmese text input
        :return: Romanized text output
        """
        burmese_to_roman: Dict[str, str] = {
        'က': 'k', 'ခ': 'K', 'ဂ': 'g', 'ဃ': 'G', 'င': 'c', "၏": "E", "၍": "rx", "၌": "Nx", "င်္": "f",
        'စ': 's', 'ဆ': 'S', 'ဇ': 'z', 'ဈ': 'Z', "ဉ": "q", 'ည': 'Q', "ဋ": "tx", "ဌ": "Tx", "ဍ": "dx", "ဎ": "Dx", "ဏ": "nx",
        "ရ": "r", "ဓ": "D", "တ": "t", "ထ": "T", "ဒ": "d", "န": "n", "ပ": "p", "ဖ": "P", "ဗ": "b", "ဘ": "B", "မ": "m",
        "ယ": "y", "ဝ": "w", "သ": "j", "ဟ": "h", "အ": "a", 'လ': 'l', "ဠ": "lx", "ဣ": "ix", "ဤ": "Ix", "၊": "/", "။": "//", "ဥ": "Ux", "ဦ": "OO", "ဧ": "ax", "ဩ": "O", "ဪ": "OR", "ါ": "A", "ာ": "A", "ိ": "i", "ီ": "I","ေ": "e",
        "ု": "u", "ူ": "U", "ဲ": "L", "ံ": "N", "့": ".", "း": ":", "ျ": "Y", "ြ": "R", "ွ": "W", "ှ": "H","၎":"4",
        "ဿ": "jx", "်": ""
    }

        try:
            text = text.strip()
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r' ', ',', text)
            text = re.sub(r',+', ',', text)

            # Tokenization for Romanization
            text = re.sub(r"([က-အ|ဥ|ဦ](င်္|[က-အ][ှ]*[့း]*[်]|([က-အ]္)|[ါ-ှႏꩻ][ꩻ]*){0,}|.)", r"\1 ", text)
            text = re.sub(r"(([က-အ])္ ([က-အ]))", r"\2် \3", text)

            rules = [
                (re.compile(r'ကျွန် မ '), "q'm "),
                (re.compile(r'ကျွန် တော် '), "q't "),
                (re.compile(r'ကျွန်ပ် '), 'Q" '),
                (re.compile(r'ဏ် ဍ'), "F")
            ]

            for rule in rules:
                text = rule[0].sub(rule[1], text)
            text = re.sub(r'([‌ေ][က-ဪ]*[ာါ]*[်])', r'\1F', text)
            
            # Romanization conversion
            for burmese_char, roman_char in sorted(burmese_to_roman.items(), key=lambda x: len(x[0]), reverse=True):
                text = text.replace(burmese_char, roman_char)

            # Clean-up
            text = re.sub(r' ,', ",", text)
            return text
        except Exception as e:
            raise Exception(f"An error occurred during Burmese_to_Romanization: {e}")

    def romanization_to_burmese(self,text):
        
        
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

            try:
                def roman_to_special_words(text):
                    reverse_rules = [
                        (re.compile(r"q'm"), 'ကျွန် မ '),
                        (re.compile(r"q't"), 'ကျွန် တော် '),
                        (re.compile(r'Q"'), 'ကျွန်ုပ် '),
                    ]
                    for rule in reverse_rules:
                        text = rule[0].sub(rule[1], text)
                    return text

                def romanize_burmese(text):
                    romanized_text = text
                    for burmese_char, roman_char in sorted(roman_to_burmese.items(), key=lambda x: len(x[0]), reverse=True):
                        romanized_text = romanized_text.replace(burmese_char, roman_char)
                    return romanized_text
                
                transformed_text = ""
                text = roman_to_special_words(text)
                for word in text.split(" "):
                    word = roman_to_special_words(word)
                    word = romanize_burmese(word)
                    word = re.sub(r"([ခဂငဒဝပ]ေ*)ာ", r"\1ါ", word)
                    word = re.sub(r"([က-အ])(.*)([က-အ])", r"\1\2\3်", word)
                    word = re.sub(r"််", "်", word) 
                    
                    transformed_text += word 
                    transformed_text = re.sub(r"၎ငး", "၎င်း", transformed_text)
                return re.sub(r',', " ", transformed_text)

            except Exception as e:
                return f"An error occurred during Romanization_to_Burmese: {e}"

# Example usage of the class
if __name__ == "__main__":
    converter = BurmeseConverter()

    # Example: Zawgyi to Unicode
    zawgyi_text = "သီဟိုဠ္မွ ဉာဏ္ႀကီးရွင္သည္ အာယုဝၯနေဆးၫႊန္းစာကို ဇလြန္ေဈးေဘး ဗာဒံပင္ထက္ အဓိ႒ာန္လ်က္ ဂဃနဏဖတ္ခဲ့သည္။"
    try:
        unicode_output = converter.zawgyi_to_unicode(zawgyi_text)
        print("Unicode Output:", unicode_output)
    except Exception as e:
        print(f"Error in Zawgyi to Unicode conversion: {e}")

    # Example: Burmese Romanization
    burmese_text = "လေကြောင်းလိုင်း ခရီးစဉ်အမှတ် ၂၂၈၃ သည် ဆော်ပိုလိုမြို့ လူနေရပ်ကွက်ပေါ်သို့ ပျက်ကျခဲ့ပြီး လိုက်ပါလာသူ ၆၂ ဦးစလုံး သေဆုံးခဲ့သည်။"
    try:
        romanized_output = converter.burmese_to_romanization(burmese_text)
        print("Romanized Output:", romanized_output)
    except Exception as e:
        print(f"Error in Burmese Romanization: {e}")
    
    # Example: Romanization Burmese
    burmese_text = "le kReAc: liuc:, K rI: sq a mHt, ၂ ၂ ၈ ၃, jQ, SeAF piu liu mRiu., lU ne rp kWk peAF jiu., pYk kY KL. pRI:, liuk pA lA jU, ၆ ၂, OO: s luN:, je SuN: KL. jQ // "
    try:
        burmese_output = converter.romanization_to_burmese(burmese_text)
        print("Burmese Output:", burmese_output)
    except Exception as e:
        print(f"Error in Romanization Burmese: {e}")


