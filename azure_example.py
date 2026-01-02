"""Browser-Use example with Azure OpenAI endpoint."""

from browser_use import Agent, Browser, ChatOpenAI
import asyncio
import os


async def example():
	"""Run a simple browser automation task with Azure OpenAI."""
	
	# Azure configuration from .env
	azure_endpoint = os.getenv('AZURE_ENDPOINT')
	azure_api_key = os.getenv('AZURE_API_KEY')
	azure_model = os.getenv('AZURE_MODEL')
	azure_api_version = os.getenv('AZURE_API_VERSION', '2024-05-01-preview')
	
	if not all([azure_endpoint, azure_api_key, azure_model]):
		raise ValueError('Missing required Azure environment variables: AZURE_ENDPOINT, AZURE_API_KEY, AZURE_MODEL')
	
	# Type assertions after validation
	assert azure_endpoint is not None
	assert azure_api_key is not None
	assert azure_model is not None
	
	browser = Browser()
	
	llm = ChatOpenAI(
		model=azure_model,
		api_key=azure_api_key,
		base_url=f'{azure_endpoint}/openai/deployments/{azure_model}',
		default_headers={
			'api-key': azure_api_key,
		},
		default_query={'api-version': azure_api_version},
		max_completion_tokens=4096,
	)
	
	agent = Agent(
		task='Find the number of stars of the browser-use repo',
		llm=llm,
		browser=browser,
	)
	
	history = await agent.run()
	return history


if __name__ == '__main__':
	asyncio.run(example())
