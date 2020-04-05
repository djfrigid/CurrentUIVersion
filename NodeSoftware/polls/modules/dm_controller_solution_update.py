# Module Name      : dm_controller_solution_update
# Module Purpose   : create a solution 
# Status           : Completed
# Parameters       : (solution <solution>)
# Returns          : (‘solution’, ‘update’, solution)
#
# Module Author    : Chenyang Liu C1965163 
# Start Date       : 01/03/2020
# End Date         : 01/03/2020
# Hours Spent      : 1h
from  dmcontroller import  dm_controller
def dm_controller_solution_update(solution):
      try:
      	dm_controller(solution,update,solution)
      	return True
      except:
      	return False