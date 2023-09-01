# HarvestHub
Vegetable Supply Chain Management


### Services
1. Owner
2. Agent
3. Farmer
4. Retailer
5. HarvestHub Portal

### Setup
- Run `docker-compose up -d`
- Run 
  - `cd harvesthub_app`
  - `npm start`
- There are 4 UIs
  - `http:localhost:5003` - owner 
    - Where you can add the farmer/agent and add the commodities to the warehouse and see the statistics
  - `http:localhost:5002` - farmer 
    - He has single page which shows all his transactions.
  - `http:localhost:5001` - agent
    - He collects the bags from the farmers and send them to the owner in truck
  - `http:localhost:5004` and `http:localhost:3000` - retailer 
    - Where the retailer purchases the commodities from the owner

