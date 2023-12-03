import xml.etree.ElementTree as ET


class Disaster:
    def __init__(self, date, aircraft_type, operator, fatalities):
        self._date = date
        self._aircraft_type = aircraft_type
        self._operator = operator
        self._fatalities = fatalities

    def to_xml(self):
        el = ET.Element("Disaster")
        el.set("Date", self._date)
        el.set("Aircraft Type", self._aircraft_type)
        el.set("Operator", self._operator)
        el.set("Fatalities", self._fatalities)
        return el