from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError


def retrieve_users(server_name, domain_name):
    # Bind to the LDAP server
    server = Server(server_name, get_info=ALL)
    conn = Connection(server, auto_bind=True)
    conn.search(f'dc={domain_name},dc=local', '(objectclass=person)', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])

    # Get users
    users = list()
    for e in conn.entries:
        users.append(e.entry_attributes_as_dict)

def search_flag(users):
    for user in users:
        # print(f"User: {user['cn'][0]}") # DEBUG
        for k,v in user.items():
            for item in v:
                if type(item) == str and '404CTF{' in item:
                    print(f"    {k}: {v}")
        print()


# Main program

users = retrieve_users('51.77.110.239', 'ctfcorp')
search_flag(users)