# JobDog 🐶

JobDog is your faithful Python companion, sniffing out job listings from various job boards and career sites. It fetches and brings back a well-organized pile of job data, making it a breeze to work with listings from multiple sources. Good boy, JobDog!

## 📋 Description

**Woof! JobDog is currently in the puppy (alpha) stage of development.**

JobDog is a tail-waggingly flexible and extensible library for fetching and parsing job listings. It's like a well-trained retriever, bringing back job data from various online "parks" (job boards and career sites). You can even teach JobDog new tricks by implementing the `BaseParser` class and using the `register_parser` decorator to support new job board breeds!

The mission of JobDog is simple: to be your best friend in gathering job listing data. Whether you're:

- A job seeker wanting to sniff out listings from multiple sources
- A researcher trying to fetch trends in the job market landscape
- A developer building the next big job-related app or tool

JobDog is here to help, with a wag of its tail and a bark of excitement!

JobDog isn't designed for high-volume scraping (that would be like trying to chase every squirrel in the park). Instead, it's your loyal companion in communicating job descriptions to LLMs, helping create fetching job applications. It's perfect for:

- Fetching individual job listings for detailed analysis
- Gathering a small set of listings for comparison
- Providing structured job data to feed into LLMs or other tools


In future releases, JobDog will learn some new tricks, using LLMs to assist with even deeper parsing of job listings. Stay tuned for these paw-some updates!


🚀 Features

- Fetch structured job listing details from supported job boards
- Support for multiple job board strategies
- Synchronous API (Asynchronous API planned for future releases)
- Error handling and logging for improved debugging and reliability
- Extensible architecture for adding new job board support
- LLM assisted parsing (coming soon)

## 🐾 Supported Job Boards

- [x] JobIndex.dk
- [x] Greenhouse.io
- [ ] LinkedIn.com (In progress)

Coming soon:

- Indeed.com
- Teamtailor.com



## 🦴 Installation



Proper instructions to come - if you for some reason want to install it now, you probably now what to do.



## 🎾 Quick Start

Here's a basic example of how to use JobDog:

```python
from jobdog import JobDog

dog = JobDog()

job = dog.fetch_details("https://www.supported-provider.com/job/123456")

print(job.job_title)  # "Chief Squirrel Chaser"
print(job.company_name)  # "Barks & Recreation Inc."
print(job.job_description)  # "Are you a good boy or girl who loves to run? We need your..."

```

## 🧠 LLM-Assisted Parsing (Coming Soon!)

Configure a LLM client of your choosing and pass it on `llm_client` when instantiating JobDog, or set OpenAI/Anthropic/etc. API key on their respective input parameters.

```python
from jobdog import JobDog
from openai import OpenAI

# Create an OpenAI client (you can use other LLM providers too!)
llm_client = OpenAI(api_key="your-secret-api-key")

# Initialize JobDog with the LLM client
dog = JobDog(llm_client=llm_client)

# Fetch job details with LLM assistance
job = dog.fetch_details("https://www.supported-provider.com/job/123456", use_llm=True)

print(job.skills)  # ["Squirrel Spotting", "High-Speed Chasing", "Tennis Ball Retrieval"]
print(job.experience_level)  # "Senior (7+ dog years)"
print(job.salary)  # "50,000 treats per year"
print(job.benefits)  # ["Unlimited belly rubs", "Premium kibble plan", "Doggy daycare"]

```


## 🦮 Advanced Usage

JobDog uses [httpx](https://www.python-httpx.org/api/#client) for fetching, so you can customize your requests:

```python
import httpx
from jobdog import JobDog

custom_client = httpx.Client(
    headers={"User-Agent": "GoodestBoy/1.0"},
    timeout=30
)

dog = JobDog(http_client=custom_client)
```



## 📄 License

This project and code within is licensed under the MIT License. Information gathered by using this tool is subject to the terms and privacy policies of the individual providers.


## 📝 Todo

- [x] Standardized job listing output
- [x] Strategy pattern for site-specific parsing
- [x] Factory for selecting appropriate parsing strategy
- [x] Extensible architecture for adding new job board support
- [x] Basic error handling and logging
- [ ] Advanced error handling, retries mechanisms
- [ ] Documentation and usage examples
- [ ] Python package distribution on PyPI
