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
        print("****************QUERIES****************")
        print("**-----------------------------------**")
        print("** 1-                **")
        print("**-----------------------------------**")
        print("** 2-             **")
        print("**-----------------------------------**")
        print("** 3-                **")
        print("**-----------------------------------**")
        print("***************************************")
        print("\n")
        opcao2 = str(input("Selecione Opcao: "))

        if (opcao2 == '1'):
            for x in server.query1():
                print(x)

        elif (opcao2 == '2'):
            for x in server.query2():
                print(x)

        elif (opcao2 == '3'):
            #NAO DA
            nome_pais = input('Introduza o nome do pais a procurar: \n')
            for x in server.query3(nome_pais):
                print(x)

        elif(opcao == '4'):
            print("ESPEREMOS QUE NÃO HAJA MAIS DESASTRES")
            pass

    else:
        print("OPÇÃO INVALIDA")