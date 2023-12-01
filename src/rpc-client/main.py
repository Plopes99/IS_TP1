import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://rpc-server:9000')

while True:
    print("\n")
    print("*************DESASTRES AÉREOS**************")
    print("**---------------------------------------**")
    print("** 1-Transformar CSV em XML              **")
    print("**---------------------------------------**")
    print("** 2-Validar o XML e importar o ficheiro **")
    print("**---------------------------------------**")
    print("** 3-Queries                             **")
    print("**---------------------------------------**")
    print("** 4-Saída                               **")
    print("*******************************************")
    print("\n")
    opcao = str(input("Selecione Opcao: "))

    if (opcao == '1'):
        print(server.to_xml_str())
        xml_data = server.get_xml_data()

        xml_path = "arquivo.xml"
        with open(xml_path, 'w') as arquivo:
            arquivo.write(xml_data)

    elif (opcao == '2'):
        print("A VALIDAR")
        xml_path = "arquivo.xml"
        result = server.validate_xml(xml_path)

        nome = input("NOME DO FICHEIRO A GUARDAR: ")
        result_data= server.import_documents(nome, xml_path)
        print("\nSUCESSO\n")
        print(result_data)

        if result:
            print('Válido! :)')
        else:
            print('Não válido! :(')

    elif (opcao == '3'):
        print("\n")
        print("************************QUERIES************************")
        print("**---------------------------------------------------**")
        print("** 1- Número de Desastres por Ano:                   **")
        print("**---------------------------------------------------**")
        print("** 2- Contagem de Desastres por Tipo de Aeronave:    **")
        print("**---------------------------------------------------**")
        print("** 3- Número de desastres desde 1927 até 2022:       **")
        print("**---------------------------------------------------**")
        print("*******************************************************")
        print("\n")
        opcao2 = str(input("Selecione Opcao: "))

        if (opcao2 == '1'):
            try:
                year_disasters = server.get_disaster_by_year()
                print("Número de Desastres por Ano")
                for row in year_disasters:
                    print(f"Year: {row[0]}, Disaster Count: {row[1]}")
            except RuntimeError as error:
                print(f"Error: {error}")

        elif (opcao2 == '2'):
            try:
                airplane_disasters = server.get_disaster_count_by_aircraft_type()
                print("Contagem de Desastres por Tipo de Aeronave:")
                for row in airplane_disasters:
                    print(f"Aircraft Type: {row[0]}, Disaster Count: {row[1]}")
            except RuntimeError as error:
                print(f"Error: {error}")

        elif (opcao2 == '3'):
            try:
                disaster_count_by_type = server.get_disasters_number()
                print("Número de desastres desde 1927 até 2022:")
                print(disaster_count_by_type)
            except RuntimeError as error:
                print(f"Error: {error}")

        elif(opcao == '4'):
            print("ESPEREMOS QUE NÃO HAJA MAIS DESASTRES")
            break

    else:
        print("OPÇÃO INVALIDA")