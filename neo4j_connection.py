from neo4j import GraphDatabase

# Replace with your actual password if different
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "strongpassword123"))

# Function to run a basic query
def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return list(result)  # Fetch all records at once

# Example query to check connection
result = run_query("RETURN 'Hello, Neo4j!' AS message")
if result:
    print(result[0]['message'])  # Access the first record

# Close the driver after use
driver.close()
