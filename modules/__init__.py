#put all your modules here or they won't work nicely!

import modules.sample as sample
import modules.select_client as select_client
import modules.list_connections as list_connections
import modules.listen as listen
import modules.kill as kill

def get_modules():
     return [sample, select_client, list_connections, listen, kill]

