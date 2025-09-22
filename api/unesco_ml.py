import random
from api import unesco

def predict(dataset_id: str):
    """
    Fetches data from a UNESCO dataset and returns a mock prediction.
    """
    records = unesco.get_records(dataset_id)

    # This is a mock prediction. In a real application, this would be replaced
    # with a call to a real machine learning model.
    if records and records.get("records"):
        # Get a random record and add a mock prediction to it
        random_record = random.choice(records["records"])
        random_record["mock_prediction"] = random.random()
        return random_record

    return {"message": "No records found to make a prediction."}
