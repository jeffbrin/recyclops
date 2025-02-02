from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import random
from utils.custom_logger import get_logger

logger = get_logger(__name__)
class Scoreboard:
    def __init__(self, host="localhost",port= 27017):
        """
        initialize the scoreboard object, create the database,and correct tables
        """
        try:

            self.dbClient = MongoClient(host,port)
            
            self.database = self.dbClient["disposing"]
            self.collection = self.database["thrown_items"]
           
        except Exception as e:
            logger.critical(f"unable to initialize the database {e}")

    def generate_dummy_data(self):
        components = [
                    {"component_name": "Bottle", "material": "Plastic", "recycling_number": "1", "disposable_category": "Recycling"},
                    {"component_name": "Cap", "material": "Plastic", "recycling_number": "5", "disposable_category": "Recycling"},
                    {"component_name": "Pizza Box", "material": "Cardboard", "disposable_category": "Compost"},
                    {"component_name": "Banana Peel", "material": "Organic Waste", "disposable_category": "Compost"},
                    {"component_name": "Plastic Bag", "material": "Plastic", "recycling_number": "4", "disposable_category": "Garbage"},
                    {"component_name": "Glass Jar", "material": "Glass", "recycling_number": "None", "disposable_category": "Recycling"},
                    {"component_name": "Paper Towel", "material": "Paper", "disposable_category": "Compost"},
                    {"component_name": "Styrofoam Cup", "material": "Polystyrene", "disposable_category": "Garbage"},
                    {"component_name": "Aluminum Can", "material": "Metal", "recycling_number": "None", "disposable_category": "Recycling"},
                    {"component_name": "Yogurt Cup", "material": "Plastic", "recycling_number": "6", "disposable_category": "Recycling"}
                ]
        base_time = datetime.now(timezone.utc)
        time_deltas = [timedelta(minutes=random.randint(1, 1440)) for _ in components]
        timestamps = [(base_time - delta).isoformat() for delta in time_deltas]
        user_bin_results = [
                    {"user_bin": "Recycling", "result": "correct", "timestamp": timestamps[0]},  
                    {"user_bin": "Garbage", "result": "incorrect", "timestamp": timestamps[1]},  
                    {"user_bin": "Compost", "result": "correct", "timestamp": timestamps[2]},  
                    {"user_bin": "Compost", "result": "correct", "timestamp": timestamps[3]},  
                    {"user_bin": "Recycling", "result": "incorrect", "timestamp": timestamps[4]}, 
                    {"user_bin": "Recycling", "result": "correct", "timestamp": timestamps[5]},  
                    {"user_bin": "Garbage", "result": "incorrect", "timestamp": timestamps[6]}, 
                    {"user_bin": "Garbage", "result": "correct", "timestamp": timestamps[7]}, 
                    {"user_bin": "Recycling", "result": "correct", "timestamp": timestamps[8]},  
                    {"user_bin": "Garbage", "result": "incorrect", "timestamp": timestamps[9]}  
                ]
        return (components,user_bin_results)
     
    def log_sorting_results(self,component,result):
        """
        receives the component from the gpt prompt and the result from the object tracking to log all the relevant info.
        :params component from the returned gpt prompt in the same format i.e  {
                        "component_name": "Cap",
                        "material": "Plastic",
                        "recycling_number": "5",
                        "disposable_category": "Recycling"
                    }
        :params results after tracking in the same format as the gpt i.e   {
                    "user_bin": "Recycling", 
                    "result": "correct", 
                    "timestamp": timestamps[0]
        }

        """
        try:
            log ={
                "component_name": component["component_name"],
                "material" : component["material"],
                "correct_bin" :component["disposable_category"],
                "user_bin" : result["user_bin"],
                "result" : result["result"],
                "timestamp" : result["timestamp"]
            }
            self.collection.insert_one(log)
        except Exception as e :
            logger.critical("Unable to get stats from the table {e}")
            self.close_connection()


    def display_total_stats(self):
        """
        Generates the statistics for the statistics for the table.

        statistics displayed are: Total logs,mistake count, accuracy, last log, most common mistake
        
        """
        try:
            total_logs = self.collection.count_documents({})
            mistake_count = self.collection.count_documents({"result" : "incorrect"})
            accuracy = (total_logs-mistake_count)/total_logs * 100
            last_log = self.collection.find_one(sort=[("timestamp", -1)])
            common_mistake = self.collection.aggregate([
                {"$match" : {"result" : "incorrect"}},
                {"$group" : {"_id": {"correct_bin": "$correct_bin", "user_bin": "$user_bin"}, "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 1}
                
            ])
            common_mistake = list(common_mistake)
            most_common_mistake = common_mistake[0]["_id"] if common_mistake else "None"
            print(f"Sorting Stats")
            print(f"Total Logs: {total_logs}")
            print(f"Mistake Count: {mistake_count}")
            print(f"Accuracy: {accuracy:.2f}%")
            print(f"Most Common Mistake: {most_common_mistake}")
            print(f"Last Log: {last_log}")

        except Exception as e :
            logger.critical("Unable to get stats from the table {e}")
            self.close_connection()


    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        try:
            self.dbClient.close()
            print("MongoDB connection closed.")
        except Exception as e:
            logger.critical(f"error closing the database connection")


     
if __name__ == "__main__":
    try:
        scoreboard = Scoreboard()
        components,user_bin_results = scoreboard.generate_dummy_data()
        for i in range(0,len(components)):
            scoreboard.log_sorting_results(components[i],user_bin_results[i])
        scoreboard.display_total_stats()
    except Exception as e :
        logger.critical(f"Unhandled exception: {e}")
    finally:
        Scoreboard.close_connection()






