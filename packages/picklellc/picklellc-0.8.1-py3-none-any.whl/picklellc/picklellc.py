import requests
import re

def is_valid_uuid(uuid_string):
    # Regular expression pattern for UUID format
    pattern = re.compile(
        r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'
    )
    return bool(pattern.match(uuid_string))

class PickleLLCAPI:
    def __init__(self, api_key, base_url='http://api.proxy.kic.pickle.com/api/'):
        """
        Initialize the PickleLLCAPI class with the provided API key and base URL.

        :param api_key: Your unique API key for authentication.
        """
        self.api_key = api_key
        self.base_url = base_url
        if not is_valid_uuid(self.api_key):
            raise ValueError('Wrong API Key Format')

    def make_post_request(self, payload):
        """
        Helper method to make a POST request to the API.

        :param payload: The payload to send in the POST request.
        :return: The API response in JSON format if successful, otherwise raises an exception.
        """
        payload['api_key'] = self.api_key
        try:
            initial_response = requests.post(self.base_url, allow_redirects=False)
            secure_url = initial_response.headers['Location'].replace('http://', 'https://')
            response = requests.post(secure_url, json=payload)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"Server Unavalaible. API Request failed: {e}")

    def solve_tsp(self, distance_matrix, n_cities, starting_point=0):
        """
        Solve the Traveling Salesman Problem (TSP).

        :param distance_matrix: A 2D array representing the distances between cities.
        :param n_cities: The number of cities to be visited.
        :param starting_point: The index of the city where the tour should start.
        :return: The optimal tour and time to solve the problem.
        """
        payload = {
            'problem_type': 'tsp',
            'distance_matrix': distance_matrix,
            'n_cities': n_cities,
            'starting_point': starting_point
        }
        return self.make_post_request(payload)

    def run_regression(self, train_data, test_data, moments_to_predict, stock_symbol=None,end_training_date='date',training_duration='day',prediction_duration='min'):
        """
        Perform regression analysis.

        :param train_data: The dataset used to train the regression model.
        :param test_data: The dataset used to test the regression model.
        :param moments_to_predict: The number of future moments for predictions.
        :param training_duration: day-min, each day or minute for the training.
        :param prediction_duration: day-min, each day or minute for the prediction.
        :param stock_symbol: A stock symbol to pull historical data (optional).
        :return: A dictionary containing loss values, predictions on train/test data, and future predictions.
        """
        payload = {
            'problem_type': 'regression',
            'train_data': train_data,
            'test_data': test_data,
            'moments_to_predict': moments_to_predict,
            'stock_symbol': stock_symbol,
            'end_training_date':end_training_date,
            'training_duration': training_duration,
            'prediction_duration': prediction_duration
        }
        return self.make_post_request(payload)

    def train_language_model(self, text_data_set, prompt):
        """
        Train a language model.

        :param text_data_set: A dataset in text format used to train the language model.
        :param prompt: An initial piece of text to guide the model's text generation.
        :return: A dictionary with the model's special code, generated text, and training time.
        """
        payload = {
            'problem_type': 'lm',
            'text_data_set': text_data_set,
            'prompt': prompt
        }
        return self.make_post_request(payload)

    def query_language_model(self, model_code, prompt):
        """
        Query a trained language model.

        :param model_code: The unique code of the trained language model to be queried.
        :param prompt: The question or prompt to query the model with.
        :return: A dictionary with the model's response and code.
        """
        payload = {
            'problem_type': 'asklm',
            'model_code': model_code,
            'prompt': prompt
        }
        return self.make_post_request(payload)

    def solve_knapsack(self, weights, values, capacity):
        """
        Solve the Knapsack Problem.

        :param weights: A list of weights for each item.
        :param values: A list of values for each item.
        :param capacity: The maximum weight capacity of the knapsack.
        :return: A dictionary with the optimal value and items selected.
        """
        payload = {
            'problem_type': 'knapsack',
            'weights': weights,
            'values': values,
            'capacity': capacity
        }
        return self.make_post_request(payload)

    def job_scheduling(self, jobs, machines):
        """
        Solve the Job Scheduling problem.

        :param jobs: A list of jobs, each with a specific duration.
        :param machines: A list of machines available for scheduling the jobs.
        :return: A dictionary with the optimal job schedule and the total time required.
        """
        payload = {
            'problem_type': 'job_scheduling',
            'jobs': jobs,
            'machines': machines
        }
        return self.make_post_request(payload)

    def content_based_filtering(self, user_profile, item_profiles):
        """
        Perform Content-Based Filtering for recommendations.

        :param user_profile: A dictionary representing the user's preferences or history.
        :param item_profiles: A list of item profiles to compare against the user profile.
        :return: A list of recommended items based on the user's profile.
        """
        payload = {
            'problem_type': 'content_filtering',
            'user_profile': user_profile,
            'item_profiles': item_profiles
        }
        return self.make_post_request(payload)

    def protein_folding(self, sequence):
        """
        Solve the Protein Folding problem.

        :param sequence: A string representing the protein sequence.
        :return: A dictionary with the predicted protein structure.
        """
        payload = {
            'problem_type': 'protein_folding',
            'sequence': sequence
        }
        return self.make_post_request(payload)

    def optimal_strategy_finding(self, game_state):
        """
        Find the optimal strategy for a given game state.

        :param game_state: A dictionary representing the current state of the game.
        :return: A dictionary with the recommended optimal move or strategy.
        """
        payload = {
            'problem_type': 'optimal_strategy',
            'game_state': game_state
        }
        return self.make_post_request(payload)

    def generative_image_model(self, dataset, prompt):
        """
        Generate images using a Generative Image Model.

        :param dataset: A dataset to train the generative image model.
        :param prompt: A text prompt to guide the image generation process.
        :return: A dictionary with the generated image data and model code.
        """
        payload = {
            'problem_type': 'generative_image',
            'dataset': dataset,
            'prompt': prompt
        }
        return self.make_post_request(payload)

    def generative_audio_model(self, dataset, prompt):
        """
        Generate audio using a Generative Audio Model.

        :param dataset: A dataset to train the generative audio model.
        :param prompt: A text prompt to guide the audio generation process.
        :return: A dictionary with the generated audio data and model code.
        """
        payload = {
            'problem_type': 'generative_audio',
            'dataset': dataset,
            'prompt': prompt
        }
        return self.make_post_request(payload)

    def classify(self, data, category):
        """
        Classify data into a specified category (e.g., images or text).

        :param data: The data to be classified.
        :param category: The category into which the data should be classified (e.g., 'images' or 'text').
        :return: A dictionary with the classification results.
        """
        payload = {
            'problem_type': 'classification',
            'data': data,
            'category': category
        }
        return self.make_post_request(payload)

# You can now use this class to interact with the Pickle LLC API for various problem types.
