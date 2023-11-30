import signal
import sys
from datetime import datetime
import xml.etree.ElementTree as ET

import psycopg2
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer

from functions.string_length import string_length
from functions.string_reverse import string_reverse
from functions.csv_to_xml_converter import CSVtoXMLConverter
from functions.validator import validator


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


with SimpleXMLRPCServer(('rpc-server', 9000), requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()


    def signal_handler(signum, frame):
        print("received signal")
        server.server_close()

        print("exiting, gracefully")
        sys.exit(0)


    def get_converter():
        return CSVtoXMLConverter("../data/aviation_accidents.csv")

    def to_xml_str():
        return get_converter().to_xml_str()


    def get_xml_data():
        return get_converter().to_xml_str()

    def validate_xml(xml_path: str):
        xsd_path="xml_schema.xsd"
        return validator(xml_path,xsd_path)

    def import_documents(file_name, xml_file):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user="is",
                                          password="is",
                                          host="is-db",
                                          port="5432",
                                          database="is")

            cursor = connection.cursor()

            with open(xml_file, encoding='utf-8') as file:
                data = file.read()
                cursor.execute("INSERT INTO imported_documents(file_name, xml) VALUES(%s,%s)", (file_name, data))

                tree = ET.parse(xml_file)
                root = tree.getroot()
                for category_elem in root.findall('.//category'):
                    category_name = category_elem.attrib.get('name', '')
                    accidents_types = category_elem.attrib.get('accident_type', '')
                    damage_types = category_elem.attrib.get('damage_type', '')

                    # Insira na tabela airplane_disasters
                    cursor.execute(
                        "INSERT INTO airplane_disasters (category_name, accidents_types, damage_types) VALUES (%s, %s, %s) RETURNING id",
                        (category_name, accidents_types, damage_types)
                    )
                    category_id = cursor.fetchone()[0]

                    for country_elem in category_elem.findall('.//country'):
                        country_name = country_elem.attrib.get('name', '')

                        # Insira na tabela countries
                        cursor.execute(
                            "INSERT INTO countries (country_name, category_id) VALUES (%s, %s) RETURNING id",
                            (country_name, category_id)
                        )
                        country_id = cursor.fetchone()[0]

                        for disaster_elem in country_elem.findall('.//disaster'):
                            date_elem = disaster_elem.find('date')
                            aircraft_type_elem = disaster_elem.find('aircraft_type')
                            operator_elem = disaster_elem.find('operator')
                            fatalities_elem = disaster_elem.find('fatalities')

                            # Verifica se os elementos estão presentes antes de acessar seus atributos
                            date_text = date_elem.attrib.get('text', '') if date_elem is not None else ''
                            aircraft_type_text = aircraft_type_elem.attrib.get('text','') if aircraft_type_elem is not None else ''
                            operator_text = operator_elem.attrib.get('text', '') if operator_elem is not None else ''
                            fatalities_text = fatalities_elem.attrib.get('text', '') if fatalities_elem is not None else ''

                            # Converte a data para o formato adequado
                            try:
                                # Converte a data para o formato adequado
                                date = datetime.strptime(date_text, "%d-%b-%Y").date() if date_text else None
                            except ValueError:
                                # Caso a conversão falhe, defina a data como nula (NULL)
                                date = None

                            # Converte as fatalidades para um valor inteiro (se disponível)
                            fatalities = int(fatalities_text) if fatalities_text and fatalities_text.isdigit() else None

                            # Insira na tabela disasters
                            cursor.execute(
                                "INSERT INTO disasters (date, aircraft_type, operator, fatalities, country_id) "
                                "VALUES (%s, %s, %s, %s, %s)",
                                (date, aircraft_type_text, operator_text, fatalities,  country_id)
                            )

                connection.commit()

        except (Exception, psycopg2.Error) as error:
            error_message = f"Failed to fetch data: {error}"
            if hasattr(error, 'pgcode') and hasattr(error, 'pgerror'):
                error_message += f" (PGCode: {error.pgcode}, PGError: {error.pgerror})"

            return error_message

        finally:
            if connection:
                cursor.close()
                connection.close()



    # signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # register both functions
    server.register_function(string_reverse)
    server.register_function(string_length)
    server.register_function(get_converter, 'get_converter')
    server.register_function(to_xml_str, 'to_xml_str')
    server.register_function(get_xml_data, 'get_xml_data')
    server.register_function(validate_xml, 'validate_xml')
    server.register_function(import_documents, 'import_documents')

    # start the server
    print("Starting the RPC Server...")
    server.serve_forever()
