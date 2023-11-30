from csv_to_xml_converter import CSVtoXMLConverter

if __name__ == "__main__":
    converter = CSVtoXMLConverter("../data/aviation_accidents.csv")
    print(converter.to_xml_str())
    nome= "arquivo.xml"
    converter.salvar_xml_em_arquivo(nome)
