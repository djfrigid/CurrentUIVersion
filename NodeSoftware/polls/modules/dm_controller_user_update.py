
# Module Name      : node_user_read
# Module Purpose   : modify the user of a node 
# Status           : Completed
# Parameters       : (node_user <node_user>)
# Returns          : ('node_user', 'update', node_user)

# Module Author    : Abubaker Omer 1846553
# Start Date       : 25/02/2020
# End Date         : 25/02/2020
# Hours Spent      : 0.15
from  dmcontroller import  dm_controller

def  dm_controller_node_user_update("user", "update", node_user):
	dm_controller("user", "update", node_user)






