# stored-agent

A framework for building agents that persist state between interactions.

## Usage

#### Create a new agent and invoke it
```python
my_agent = StoredAgent(id='agent1', name='My Agent')
response = my_agent.invoke(input='Hello, how are you?')
print(response)
```

#### Load an existing agent and invoke it
```python
my_agent = StoredAgent(id='agent1')
response = my_agent.invoke(input='Hello, how are you?')
print(response)
```

