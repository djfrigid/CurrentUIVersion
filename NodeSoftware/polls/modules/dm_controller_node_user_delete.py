# Module Name      : node_user_read
# Module Purpose   : delete user from a node 
# Status           : Completed
# Parameters       : (node_user <node_user>)
# Returns          : ('node_user', 'delete', node_user)

# Module Author    : Abubaker Omer 1846553
# Start Date       : 24/03/2020
# End Date         : 24/03/2020
# Hours Spent      : 0.15

from  dmcontroller import  dm_controller

def  dm_controller_node_user_delete("user", "delete", node_user):
	dm_controller("user", "delete", node_user)




