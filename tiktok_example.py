"""Browser-Use example to scrape TikTok creator's top 5 videos."""

from browser_use import Agent, Browser, ChatOpenAI
import asyncio
import os


async def scrape_tiktok_videos(creator_username: str = "tiktok"):
	"""Scrape top 5 videos from a TikTok creator."""
	
	# Azure configuration from .env
	azure_endpoint = os.getenv('AZURE_ENDPOINT')
	azure_api_key = os.getenv('AZURE_API_KEY')
	azure_model = os.getenv('AZURE_MODEL')
	azure_api_version = os.getenv('AZURE_API_VERSION', '2024-12-01-preview')
	
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
	
	# Define the task
	task = f"""
	1. Navigate to https://www.tiktok.com/@{creator_username}
	2. Extract the links from the 5 most recent/latest video tiles visible on the page
	3. Return the results as a numbered list of complete video URLs
	Format:
	1. [full URL]
	2. [full URL]
	3. [full URL]
	4. [full URL]
	5. [full URL]
	"""
	
	agent = Agent(
		task=task,
		llm=llm,
		browser=browser,
	)
	
	history = await agent.run()
	return history


if __name__ == '__main__':
	# Change username to any TikTok creator you want
	asyncio.run(scrape_tiktok_videos(creator_username="eugbrandstrat"))
