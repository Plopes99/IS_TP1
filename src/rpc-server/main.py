import signal
import sys




from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer

from functions.string_length import string_length
from functions.string_reverse import string_reverse
from functions.csv_to_xml_converter import CSVtoXMLConverter
from functions.validator import validator
from functions.xml_data_manipulation import get_disaster_by_year, get_disasters_number, get_disaster_count_by_aircraft_type
from functions.import_documents import import_documents

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
    server.register_function(import_documents, 'import_documents.py')
    server.register_function(get_disaster_by_year)
    server.register_function(get_disaster_count_by_aircraft_type)
    server.register_function(get_disasters_number)


    # start the server
    print("Starting the RPC Server...")
    server.serve_forever()
