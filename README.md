# JobDog

JobDog is a Python library for fetching and parsing job listings from various job boards and career sites. It provides a standardized output format for job data, making it easy to work with job listings from multiple sources.

## Description

**JobDog is currently in the alpha stage of development.**

JobDog is designed to be a flexible and extensible library for fetching and parsing job listings from various job boards and career sites. It allows you to add support for new providers by implementing the `BaseParser` class and registering the parser using the `register_parser` decorator.

The primary goal of JobDog is to simplify the process of gathering job listing data for analysis, integration with other tools, or feeding into language models for improved job application processes. It's particularly useful for:

- Job seekers looking to aggregate listings from multiple sources
- Researchers analyzing job market trends
- Developers building job-related applications or tools

JobDog is not built to be compatible with large volume scrapers - rather, it is designed as a tool to help you communicate job descriptions to LLMs to create better applications.

## Core Functionality

- Fetch job listing details from supported job boards
- Parse job listings into a standardized format (JobListing model)
- Support for multiple job board strategies
- Synchronous API (Asynchronous API planned for future releases)
- Error handling and logging for improved debugging and reliability
- Extensible architecture for adding new job board support

## Supported Providers

- [x] JobIndex.dk
- [ ] LinkedIn.com (In progress)

### Planned Support

- Indeed.com
- Greenhouse.io
- Teamtailor.com

## Features Checklist

- [x] Standardized job listing output
- [x] Strategy pattern for site-specific parsing
- [x] Factory for selecting appropriate parsing strategy
- [x] Extensible architecture for adding new job board support
- [x] Basic error handling and logging
- [ ] Advanced error handling, retries mechanisms
- [ ] Documentation and usage examples
- [ ] Python package distribution on PyPI

## Installation

Proper instructions to come - if you for some reason want to install it now, use poetry.


## Usage

Here's a basic example of how to use JobDog:

```python
dog = JobDog()

job_listing = dog.fetch_details("https://www.supported-provider.com/job/123456")
```
This will return a JobListing object with a varying degree of detail depending on the provider - but always the job title, description and company name.

JobDog uses httpx for fetching, so you can pass in any httpx request kwargs - or pass a custom httpx client when instantiating JobDog.





## License

This project and code within is licensed under the MIT License. Information gathered by using this tool is subject to the terms and privacy policies of the individual providers.