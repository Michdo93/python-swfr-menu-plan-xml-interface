# python-swfr-menu-plan-xml-interface
A simple python code accessing the XML interface of the menu plan from SWFR (Studierendenwerk Freiburg-Schwarzwald).

More informations you can find [here](https://www.swfr.de/essen/mensen-cafes-speiseplaene/speiseplan-xml-schnittstelle).

## Pre-Installation

The code is written in such a way that it can be used in both Python 2.7 and Python 3.x. The following must be installed via pip before use.

Python 2.7:

```
python -m pip install requests
python -m pip install xmltodict
```

Python 3:

```
python3 -m pip install requests
python3 -m pip install xmltodict
```

## Explanation XML interface

### API-Key

If you want to access the XML interace you need an API-Key which you can request at SWFR. The `baseurl` is:

```
https://www.swfr.de/apispeiseplan?&type=98&tx_speiseplan_pi1[apiKey]={YOUR_API_KEY}
```

### Location ID

If you want to retrieve data from a specific location you have to add following to the `baseurl`:

```
&tx_speiseplan_pi1[ort]={LOCATION_ID}
```

| Location | ID |
|:--------:|:--:|
|Mensa Rempartstraße|610|
|Mensa Institutsviertel|620|
|Mensa Littenweiler|630|
|Mensa Furtwangen|641|
|Mensa Offenburg|651|
|Mensa Gengenbach|652|
|Mensa Kehl|661|
|Mensa Schwenningen|671|
|Mensa Lörrach|677|
|Mensa Flugplatz|681|
|MusiKantine|722|
|Haus zur Lieben Hand|776|
|Otto-Hahn-Gymnasium Furtwangen|9012|

### Days

If you do not specify how many days you would like to receive the information, you will receive the information for the next 6 days (including today). If you want to limit the days displayed, you can add the following to the `url`:

```
&tx_speiseplan_pi1[tage]={DAYS}
```

|Days|Meaning|
|:--:|:-----:|
| |today + the next 5 days|
|None|today + the next 5 days|
|0|today + the next 5 days|
|1|today|
|2|today + tomorrow|
|3|today + the next 2 days|
|4|today + the next 3 days|
|5|today + the next 4 days|
|6|today + the next 5 days|
|n > 6|today + the next 5 days|

Please notice:

1. Sunday is fundamentally ignored.
2. Today is always taken as the starting point. So 1 will only stand for Monday on a Monday and not always for Monday.
3. A week break is made, minus Sundays.
4. Days on which the canteen is closed are ignored. If, for example, there are public holidays and a long weekend within the next few days, fewer data records will be returned. During semester or school holidays, this can mean that no data records are returned at all.

### i18n (Internationalization)

A little fact in passing as to why we use i18n in computer science. In the English word internationalisation, there are 18 letters between the i and the n.

The interface offers the option of requesting the data in English. However, the interface only offers English or German. To access the English API, the baseurl changes as follows:

```
https://www.swfr.de/en/apispeiseplan?&type=98&tx_speiseplan_pi1[apiKey]={YOUR_API_KEY}
```

## Usage

This Python code serves as a wrapper for the menu plan API of Studierendenwerke Freiburg-Schwarzwald (SWFR). It makes it possible to retrieve menus for various canteens and extract information on menus, prices, allergens and more.

### Using the MenuPlan object

Please replace `<YOUR_API_KEY>` with your own api key.

```
from menu_plan import MenuPlan

# create instance of MenuPlan
menu_plan_instance = MenuPlan(api_key="<YOUR_API_KEY>")

# Example tests
location_id = 641
location_name = "Mensa Furtwangen"
menu_type = "Essen 1"
schedule_date = "27.02.2024"

# function tests
menu_plan_instance.set_location_id(location_id)
print("Location Name by ID:", menu_plan_instance.get_location_name_by_id(location_id))

menu_plan_instance.set_location_id_by_location_name(location_name)
print("Location ID by Name:", menu_plan_instance.get_location_id())

xml_data = menu_plan_instance.get_menu_plan_from_xml_interface(location_id)
print(xml_data)

menu_data = menu_plan_instance.get_menu_from_menu_plan(location_id, menu_type, schedule_date)
print("\nMenu Data:")
print(menu_data)

# ... (further code)
```

### MenuPlan Class

#### Initialization

You could create one or multiple instances like this:

```
menu_plan_instance = MenuPlan(api_key, location_id=None, days=None, i18n=False)
```


- `api_key`: Your personal API key for accessing the menu plan API.
- `location_id`: The ID of the dining hall for which information is to be retrieved (optional).
- `days`: The number of days for which the menu plan is to be retrieved (optional).
- `i18n`: Indicates whether the internationalized version of the menu plan should be used (optional).

#### Methods

##### `set_location_id(location_id=None)`

Sets the location ID for the dining hall to be retrieved.

###### Parameters
- `location_id`: The ID of the dining hall.

###### Returns
None

###### Description
This method sets the location ID for the dining hall to be retrieved.

##### `get_location_id()`

Returns the currently set location ID.

###### Parameters
None

###### Returns
- `location_id`: The ID of the currently set dining hall.

###### Description
This method returns the currently set location ID.

##### `set_location_id_by_location_name(location_name=None)`

Sets the location ID based on the dining hall name.

###### Parameters
- `location_name`: The name of the dining hall.

###### Returns
None

###### Description
This method sets the location ID based on the dining hall name.

##### `set_days(days=None)`

Sets the number of days for the menu plan.

###### Parameters
- `days`: The number of days.

###### Returns
None

###### Description
This method sets the number of days for the menu plan.

##### `get_days()`

Returns the currently set number of days.

###### Parameters
None

###### Returns
- `days`: The number of days.

###### Description
This method returns the currently set number of days.

##### `set_i18n(i18n=False)`

Enables or disables the international version of the menu plan.

###### Parameters
- `i18n`: A boolean indicating whether the international version should be enabled.

###### Returns
None

###### Description
This method enables or disables the international version of the menu plan.

##### `get_i18n()`

Returns whether the international version of the menu plan is enabled.

###### Parameters
None

###### Returns
- `i18n`: A boolean indicating whether the international version is enabled.

###### Description
This method returns whether the international version of the menu plan is enabled.

##### `set_api_key(api_key)`

Sets the API key for the menu plan.

###### Parameters
- `api_key`: Your personal API key.

###### Returns
None

###### Description
This method sets the API key for accessing the menu plan API.

##### `get_api_key()`

Returns the set API key.

###### Parameters
None

###### Returns
- `api_key`: Your personal API key.

###### Description
This method returns the set API key.

##### `get_menu_plan_from_xml_interface(location_id=None, days=None, i18n=False)`

Retrieves the menu plan as XML from the API.

###### Parameters
- `location_id`: The ID of the dining hall.
- `days`: The number of days.
- `i18n`: A boolean indicating whether the international version should be used.

###### Returns
- `xml_data`: The menu plan data in XML format.

###### Description
This method retrieves the menu plan as XML from the API.

##### `get_menu_from_menu_plan(location=None, menu_type="Essen 1", schedule_date=datetime.now().strftime("%d.%m.%Y"))`

Retrieves information about a specific menu.

###### Parameters
- `location`: The location (ID or name) for which to retrieve the menu.
- `menu_type`: The type of menu (default is "Essen 1").
- `schedule_date`: The date for which to retrieve the menu (default is today).

###### Returns
- `menu_data`: Information about the specified menu.

###### Description
This method retrieves information about a specific menu.

#### Additional Methods

There are many more methods in the `MenuPlan` class that retrieve information about prices, allergens, additives, etc.

**Note:** Please replace `<YOUR_API_KEY>` with your actual API key.


#### Additional Methods (Continued)

##### `get_menu_types()`

Retrieves a dictionary of available menu types for each dining hall.

###### Parameters
None

###### Returns
- `menu_types`: A dictionary mapping dining hall IDs to a list of available menu types.

###### Description
This method retrieves a dictionary of available menu types for each dining hall.

##### `get_menu_type(id_or_name)`

Retrieves the available menu types for a specific dining hall.

###### Parameters
- `id_or_name`: The ID or name of the dining hall.

###### Returns
- `menu_types`: A list of available menu types for the specified dining hall.

###### Description
This method retrieves the available menu types for a specific dining hall.

##### `get_menu_type_by_id(id)`

Retrieves the available menu types for a specific dining hall by ID.

###### Parameters
- `id`: The ID of the dining hall.

###### Returns
- `menu_types`: A list of available menu types for the specified dining hall.

###### Description
This method retrieves the available menu types for a specific dining hall by ID.

##### `get_customer_types()`

Retrieves a list of customer types.

###### Parameters
None

###### Returns
- `customer_types`: A list of customer types.

###### Description
This method retrieves a list of customer types, such as "studierende," "angestellte," "gaeste," and "schueler."

##### `get_menu_type_by_name(name)`

Retrieves the available menu types for a specific dining hall by name.

###### Parameters
- `name`: The name of the dining hall.

###### Returns
- `menu_types`: A list of available menu types for the specified dining hall.

###### Description
This method retrieves the available menu types for a specific dining hall by name.

##### `set_xml(xml_string=None)`

Sets the XML data for the menu plan.

###### Parameters
- `xml_string`: The XML data as a string.

###### Returns
None

###### Description
This method sets the XML data for the menu plan.

##### `get_xml()`

Retrieves the currently set XML data.

###### Parameters
None

###### Returns
- `xml_data`: The currently set XML data.

###### Description
This method retrieves the currently set XML data.

##### `get_location_id_by_name(location_name)`

Retrieves the location ID for a dining hall by name.

###### Parameters
- `location_name`: The name of the dining hall.

###### Returns
- `location_id`: The ID of the specified dining hall.

###### Description
This method retrieves the location ID for a dining hall by name.

##### `get_location_name_by_id(location_id)`

Retrieves the name of a dining hall by ID.

###### Parameters
- `location_id`: The ID of the dining hall.

###### Returns
- `location_name`: The name of the specified dining hall.

###### Description
This method retrieves the name of a dining hall by ID.

##### `get_locations()`

Retrieves a dictionary of available dining hall IDs and names.

###### Parameters
None

###### Returns
- `locations`: A dictionary mapping dining hall IDs to names.

###### Description
This method retrieves a dictionary of available dining hall IDs and names.

##### `set_location_id(location_id=None)`

Sets the location ID for a dining hall.

###### Parameters
- `location_id`: The ID of the dining hall.

###### Returns
None

###### Description
This method sets the location ID for a dining hall.

##### `set_location_id_by_location_name(location_name=None)`

Sets the location ID based on the dining hall name.

###### Parameters
- `location_name`: The name of the dining hall.

###### Returns
None

###### Description
This method sets the location ID based on the dining hall name.

##### `get_menu_plan_from_xml(location=None)`

Retrieves the menu plan as XML data.

###### Parameters
- `location`: The location (ID or name) for which to retrieve the menu plan.

###### Returns
- `xml_data`: The menu plan data in XML format.

###### Description
This method retrieves the menu plan as XML data.

##### `get_menu_plan_from_xml_by_location_id(location_id=641)`

Retrieves the menu plan as XML data for a specific dining hall by ID.

###### Parameters
- `location_id`: The ID of the dining hall.

###### Returns
- `xml_data`: The menu plan data in XML format.

###### Description
This method retrieves the menu plan as XML data for a specific dining hall by ID.

##### `get_menu_plan_from_xml_by_location_name(location_name="Mensa Furtwangen")`

Retrieves the menu plan as XML data for a specific dining hall by name.

###### Parameters
- `location_name`: The name of the dining hall.

###### Returns
- `xml_data`: The menu plan data in XML format.

###### Description
This method retrieves the menu plan as XML data for a specific dining hall by name.

##### `get_menu_from_menu_plan_by_name(location_name, menu_type="Essen 1", schedule_date=datetime.now().strftime("%d.%m.%Y"))`

Retrieves information about a specific menu by dining hall name.

###### Parameters
- `location_name`: The name of the dining hall.
- `menu_type`: The type of menu (default is "Essen 1").
- `schedule_date`: The date for which to retrieve the menu (default is today).

###### Returns
- `menu_data`: Information about the specified menu.

###### Description
This method retrieves information about a specific menu by dining hall name.

##### `get_menu_from_menu_plan_by_location_id(location_id, menu_type="Essen 1", schedule_date=datetime.now().strftime("%d.%m.%Y"))`

Retrieves information about a specific menu by dining hall ID.

###### Parameters
- `location_id`: The ID of the dining hall.
- `menu_type`: The type of menu (default is "Essen 1").
- `schedule_date`: The date for which to retrieve the menu (default is today).

###### Returns
- `menu_data`: Information about the specified menu.

###### Description
This method retrieves information about a specific menu by dining hall ID.

##### `get_menu_from_menu_plan_by_location(location, menu_type="Essen 1", schedule_date=datetime.now().strftime("%d.%

m.%Y"))`

Retrieves information about a specific menu by dining hall.

###### Parameters
- `location`: The location (ID or name) for which to retrieve the menu.
- `menu_type`: The type of menu (default is "Essen 1").
- `schedule_date`: The date for which to retrieve the menu (default is today).

###### Returns
- `menu_data`: Information about the specified menu.

###### Description
This method retrieves information about a specific menu by dining hall.

##### `get_menus_from_menu_plan(location=None, menu_types=["Essen 1"], schedule_date=datetime.now().strftime("%d.%m.%Y"))`

Retrieves information about multiple menus by dining hall.

###### Parameters
- `location`: The location (ID or name) for which to retrieve the menus.
- `menu_types`: A list of menu types to retrieve (default is ["Essen 1"]).
- `schedule_date`: The date for which to retrieve the menus (default is today).

###### Returns
- `result_menus`: Information about the specified menus.

###### Description
This method retrieves information about multiple menus by dining hall.

##### `get_menu_prices_from_menu_plan(menus)`

Retrieves the prices of menus.

###### Parameters
- `menus`: A list of menus.

###### Returns
- `prices`: A dictionary mapping menu types to prices.

###### Description
This method retrieves the prices of menus.

##### `get_menu_prices_from_menu_plan_by_customer_type(menus, customer_type="studierende")`

Retrieves the prices of menus for a specific customer type.

###### Parameters
- `menus`: A list of menus.
- `customer_type`: The customer type for which to retrieve prices (default is "studierende").

###### Returns
- `prices`: A dictionary mapping menu types to prices.

###### Description
This method retrieves the prices of menus for a specific customer type.

##### `get_pupil_menu_prices_from_menu_plan(menu)`

Retrieves the prices of menus for pupils.

###### Parameters
- `menu`: A menu.

###### Returns
- `prices`: A dictionary mapping menu types to prices.

###### Description
This method retrieves the prices of menus for pupils.

##### `get_student_menu_prices_from_menu_plan(menu)`

Retrieves the prices of menus for students.

###### Parameters
- `menu`: A menu.

###### Returns
- `prices`: A dictionary mapping menu types to prices.

###### Description
This method retrieves the prices of menus for students.

##### `get_employee_menu_prices_from_menu_plan(menu)`

Retrieves the prices of menus for employees.

###### Parameters
- `menu`: A menu.

###### Returns
- `prices`: A dictionary mapping menu types to prices.

###### Description
This method retrieves the prices of menus for employees.

##### `get_guest_menu_prices_from_menu_plan(menu)`

Retrieves the prices of menus for guests.

###### Parameters
- `menu`: A menu.

###### Returns
- `prices`: A dictionary mapping menu types to prices.

###### Description
This method retrieves the prices of menus for guests.

##### `get_menu_price_from_menu(menu)`

Retrieves the price of a specific menu.

###### Parameters
- `menu`: A menu.

###### Returns
- `price`: The price of the specified menu.

###### Description
This method retrieves the price of a specific menu.

##### `get_menu_price_from_menu_by_customer_type(menu, customer_type="studierende")`

Retrieves the price of a specific menu for a specific customer type.

###### Parameters
- `menu`: A menu.
- `customer_type`: The customer type for which to retrieve the price (default is "studierende").

###### Returns
- `price`: The price of the specified menu for the specified customer type.

###### Description
This method retrieves the price of a specific menu for a specific customer type.

##### `get_pupil_menu_price_from_menu(menu)`

Retrieves the price of a specific menu for pupils.

###### Parameters
- `menu`: A menu.

###### Returns
- `price`: The price of the specified menu for pupils.

###### Description
This method retrieves the price of a specific menu for pupils.

##### `get_student_menu_price_from_menu(menu)`

Retrieves the price of a specific menu for students.

###### Parameters
- `menu`: A menu.

###### Returns
- `price`: The price of the specified menu for students.

###### Description
This method retrieves the price of a specific menu for students.

##### `get_employee_menu_price_from_menu(menu)`

Retrieves the price of a specific menu for employees.

###### Parameters
- `menu`: A menu.

###### Returns
- `price`: The price of the specified menu for employees.

###### Description
This method retrieves the price of a specific menu for employees.

##### `get_guest_menu_price_from_menu(menu)`

Retrieves the price of a specific menu for guests.

###### Parameters
- `menu`: A menu.

###### Returns
- `price`: The price of the specified menu for guests.

###### Description
This method retrieves the price of a specific menu for guests.

##### `additives_text_to_dict(additives_text)`

Converts additives text to a dictionary.

###### Parameters
- `additives_text`: Text containing additives information.

###### Returns
- `additives_dict`: A dictionary containing additives information.

###### Description
This method converts additives text to a dictionary.

##### `get_additives_from_menu(menu)`

Retrieves additives information from a menu.

###### Parameters
- `menu`: A menu.

###### Returns
- `additives_dict`: A dictionary containing additives information.

###### Description
This method retrieves additives information from a menu.

##### `get_allergens_from_menu(menu)`

Retrieves allergens information from a menu.

###### Parameters
- `menu`: A menu.

###### Returns
- `allergens_dict`: A dictionary containing allergens information.

###### Description
This method retrieves allergens information from a menu.

##### `get_daily_schedule(location=None

, schedule_date=datetime.now().strftime("%d.%m.%Y"))`

Retrieves the daily schedule for a specific dining hall.

###### Parameters
- `location`: The location (ID or name) for which to retrieve the daily schedule.
- `schedule_date`: The date for which to retrieve the daily schedule (default is today).

###### Returns
- `schedule_data`: Information about the daily schedule.

###### Description
This method retrieves the daily schedule for a specific dining hall.

##### `get_schedule_plans(location=None, start_date=datetime.now().strftime("%d.%m.%Y"), num_days=6)`

Retrieves multiple daily schedules for a specific dining hall.

###### Parameters
- `location`: The location (ID or name) for which to retrieve the daily schedules.
- `start_date`: The starting date for retrieving schedules (default is today).
- `num_days`: The number of days for which to retrieve schedules (default is 6).

###### Returns
- `schedule_plans`: Information about the daily schedules.

###### Description
This method retrieves multiple daily schedules for a specific dining hall.
