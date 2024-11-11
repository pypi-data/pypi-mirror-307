import json

class StoredAgent:
    """
    A class for building agents that persist state between interactions.
    """
    def __init__(self, id: str, **kwargs):
        """
        Initialize the agent. If the agent state file exists, load it.
        Otherwise, save the current state.

        Args:
            id (str): Unique identifier for the agent
            **kwargs: Additional attributes to store on the agent
        """
        self.id = id
        # If the agent state file exists, load it
        try:
            self.load(id)
        except FileNotFoundError:
            pass
        ## Store all other kwargs as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def save(self):
        # Save the agent state as JSON to a file, including all attributes
        with open(f'{self.id}.json', 'w') as f:
            json.dump(self.__dict__, f)

    def load(self, id: str):
        # Load the agent state from a JSON file
        with open(f'{id}.json', 'r') as f:
            self.__dict__ = json.load(f)

    def process(self, input: str):
        # Print the agent's attributes
        print(self.__dict__, input)
        return input

    def invoke(self, input: str):
        # Load the agent state from the file
        self.load(self.id)
        # Invoke the agent with input
        output = self.process(input)
        # Save the agent state to the file
        self.save()
        return output
