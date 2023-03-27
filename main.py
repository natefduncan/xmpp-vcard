import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import xmpp
from vcard import parse_contacts

JID = os.getenv("JID")
JPASS = os.getenv("JPASS")
VCARD_PATH = os.getenv("VCARD_PATH")

if __name__ == "__main__":
    # Connect to XMPP 
    jid = xmpp.protocol.JID(JID)
    client = xmpp.Client(jid.getDomain(), debug=[])
    client.connect()
    client.auth(jid.getNode(), JPASS)

    # Read in vcard
    with open(Path(VCARD_PATH).expanduser(), "r") as f:
        vcard_str = f.read()
    contacts = parse_contacts(vcard_str)
    for contact in contacts:
       print(contact)

    # Update XMPP roster
    roster = client.getRoster()
    for jid in roster.getItems():
        print(jid)
