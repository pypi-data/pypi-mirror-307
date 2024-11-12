
# Greenhub Python SDK

`/greenhub-sdk` is the python pip package for greenhub.ai. 
It allows an end user, such as a scientist, to download the greenhub SDK as a pip package which provides the following functionalities:
- data access to all feature datasets (e.g. vi, soil)
- CLI script to test a yield model implementation before uploading it to greenhub.ai

The following explains the structure and technical details of the package implementations in `/greenhub-sdk`. 
Developers of the package should carefully read this brief overview and, if necessary, expand it when making any changes to the package.


---
## General package structure

The basic structure was built according to the official [pip package documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/). 
TODO division into `/src`, `/test`, and `/dest`, as well as the purpose of `LICENSE`, `pyproject.toml`, and `README_PIP.md`.

For now the `/test` directory does not contain any tests, it only contains some usage examples of the package.

The `/src/greenhub` contains the actual logic of the package. It is further divided into:
- `/scripts` containing the CLI scripts (see below)
- `/utilities` containing arbitrary implementations like helpers, calculations, etc.
- `/data.py` containing the functionalities for data access (see below)
- `/initialize.py` containing the basic functionalities for the user to initialize using an api key (see below)

### System architecture overview
The following model outlines all the important backend components required by the Greenhub SDK (Greenhub pip package). 
The two main objectives of this structure are: API key management and REST API for data access.
The following documentation will repeatedly reference this model.

<img src="greenhub_sdk_system_backend_architecture.png" alt="drawing" width="1000"/>


---
## Backend - implementation details

### API Authentication

As the script provided by the scientist should be runnable either during development locally or in the cloud during when executed on the platform, we provide two different forms of authentication: Cloud ID Token / API Key.
The switch between these two different methods of authentication is done transparent for the scientist in `utitilities/auth.py` depending on whether the `CLOUD_RUN_JOB` environment variable is set.

#### API Key Management
In the greenhub.ai's Firebase Database, a new database named `apiKeys` has been created. It includes all active and deactivated API keys.
A user registered on greenhub.ai possesses exactly one active API key, which one can read and reset on greenhub.ai.
Each API key (Firebase Database `apiKeys` document) consists of the following attributes:
- `deactivated: bool`: if a key is deactivated, e.g. the user generates or requests a new one, this attribute is set to `true` so that others (e.g. REST API for data access) know that this key must no longer be used. The `apiKeys` Firebase document is deliberately not deleted, so that even after deactivation, it can be traced how often this key was used and by whom.
- `generatedOn: timestamp`: timestamp of when the key was created.
- `key: string`: API key secret, 32 characters long, consisting only of [A-Z][a-z][0-9]
- `lastUsedOn: timestamp`: timestamp of when the key was last used (e.g. through REST API for data access).
- `requestsCount: 36`: when the API key is used, this counter is incremented by 1.
- `userEmail: string`: email of the user registered on greenhub.ai.

The stored API keys are manipulated only by the following functionalities:
- greenhub.ai website (see `/WebApp`): user can reset api key -> old API key in `apiKeys` is deactivated and a new one is generated.
- google cloud function `createApiKeyForNewUser`: is automatically triggered by Google Cloud when a user registers (= new user in Firebase is created) -> generates a new API key for the user in `apiKeys`. (see `Greenhub.ai/firebase/functions/src/index.ts`)

#### Google Cloud ID Token Authentication
In order to be able to run the scripts created by the user independently of the set API Key, that may be renewed or may expire at some time in the future, within the Google Cloud OIDC ID Token are used for the authentication.
These ID Tokens are retrieved from and endpoint provided within the Google Cloud Run Environment. 
The ID Token is then send in `Authorization` Header as Bearer Token to the API.

### REST API for data access

To enable the access to the data using the SDK, we create a simple REST API endpoint using Google Cloud Functions. 
This API returns the requested feature data as a csv when requested with an API key and a feature data path.
This REST API is implemented with a Google Cloud Function named `getFeatureData` (see `Greenhub.ai/firebase/functions/src/index.ts`). 
In essence, it first validates the provided API key and then returns the requested data. The data to be returned is specified by the `featureDataPath` parameter. 
This parameter contains the path to the requested feature data csv file, which is stored in Google Cloud Storage under `/featureData`, for example: `/BR/vi/country/2010-01.csv`.

---
## Package functionalities - implementation details
The following section discusses the implementation of the actual functionalities of the pip package (greenhub SDK). 
The code for this can be found in `/src/greenhub` 

### functionality: data access to all feature datasets (e.g. vi, soil)
In `/src/greenhub/data.py` all data loading functionalities are implemented. 
For each available feature data type, there is an individual method that can be configured via parameters, 
allowing the user to load exactly the feature data they want. Additionally, there are some extra functionalities that 
enable loading multiple different feature data sources simultaneously.

All functions that load data from Google Cloud Storage work roughly as follows: 
Using the parameters of the function, the function compiles a list of "paths" that point to the csv files in Google Cloud Storage, 
which are to be loaded, concatenated, and returned. Then, for each path, it is checked whether it already exists in the cache, 
and if not, the (Google Cloud Function) REST API `getFeatureDate` is called to request the corresponding csv data for each path.

#### caching
With the help of the `FeatureDataCache` in `/src/greenhub/utilities/feature_data_cache.py`, data loaders are enabled 
to cache loaded data, so that upon a repeated request, the data is loaded faster and the REST API is relieved.
The stored data is saved in the background in a dedicated temp directory and remains available even after closing the 
terminal, environment, etc. The cached data is only lost upon restarting the computer.
For more details, please have a look into `/src/greenhub/data.py`.

### functionality: CLI script to test a yield model implementation before uploading it to greenhub.ai
Another function of the greenhub python SDK package is to provide a simple command line tool (CLI) that allows the user 
to test their created folder with their implemented model before uploading it, calling `greenhub test` in the terminal.
This involves checking if a file named `run.py` exists and if it contains a `run` method with one of the expected signatures.
The CLI was implemented as the 'Entry Point' functionality [more](https://setuptools.pypa.io/en/latest/userguide/entry_point.html).

---
## Building and uploading the package
##### For testing
For testing purposes, the greenhub package can be uploaded to pip's test environment/website [more](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives).
Main steps:
1. cd to `/greenhub-sdk`
2. `python3 -m build`
3. `python3 -m twine upload --skip-existing --repository testpypi dist/*`

for production, the greenhub package is uploaded to pip, following these steps:
1. cd to `/greenhub-sdk`
2. `python3 -m build`
3. `python3 -m twine upload dist/*`