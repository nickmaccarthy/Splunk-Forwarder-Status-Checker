# Splunk Forwarder Checker #

What is this?
---------------------------------
A very simple splunk app that will connect to splunk forwarders on thier management port to see if they are up or not.

This is very useful for adding a layer of physical monitor Splunks deployment monitor does not offer currently.

How do I set it up?
---------------------------------
Define your forwarders in $app/local/forwarders.conf ( see $app/default/forwarders.conf for details ), and restart Splunk.  

Note will create an index called "host_monitor" where these events will go by default.  If that needs to be different, remove indexes.conf from default before you install the app. Additionally if you are in a distributed indexing envrionment, this index will need to created on your indexers. 

Also Note that if you a more than 5 minute interval, override the default inputs.conf in $app/local

What do I do now?
---------------------------------
After you have it up and running, define some alerts for when your forwarders go down ( status="down" ). 


### Author: Nick MacCarthy
### Date: 10/2013
### Email: nickmaccarthy@gmail.com

