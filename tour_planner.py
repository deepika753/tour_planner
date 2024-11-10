from neo4j_connection import run_query

def get_all_locations():
    query = "MATCH (l:Location) RETURN l.name AS location"
    result = run_query(query)
    for record in result:
        print(record['location'])

def get_routes_from_location(location_name):
    query = """
    MATCH (l:Location {name: $location_name})-[:CONNECTED_TO]->(r:Location)
    RETURN r.name AS destination, r.distance AS distance, r.time AS time
    """
    result = run_query(query, location_name=location_name)
    for record in result:
        print(f"Destination: {record['destination']}, Distance: {record['distance']} km, Time: {record['time']} hours")

def get_recommendations(location_name):
    query = """
    MATCH (l:Location {name: $location_name})-[:HAS_RECOMMENDATION]->(r:Recommendation)
    RETURN r.recommended_by AS recommended_by, r.reason AS reason
    """
    result = run_query(query, location_name=location_name)
    for record in result:
        print(f"Recommended by: {record['recommended_by']}, Reason: {record['reason']}")

def start_cli():
    print("Welcome to the Tour Planner!")
    while True:
        print("\nChoose an option:")
        print("1. View all locations")
        print("2. Get routes from a location")
        print("3. Get recommendations for a location")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            get_all_locations()
        elif choice == "2":
            location = input("Enter the location: ")
            get_routes_from_location(location)
        elif choice == "3":
            location = input("Enter the location: ")
            get_recommendations(location)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

start_cli()
