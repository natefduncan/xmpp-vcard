import os
from dotenv import load_dotenv
load_dotenv()

import xmpp

JID = os.getenv("JID")
JPASS = os.getenv("JPASS")

if __name__ == "__main__":
    jid = xmpp.protocol.JID(JID)
    client = xmpp.Client(jid.getDomain(), debug=[])
    client.connect()
    client.auth(jid.getNode(), JPASS)
    roster = client.getRoster()
    for jid in roster.getItems():
        print(jid)
