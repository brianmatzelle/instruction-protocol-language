# Connect with people that work at docker by contributing to their personal github projects
1. get a list 
2. write a dockerized LLM integrated program
  context: each container is given a linkedin username/pfp argument.
  a. first, go to linkedin
    i. then, find people that work at docker
  b. then, use perplexity/grok to search the web to (see if they have a personal github account)
    i. if so, scan the person's projects, (find an easy change) *use GitHub MCP*
    ii. run an MCP workflow with claude to
      - clone the repo
      - make a small change
      - test the output to make sure it works
      - create a pull request
      - commit and push the changes
  d. TODO