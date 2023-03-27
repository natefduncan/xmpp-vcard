from typing import NamedTuple, List
import re
import phonenumbers

class Contact(NamedTuple):
    name: str
    number: str

def parse_contacts(vcard_str: str) -> List[Contact]:
    NAME_RE = r'FN:(.+)'
    NUMBER_RE = r'TEL;.*type=pref:(.+)'
    token_specification = [
        ('START', r'BEGIN'),
        ('END', r'END'),
        ('NAME', NAME_RE),
        ('NUMBER', NUMBER_RE),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    name = None
    number = None
    for mo in re.finditer(tok_regex, vcard_str):
        kind = mo.lastgroup
        if kind == 'NAME':
            name = re.match(NAME_RE, mo.group('NAME')).group(1)
        elif kind == "NUMBER":
            number = phonenumbers.format_number(
                phonenumbers.parse(
                    re.match(
                        NUMBER_RE, 
                        mo.group('NUMBER')
                    ).group(1), 
                "US"), 
                phonenumbers.PhoneNumberFormat.E164
            )        
        elif kind == "END":
            yield Contact(name, number)
        else:
            continue
