## Before run:
`pip3 install -r requirements.txt`

## To run:
`flask --app main run`
### Then go to http://127.0.0.1:5000 in your browser

### Each time you refresh the page, all nonces are recalculated

# How to config:
## In config.py you can freely add/remove chains, like: "chain_name": "rpc"
## Public keys are in publics.txt file
## Order in cinfig.py matters, to change order in table, need to change the order in config file