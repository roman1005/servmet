from ldap3 import *
from ldap3.utils.log import set_library_log_detail_level, EXTENDED

from service_catalog.settings import LDAP_AUTH_URL, LDAP_AUTH_CONNECTION_PASSWORD, LDAP_AUTH_SEARCH_BASE, \
    LDAP_AUTH_CONNECTION_USERNAME, LDAP_AUTH_CONNECTION_PASSWORD





from ldap3 import Server, \
    Connection, \
    AUTO_BIND_NO_TLS, \
    SUBTREE, \
    ALL_ATTRIBUTES


def get_ldap_mail(firstName,lastName):

    ldap_mail=None


    ldap_entries=ldap_search(firstName,lastName)
    if len(ldap_entries)==1:
        ldap_mail=ldap_entries[0].mail

    return ldap_mail


def ldap_search(firstName,lastName):
    set_library_log_detail_level(EXTENDED)
    url = LDAP_AUTH_URL.split(':')
    ldapport = eval(url[2])
    server = url[1].replace('//', '')
    s = Server(server, port=ldapport, use_ssl=True)
    con = Connection(s, LDAP_AUTH_CONNECTION_USERNAME, LDAP_AUTH_CONNECTION_PASSWORD, auto_bind=AUTO_BIND_NO_TLS)
    print(con)  # to check the connection status
    con.search(search_base=LDAP_AUTH_SEARCH_BASE,
               search_filter='(&(givenName=' + firstName + ')  (sn=' + lastName + '))',
               search_scope=SUBTREE,
               attributes=ALL_ATTRIBUTES,
               get_operational_attributes=True)
    return con.entries