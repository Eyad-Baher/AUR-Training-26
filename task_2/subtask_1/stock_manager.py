def loadFile():
    stock=[]

    try:
        with open('stock.txt','r') as f:
            for i,line in enumerate(f):
                line=line.strip()
                if not line:
                    continue
                try:
                    key,value=line.split(",")
                    item={}
                    item['id']=i+1
                    item['item']=key.strip().lower()
                    item['value']=int(value.strip())
                    stock.append(item)
                except ValueError:
                    print(f'Skipping corrupted line: {line}')
        return stock
    except FileNotFoundError:
        print('File not found')
        return []


def saveFile(stock):
    with open('stock.txt','w') as f:
        for item in stock:
            f.write(f"{item['item']},{item['value']}\n")


def menu(stock):
    while(1):
        print('enter 1 to add stock')
        print('enter 2 to remove stock')
        print('enter 3 to show stock\'s contents')
        print('enter 4 to exit the program')

        choice=input('Enter your choice: ').strip()

        if not choice.isdigit() or int(choice) not in [1,2,3,4]:
            print('INVALID CHOICE.\nReenter your choice.')
            continue

        choice=int(choice)

        match choice:
            case 1:
                addStock(stock)
            case 2:
                removeStock(stock)
            case 3:
                viewProducts(stock)
            case 4:
                saveFile(stock)
                print('Thank you for using the program.')
                break


def addStock(stock):

    item_names=[]
    id_all=[]
    for item in stock:
        print(f'{item['id']}. {item['item']}: {item['value']}')

    item_names=[item['item'] for item in stock]
    id_all=[item['id'] for item in stock]

    while True:

        id_raw=input('Enter the id of the item you want to change or its name: ').strip().lower()

        if id_raw.isdigit():
            id_num=int(id_raw)
            if id_num not in id_all:
                print('Invalid Id.\n')
                continue
            else:
                item_match=[i for i in stock if i['id']==id_num]
                id_name=item_match[0]['item']
                break

        else:
            id_name=id_raw
            break

    while True:

        amount=input(f'Enter the amount to add to the item {id_name}: ').strip()
        if amount.isdigit():
            amount=int(amount)
            break

        print(f'Invalid stock amount.')

    flag=False
    for entry in stock:
        if entry['item']== id_name:
            entry['value']+=amount
            flag=True
            break

    if flag== False:
            new_item={}

            new_id=max(id_all,default=0)+1
            new_item['id']=new_id
            new_item['item']=id_name
            new_item['value']=amount

            stock.append(new_item)


def removeStock(stock):
    item_names=[]
    id_all=[]
    for item in stock:
        print(f'{item['id']}. {item['item']}: {item['value']}')

    item_names=[item['item'] for item in stock]
    id_all=[item['id'] for item in stock]

    while True:
        id_raw=input('Enter the id of the item you want to change or its name: ').strip().lower()

        if id_raw.isdigit():
            id_num=int(id_raw)
            if id_num not in id_all:
                print('Invalid Id.\n')
                continue
            else:
                item_match=[i for i in stock if i['id']==id_num]
                id_name=item_match[0]['item']
                break

        else:
            id_name=id_raw
            if id_name in item_names:
                break
            else:
                print('INVALID ITEM')
                continue

    while True:

        amount=input(f'Enter the amount to remove from the item {id_name}: ').strip()
        if amount.isdigit():
            amount=int(amount)
            break

        print(f'Invalid stock amount.')

    for entry in stock:
        if entry['item']== id_name:
            if amount>entry['value']:
                print(f'Cannot remove {amount}, only {entry["value"]} in stock.')
            else:
                entry['value']-=amount
            break


def viewProducts(stock):

    for item in stock:
        print(f'{item['id']}. {item['item']}: {item['value']}')


stock=loadFile()

menu(stock)