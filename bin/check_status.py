######################################################################################################################
#
#
#       Very simple script that connects to splunk forwarders  to see if they are up or not
#
#       Forwarders can defined in $app/local/forwarders.conf, see $app/default/forwarders.conf for more information
#
#
#######################################################################################################################

            
import os, sys
import socket
import optparse
import re
import datetime,time
import splunk
import splunk.appserver.mrsparkle.lib.util as app_util
import splunk.clilib.cli_common as conf_tools

APPS_DIR = app_util.get_apps_dir()
APP_NAME = os.path.split(os.path.abspath(os.path.join(__file__, '../', '../')))[1]
APP_PATH = os.path.join(APPS_DIR, APP_NAME)

FORWARDER_CONF = os.path.join(APP_PATH, 'local', 'forwarders')

SPLUNK_HOME = os.environ.get('SPLUNK_HOME')


# to be safe, we will add the <app>/bin path to syspath so we can import any modules specific to this app
if not os.path.join(APPS_DIR, APP_NAME, 'bin') in sys.path:
   sys.path.append(os.path.join(APPS_DIR, APP_NAME, 'bin'))


def load_conf():
   
    global FORWARDER_CONF

    try:
         
        group_stanza = conf_tools.getConfStanza(FORWARDER_CONF, 'groups')
        groups = group_stanza['groupList'].split(',')
        # clean any extra whitespace out of our grouplist
        groups = map(lambda x: x.strip(), groups)

    except Exception, e:
        print e

    forwarders = {}
    for group in groups:
        forwarders[group] = get_forwarders(group) 

    return forwarders

def get_forwarders(group):

    try:
        host_groups = conf_tools.getConfStanza(FORWARDER_CONF, group)
    except Exception, e:
        print( "Unable to find group: %s, reason: %s" % ( group, e ) )
        return None

    #print host_groups
    
    hosts = []
    try:
        for k,v in host_groups.iteritems():

            if "," in v:
                multi_hosts = v.split(',')
                multi_hosts = map(lambda x: x.strip(), multi_hosts)
                for host in multi_hosts:
                    hosts.append(host)
            else:
                hosts.append(v)

    except Exception, e:
        print e


    return hosts


def check_forwarders(dict):

    for group, hosts in dict.iteritems():

        if not hosts:
            print "Issue processing group: %s, please verify naming and uniqueness" % ( group)
            continue

        for host in hosts:


            if ":" in host:
                host,port = host.split(':')
            else:
                port = 8089

            port = int(port)

            # Get a TCP socket
            s = socket.socket()
            # Timeout default = 10s  -- consider changing this if you have a large number of hosts to check
            socket.setdefaulttimeout(10)

            log_time = time.strftime("%Y-%m-%d %H:%M:%S %Z")


            try:
                hostname = socket.getfqdn(host)
                ip = socket.gethostbyname(host) 
            except socket.error, e:
                hostname = "no_name_found"
                ip = "no_ip_found"
                fqdn = "no_fqdn_found"
 

            try:
                s.connect( (host, port) )
                status = "up"
            except socket.error, e:
                status = "down"

            print '%s - host_tested="%s", fqdn="%s", ip="%s", port="%i", status="%s", group="%s"' % ( log_time, host, hostname, ip, port, status, group )

if __name__ == "__main__":

    my_forwarders = load_conf()

    check_forwarders(my_forwarders)

    sys.exit(0)

