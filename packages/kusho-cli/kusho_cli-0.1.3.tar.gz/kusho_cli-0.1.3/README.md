# Kusho CLI

### What is KushoAI?

KushoAI is an **AI-powered API testing agent** that helps developers by **generating extensive test suites for APIs within minutes**. If you’re tired of manual testing after every small update or want more reliable monitoring to catch errors before they hit production, KushoAI can help. Simply provide your API information, and KushoAI will generate real-world test cases that are ready to execute.

`kusho-cli` is the command-line tool for using KushoAI to generate and run test suites directly from your terminal. For the full range of features, try the [KushoAI web application](https://kusho.ai).

## Installation

To install the `kusho-cli` tool, use:

```bash
pip install kusho-cli
```


### Usage

- Invoke `kusho-cli` using this
```bash
kusho-cli
```
- You will be prompted to enter details about your API like HTTP method, URL, headers, query/path params, request body.
- Wait while KushoAI generates tests for your API using above entered details. This generally takes 2-3 minutes.
- Once the generation is completed, you'll see the tests displayed as a numbered list. Use the number to run a test like this
```bash
--------------------
Test Case 12:
{"description": "Test with a valid identifier in Roman numeral format for 'query_params.key'", "request": {"method": "get", "url": "https://localhost:8080/hello", "api_desc": "", "headers": {}, "path_params": {}, "query_params": {"key": "V"}, "json_body": {}}, "categories": ["Other"], "types": ["Business Logic"], "fields": ["query_params.key"], "uuid": "f01a9524-14d1-41df-9b9b-dc6a039d0e03", "test_suite_id": 19019}
--------------------
Test Case 13:
{"description": "Test without the 'key' identifier field in 'query_params'", "request": {"method": "get", "url": "https://localhost:8080/hello", "api_desc": "", "headers": {}, "path_params": {}, "query_params": {"key": ""}, "json_body": {}}, "categories": ["Other"], "types": ["Business Logic"], "fields": ["query_params.key"], "uuid": "77061233-4e70-40df-9fbd-a5abac5bce85", "test_suite_id": 19019}
--------------------
Test Case 14:
{"description": "Test with an invalid format of Identifier for 'query_params.key'", "request": {"method": "get", "url": "https://localhost:8080/hello", "api_desc": "", "headers": {}, "path_params": {}, "query_params": {"key": "invalidFormat"}, "json_body": {}}, "categories": ["Other"], "types": ["Business Logic"], "fields": ["query_params.key"], "uuid": "c6828701-d441-4560-81bb-55d6395ba6b2", "test_suite_id": 19019}
--------------------
Test Case 15:
{"description": "Test with mixed case characters in the 'key' identifier field in 'query_params'", "request": {"method": "get", "url": "https://localhost:8080/hello", "api_desc": "", "headers": {}, "path_params": {}, "query_params": {"key": "mIxEdCaSe"}, "json_body": {}}, "categories": ["Other"], "types": ["Business Logic"], "fields": ["query_params.key"], "uuid": "cd9c2587-0826-408e-a7e9-65286c627481", "test_suite_id": 19019}
--------------------
Test Case 16:
{"description": "Test with a valid format for the 'key' identifier field in 'query_params'", "request": {"method": "get", "url": "https://localhost:8080/hello", "api_desc": "", "headers": {}, "path_params": {}, "query_params": {"key": "validIdentifier"}, "json_body": {}}, "categories": ["Other"], "types": ["Business Logic"], "fields": ["query_params.key"], "uuid": "a946b37a-f183-432f-89ec-f31203a1cac3", "test_suite_id": 19019}
--------------------
Test Case 17:
{"description": "Test with a negative value for the 'key' identifier field in 'query_params'", "request": {"method": "get", "url": "https://localhost:8080/hello", "api_desc": "", "headers": {}, "path_params": {}, "query_params": {"key": -123}, "json_body": {}}, "categories": ["Other"], "types": ["Business Logic"], "fields": ["query_params.key"], "uuid": "06b3c5f0-f7d7-49ee-bed3-3a130a7940d3", "test_suite_id": 19019}
--------------------
Test Case 18:
{"description": "Test with an identifier containing punctuation for the 'key' identifier field in 'query_params'", "request": {"method": "get", "url": "https://localhost:8080/hello", "api_desc": "", "headers": {}, "path_params": {}, "query_params": {"key": "punct;uation"}, "json_body": {}}, "categories": ["Other"], "types": ["Business Logic"], "fields": ["query_params.key"], "uuid": "efb5fb98-da95-487c-8516-3c18d5900072", "test_suite_id": 19019}
--------------------
Test Case 19:
{"description": "Test with an identifier containing emojis for the 'key' identifier field in 'query_params'", "request": {"method": "get", "url": "https://localhost:8080/hello", "api_desc": "", "headers": {}, "path_params": {}, "query_params": {"key": "emojis\ud83d\ude00"}, "json_body": {}}, "categories": ["Other"], "types": ["Business Logic"], "fields": ["query_params.key"], "uuid": "6021f63a-0192-4e2d-9410-c2c56f2b6732", "test_suite_id": 19019}
--------------------

Select an option:
1. List all test cases
2. Execute all test cases
3. Run a specific test case
4. Exit

> 3 17
```
- Alternatively, you can run all tests using option 2   


For a detailed product walkthrough of the KushoAI web application, you can watch the video [here](https://www.youtube.com/watch?v=4z4pI5N0_7o).

<br>

> NOTE: This CLI version of KushoAI has limited features at the moment. For our full suite of features, you can use the [KushoAI web application](https://kusho.ai). 