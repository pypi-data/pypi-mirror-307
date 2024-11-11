# EnydayPy Python Client

EnydayPy is a Python client library for interacting with the Enyday API. This library provides access to user authentication, user details, authorization data, address information, and power consumption data.

## Installation

To install the EnydayPy library, use `pip`:

```bash
pip install EnydayPy
```
## Usage

The following is an example of how to use the EnydayPy client to interact with the Enyday API:

1. Import the necessary libraries
```python
from EnydayPy import EnydayClient
from getpass import getpass
from datetime import datetime, timedelta
import pytz
```
2. Create an instance of the API class
You will need to provide your Enyday email and password to authenticate.
```python
username = input("Enter your Enyday email: ")
password = getpass("Enter your Enyday password: ")

client = EnydayClient()
client.connect(username, password)
```
3. Get the user details
Once authenticated, you can fetch the user details.
```python
User = client.get_user_details()
print(User.id)
```
4. Get the user's addresses
You can retrieve the addresses associated with your user ID.
```python
Addresses = client.get_address_by_user_id(User.id).addresses
print(Addresses)
```
5. Get the Eloverblik authorizations
This allows you to fetch the Eloverblik authorization data for the user.
```python
Eloverblik = client.get_eloverblik_authorization(User.id)
print(Eloverblik)
```
6. Get the power consumption
You can fetch the power consumption data by specifying a date range. The following example shows how to get power consumption between two dates (using the Europe/Copenhagen timezone):
```python
begin = datetime(2024, 11, 8, 0, 0, 0)
end = datetime(2024, 11, 8, 0, 0, 0)

# Set the timezone to Europe/Copenhagen
begin = pytz.timezone("Europe/Copenhagen").localize(begin)
end = pytz.timezone("Europe/Copenhagen").localize(end)

# Convert datetime from Europe/Copenhagen to UTC
begin = begin.astimezone(pytz.utc)
end = end.astimezone(pytz.utc)

print(f"Begin: {begin}")
print(f"End: {end}")

Power = client.get_power_consumption_by_user_and_address_ids(
    User.id, 
    Addresses[0].id, 
    begin, 
    end, 
    as_dataframe=True
)

# Print the sum of the power consumption
print(f"Power from PV: {Power['power_internal'].sum()}")
print(f"Power from grid: {Power['power_external'].sum()}")
```
7. Notes
The EnydayPy client requires a valid Enyday user account for authentication.
All time-related data is converted to UTC for consistency.
The library supports retrieval of power consumption, addresses, and Eloverblik authorizations.

## License

This project is licensed under the MIT License.

MIT License

Copyright (c) [2024] [Bruno Adam]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.