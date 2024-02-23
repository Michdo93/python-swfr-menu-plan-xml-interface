import requests
import xmltodict
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

class MenuPlan(object):
    def __init__(self, api_key, location_id=None, days=None, i18n=False):
        self.type = 98
        self.locations = {
            610: "Mensa Rempartstraße",
            620: "Mensa Institutsviertel",
            630: "Mensa Littenweiler",
            641: "Mensa Furtwangen",
            651: "Mensa Offenburg",
            652: "Mensa Gengenbach",
            661: "Mensa Kehl",
            671: "Mensa Schwenningen",
            677: "Mensa Lörrach",
            681: "Mensa Flugplatz",
            722: "MusiKantine",
            776: "Haus zur Lieben Hand",
            9012: "Otto-Hahn-Gymnasium Furtwangen"
        }

        self.menu_types = {
            610: ["Tagesgericht", "Schneller Teller", "Essen 1", "Essen 2", "Wochenangebot", "Buffet"],
            620: ["Schneller Teller", "Essen 1", "Essen 2", "Essen 3", "Wochenangebot", "Buffet", "Abendessen"],
            630: ["Essen 1", "Essen 2", "Wochenangebot", "Buffet"],
            641: ["Schneller Teller", "Essen 1", "Essen 2"],
            651: ["Buffet"],
            652: ["Essen 1", "Essen 2"],
            661: ["Schneller Teller", "Essen 1", "Essen 2", "Essen 3"],
            671: ["Essen 1", "Essen 2", "Essen 3", "Wochenangebot"], # two times Wochenangebot
            677: ["Essen 1", "Essen 2", "Essen 3"],
            681: ["Essen 1", "Essen 2"],
            722: ["Schneller Teller", "Essen 1", "Essen 2"],
            776: ["Essen 1", "Essen 2", "Essen 3"],
            9012: ["Essen 1", "Essen 2"]
        }

        self.customer_types = ["studierende", "angestellte", "gaeste", "schueler"]

        self.set_api_key(api_key)
        self.set_location_id(location_id)
        self.set_days(days)
        self.set_i18n(i18n)

        self.set_baseurl()
        self.xml = None

        self.menu_plan = None

    def __common_elements_in_lists(self, list1, list2):
        common_elements = set(list1).intersection(set(list2))
        return list(common_elements)

    def __convert_to_dict(self, xml):
        try:
            if isinstance(xml, str):
                root = ET.fromstring(xml)
            elif isinstance(xml, ET.Element):
                root = xml
            else:
                raise ValueError()

            # Wenn erfolgreich geparst, konvertiere zu einem Dictionary
            return xmltodict.parse(ET.tostring(root).decode('utf-8'))
        
        except (ValueError, ET.ParseError) as e:
            return xml

    def get_inner_dict(self, outer_dict, outer_key):
        return outer_dict.get(outer_key, {}) if isinstance(outer_dict, dict) else outer_dict

    def __remove_blank_lines(self, xml_string):
        while "\n\n" in xml_string:
            xml_string = xml_string.replace("\n\n", "\n")
        return xml_string
    
    def __remove_element_recursively(self, root, parent, tag):
        parents = root.findall('.//' + parent)
        for parent in parents:
            element = parent.find(tag)
            if element is not None:
                parent.remove(element)
        return root

    def get_menu_types(self):
        return dict(self.menu_types)
    
    def get_menu_type(self, id_or_name):
        if isinstance(id_or_name, str):
            return self.get_menu_type_by_name(id_or_name)
        elif isinstance(id_or_name, int):
            return self.get_menu_type_by_id(id_or_name)
    
    def get_menu_type_by_id(self, id):
        if id in self.get_menu_types():
            return self.get_menu_types()[id]
        else:
            raise Exception("ID {} for canteen does not exist".format(id))

    def get_customer_types(self):
        return self.customer_types

    def get_menu_type_by_name(self, name):
        return self.get_menu_type_by_id(self.get_location_id_by_name(name))
    
    def set_xml(self, xml_string=None):
        self.xml = self.__remove_blank_lines(self.__remove_element_recursively(ET.fromstring(xml_string), "menue", "nameMitUmbruch"))

    def get_xml(self):
        return self.xml
    
    def get_location_id_by_name(self, location_name):
        for id, name in self.get_locations().items():
            if name == location_name:
                return id
        raise Exception("Name {} for canteen does not exist".format(location_name))

    def get_location_name_by_id(self, location_id):
        for id, name in self.get_locations().items():
            if id == location_id:
                return name
        raise Exception("ID {} for canteen does not exist".format(location_id))

    def get_locations(self):
        return self.locations

    def set_location_id(self, location_id=None):
        if location_id is not None:
            for id, name in self.get_locations().items():
                if str(id) == str(location_id):
                    self.location_id = int(location_id)
                    return
            self.location_id = None
            raise Exception("ID {} for canteen does not exist".format(location_id))
        else:
            self.location_id = None

    def get_location_id(self):
        return self.location_id
    
    def set_location_id_by_location_name(self, location_name=None):
        for id, name in self.get_locations().items():
            if name == location_name:
                self.set_location_id(id)
                return
        raise Exception("Name {} for canteen does not exist".format(location_name))


    def set_days(self, days=None):
        if days is None:
            self.days = None
        else:
            if isinstance(days, int) and 1 <= days <= 6:
                self.days = days
            else:
                self.days = None

    def get_days(self):
        return self.days

    def set_baseurl(self):
        i18n_suffix = "en/" if self.get_i18n() else ""
        self.base_url = "https://www.swfr.de/{}apispeiseplan?&type={}&tx_speiseplan_pi1[apiKey]={}".format(i18n_suffix, self.type, self.get_api_key())

    def get_baseurl(self):
        return self.base_url

    def set_i18n(self, i18n=False):
        self.i18n = i18n

    def get_i18n(self):
        return self.i18n

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_api_key(self):
        return self.api_key
    
    def get_menu_plan_from_xml_interface(self, location_id=None, days=None, i18n=False):
        # Resetting for multiple use
        if location_id is not None:
            self.set_location_id(location_id)
        
        if days is not None:
            self.set_days(days)

        if i18n is not None:
            self.set_i18n(i18n)

        self.set_baseurl()

        url = self.get_baseurl()

        if location_id is not None:
            url += "&tx_speiseplan_pi1[ort]={}".format(location_id)

        if days is not None:
            url += "&tx_speiseplan_pi1[tage]={}".format(days)

        response = requests.get(url)

        if response.status_code == 200:
            self.set_xml(response.text)
        else:
            raise Exception("Error {}: {}".format(response.status_code, response.text))
        
        return self.get_xml()
    
    def get_menu_plan_from_xml(self, location=None):
        if location in self.get_locations().items():
            if isinstance(location, int):
                return self.get_menu_plan_from_xml_by_location_id(location)
            elif isinstance(location, str):
                return self.get_menu_from_menu_plan_by_name(location)
        return None

    def get_menu_plan_from_xml_by_location_id(self, location_id=641):
        for location in self.get_xml().findall('.//ort'):
            if location.get('id') == str(location_id):
                return self.__convert_to_dict(location)
        return None

    def get_menu_plan_from_xml_by_location_name(self, location_name="Mensa Furtwangen"):
        for location in self.get_xml().findall('.//ort'):
            if location.find('mensa').text == str(location_name):
                return self.__convert_to_dict(location)
        return None
    """
    def get_menu_plan_from_xml_by_day(self, day=1):
        today = datetime.now()

        if day <= 1:
            search_date = today
        else:
            if day in range(2,8):
                search_date = today + timedelta(days=day-1)
            else:
                search_date = today + timedelta(days=6)
    """

    def get_menu_from_menu_plan(self, location=None, menu_type="Essen 1", schedule_date=datetime.now().strftime("%d.%m.%Y")):
        if isinstance(location, int):
            location_id = location
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_id(location_id), pretty=True))
        elif isinstance(location, str):
            location_id = self.get_location_id_by_name(location)
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_name(location), pretty=True))
        elif isinstance(location, dict):
            location_id = list(location.keys())[0]
            location_plan = ET.fromstring(xmltodict.unparse(location, pretty=True))
        elif isinstance(location, None):
            location_id = self.get_location_id()
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_id(location_id), pretty=True))

        if menu_type in self.get_menu_types()[location_id]:
            for daily_schedule in location_plan.findall('.//tagesplan[@datum="{}"]'.format(schedule_date)):
                for menu in daily_schedule.findall('.//menue[@art="{}"]'.format(menu_type)):
                    return self.__convert_to_dict(menu)
        return None

    def get_menus_from_menu_plan(self, location=None, menu_types=["Essen 1"], schedule_date=datetime.now().strftime("%d.%m.%Y")):
        if isinstance(location, int):
            location_id = location
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_id(location_id), pretty=True))
        elif isinstance(location, str):
            location_id = self.get_location_id_by_name(location)
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_name(location), pretty=True))
        elif isinstance(location, dict):
            location_id = list(location.keys())[0]
            location_plan = ET.fromstring(xmltodict.unparse(location, pretty=True))
        elif isinstance(location, None):
            location_id = self.get_location_id()
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_id(location_id), pretty=True))

        result_menus = []

        menu_types = self.__common_elements_in_lists(menu_types, self.get_menu_types()[location_id])

        for daily_schedule in location_plan.findall('.//tagesplan[@datum="{}"]'.format(schedule_date)):
            for menu_type in menu_types:
                for menu in daily_schedule.findall('.//menue[@art="{}"]'.format(menu_type)):
                    result_menus.append(self.__convert_to_dict(menu))

        return result_menus
    
    def get_menu_prices_from_menu_plan(self, menus):
        if isinstance(menus, list):
            list = ET.fromstring(xmltodict.unparse(menus, pretty=True))

        prices = {}

        for menu_element in menus.findall('.//menue'):
            menu_type = menu_element.get('art')
            prices[menu_type] = self.__convert_to_dict(menu_element.find('.//preis'))

        return prices
    
    def get_menu_prices_from_menu_plan_by_customer_type(self, menus, customer_type="studierende"):
        if isinstance(menus, list):
            list = ET.fromstring(xmltodict.unparse(menus, pretty=True))

        prices = {}

        for menu_element in menus.findall('.//menue'):
            menu_type = menu_element.get('art')
            prices[menu_type] = menu_element.find('.//preis/{}'.format(customer_type)).text

        return prices
    
    def get_pupil_menu_prices_from_menu_plan(self, menu):
        return self.get_menu_prices_from_menu_plan_by_customer_type(menu, "schueler")
    
    def get_student_menu_prices_from_menu_plan(self, menu):
        return self.get_menu_prices_from_menu_plan_by_customer_type(menu, "studierende")
    
    def get_employee_menu_prices_from_menu_plan(self, menu):
        return self.get_menu_prices_from_menu_plan_by_customer_type(menu, "angestellte")
    
    def get_guest_menu_prices_from_menu_plan(self, menu):
        return self.get_menu_prices_from_menu_plan_by_customer_type(menu, "gaeste")
    
    def get_menu_price_from_menu(self, menu):
        if isinstance(menu, dict):
            menu = ET.fromstring(xmltodict.unparse(menu, pretty=True))

        price_element = menu.find('.//preis')
        return self.__convert_to_dict(price_element)

    def get_menu_price_from_menu_by_customer_type(self, menu, customer_type="studierende"):
        if customer_type in self.get_customer_types():
            if isinstance(menu, dict):
                menu = ET.fromstring(xmltodict.unparse(menu, pretty=True))
            
            price_element = menu.find('.//preis/{}'.format(customer_type))
            return self.__convert_to_dict(price_element.text) if price_element is not None else None
        else:
            return None
        
    def get_pupil_menu_price_from_menu(self, menu):
        return self.get_menu_price_from_menu_by_customer_type(menu, "schueler")
    
    def get_student_menu_price_from_menu(self, menu):
        return self.get_menu_price_from_menu_by_customer_type(menu, "studierende")
    
    def get_employee_menu_price_from_menu(self, menu):
        return self.get_menu_price_from_menu_by_customer_type(menu, "angestellte")
    
    def get_guest_menu_price_from_menu(self, menu):
        return self.get_menu_price_from_menu_by_customer_type(menu, "gaeste")
    
    def additives_text_to_dict(self, additives_text):
        additives_list = additives_text.split(', ')
        additives_dict = {}

        for item in additives_list:
            parts = item.split(': ')
            if len(parts) == 2:
                key, value = parts
                additives_dict[key] = value

        return additives_dict

    def get_additives_from_menu(self, menu):
        if isinstance(menu, dict):
            menu = ET.fromstring(xmltodict.unparse(menu, pretty=True))

        additives_element = menu.find('.//kennzeichnungen')
        additives_text = additives_element.text if additives_element is not None else None

        if additives_text:
            additives_dict = self.additives_text_to_dict(additives_text)
            return additives_dict

        return None

    def get_allergens_from_menu(self, menu):
        if isinstance(menu, dict):
            menu = ET.fromstring(xmltodict.unparse(menu, pretty=True))

        allergens_element = menu.find('.//allergene')
        return self.__convert_to_dict(allergens_element.text) if allergens_element is not None else None

    def get_daily_schedule(self, location=None, schedule_date=datetime.now().strftime("%d.%m.%Y")):
        if isinstance(location, int):
            location_id = location
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_id(location_id), pretty=True))
        elif isinstance(location, str):
            location_id = self.get_location_id_by_name(location)
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_name(location), pretty=True))
        elif isinstance(location, dict):
            location_id = list(location.keys())[0]
            location_plan = ET.fromstring(xmltodict.unparse(location, pretty=True))
        elif isinstance(location, None):
            location_id = self.get_location_id()
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_id(location_id), pretty=True))

        schedule_element = location_plan.find('.//tagesplan[@datum="{}"]'.format(schedule_date))
        return self.__convert_to_dict(schedule_element) if schedule_element is not None else None
    
    def get_schedule_plans(self, location=None, start_date=datetime.now().strftime("%d.%m.%Y"), num_days=6):
        if isinstance(location, int):
            location_id = location
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_id(location_id), pretty=True))
        elif isinstance(location, str):
            location_id = self.get_location_id_by_name(location)
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_name(location), pretty=True))
        elif isinstance(location, dict):
            location_id = list(location.keys())[0]
            location_plan = ET.fromstring(xmltodict.unparse(location, pretty=True))
        elif isinstance(location, None):
            location_id = self.get_location_id()
            location_plan = ET.fromstring(xmltodict.unparse(self.get_menu_plan_from_xml_by_location_id(location_id), pretty=True))

        schedule_plans = []
        current_date = datetime.strptime(start_date, "%d.%m.%Y")

        if days > 6:
            days = 6

        for _ in range(num_days):
            schedule_element = location_plan.find('.//tagesplan[@datum="{}"]'.format(current_date.strftime("%d.%m.%Y")))
            if schedule_element is not None:
                schedule_plans.append(self.__convert_to_dict(schedule_element))
            current_date += timedelta(days=1)

        return schedule_plans

if __name__ == "__main__":
    pass
