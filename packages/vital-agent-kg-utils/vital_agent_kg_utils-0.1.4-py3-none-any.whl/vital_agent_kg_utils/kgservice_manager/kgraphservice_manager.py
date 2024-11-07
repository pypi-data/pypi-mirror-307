

# wrapper around:
# vital_agent_rest_client and vital_agent_rest_resource_client
# for updating kgraph data with create, update, delete
# and read, search, and query via vital_agent_rest_resource_client

# for changes, these are made first to vital_agent_rest_client
# and upon success, changes make to kgservice via vital_agent_rest_resource_client

# parameter passed to vital_agent_rest_client such that it does not write such changes
# via vital_agent_rest_resource_client to the graph and vector db

# the purpose is to allow the agent to "see" the changes its making to rest_resource
# immediately since changes are being made via its client, which may have some caching
# and to not make vital_agent_rest a bottleneck

# such changes should be in the namespace of the current user (account namespace) interacting
# with the agent, so other accounts wouldn't being seeing them anyway

# changes made to vital_agent_rest_client eventually get replicated into the
# graph and vector dbs acting as indexes of this, and we want to allow that to lag behind
# if the updates are already in the graph and vector db then no net change

