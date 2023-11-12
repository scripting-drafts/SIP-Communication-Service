# A SIP Communication Service

Requirement - Add Client IP Address Server and Client Sides  
Server: Run data_handler  
Client: Run conversational  

## How it works

**Client**: Listens voice -> Translates to text -> Relays text  
**Server**: Feeds text to Neural Network (microsoft/GODEL-v1_1-large-seq2seq)-> arbitrarily gets summarized (google/pegasus-xsum) -> logging proceeds -> Answers get relayed  
**Client**: Speaks answers out loud  

### TODO

 - Make the generation of Files available to models that require 'knowledge' logging - Autogenerate  
 - _Encrypt_ UDP  
 - Evolve from Backbone Edge Computing to Cloud Native  
