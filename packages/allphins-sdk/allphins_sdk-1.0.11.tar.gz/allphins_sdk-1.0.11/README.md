# Allphins SDK

The Allphins SDK allows authorized users to access the Allphins API.

The SDK provides a set of interfaces to interact with the Allphins API.

The SDK is designed to be straightforward to use and to provide a seamless experience for users.

## Installation
To install the allphins sdk, run the command:

```
pip install allphins-sdk
```  
Python >= 3.10 is required.

## SDK Authentication
To authenticate to Allphins, set the following environment variables:  
```
ALLPHINS_APIKEY=YOUR_API_KEY
ALLPHINS_PASSKEY=YOUR_PASS_KEY
```

## Usage
To use the SDK, import the `allphins` module and then start using one of the interfaces.

ex:

```python
import allphins

allphins.get_portfolios()
```

## Documentation
The full documentation is accessible [here](https://sdk-doc.allphins.com/)