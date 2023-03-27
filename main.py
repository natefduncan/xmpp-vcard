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

    # Update XMPP roster
    roster = client.getRoster()
    jids = roster.getItems()
    for contact in contacts:
        new_jid = f"{contact.number}@cheogram.com"
        if new_jid not in jids:
            roster.setItem(new_jid, name=contact.name)
            roster.Subscribe(new_jid)
            roster.Authorize(new_jid)
