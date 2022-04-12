#******************************code starts here ******************************

#C.S. PROJECT (VIKAS,MEET,DREAM)

import sys
import os
import datetime
import random
import time
import getpass
import mysql.connector as mc
import matplotlib.pyplot as pl

#print text slowly
def print_slow(t,s=0.01):
    for y in t:
        sys.stdout.write(y)
        sys.stdout.flush()
        time.sleep(s)
    print('')

#display title
def title(t):
    col,lin=os.get_terminal_size()
    print('\n' + '='*(col) + '\n' +
          ' '*int((col-len(t)-31)/4)+
          'DATE : '+datetime.datetime.now().strftime("%d-%m-%y")+
          ' '*int((col-len(t)-31)/4)+
          '# '+t+' #'+
          ' '*int((col-len(t)-31)/4)+
          'TIME - '+ datetime.datetime.now().strftime("%H:%M")+
          ' '*int((col-len(t)-31)/4)+
          '\n' + '='*(col)+'\n')

#to print a heading
def heading(t):
    col,lin=os.get_terminal_size()
    print('-'*int((col-len(t)-4)/2) + '\ '+t+' /' \
          +'-'*(int((col-len(t)-4)/2))+'\n')

#standardising lengths of strings
def cut(s,n):
    s=str(s)
    if len(s)>n:
        return(s[:n])
    elif len(s)==n:
        return s
    else:
        return s+' '*(n-len(s))

#========================= MAIN PROGRAM FUNCTONS =============================

#MAIN MENU
def main_menu():
    os.system('cls')
    title(com_name)
    heading('MAIN MENU')
    print('''\
\t1       -->     Admin Portal
\t2       -->     Customer Portal
\t3       -->     Credits
\n\tEnter   -->     Exit
    ''')
    ch=input('\n\tEnter the choice: ')
    if ch=='1':
        admin_authentication()
    elif ch=='2':
        customer_portal()
    elif ch=='3':
        credit()
        main_menu()
    else:
        program_end()
    return

#========================= CUSTOMER PORTAL FUNCTONS ==========================

#CUSTOMER PORTAL
def customer_portal():
    os.system('cls')
    title(com_name)
    heading('CUSTOMER PORTAL')
    print('''\
\t1       -->     View Cars
\t2       -->     Rent Cars
\t3       -->     Return Cars
\n\tEnter   -->     Back
    ''')
    ch=input('\tEnter the choice: ')
    if ch=='1':
        view_cars_customer()
    elif ch=='2':
        rent_cars()
    elif ch=='3':
        return_cars()
    else:
        main_menu()
    return

#RENT CARS
def rent_cars():
    os.system('cls')
    title(com_name)
    heading('CUSTOMER PORTAL')
    heading('RENT CARS')

    #printing available cars
    cur=cn.cursor()
    cur.execute("select car_no,car_class,model_name,car_color,capacity,\
daily_rent from cars where car_status='AVAILABLE' order by Car_Class;")
    l=cur.fetchall()
    if len(l)==0:
        print_slow('\n\n\t\tSORRY! ALL CARS ARE CURRENTLY RENTED!!')
        print_slow('\n\t\tRedirecting to Customer Portal... Press Enter')
        input()
        customer_portal()
        return
    print('\tAVAIABLE CARS:\n')
    print('')
    sp=[15,15,20,15,15,15]
    z='+'
    for y in sp:
        z=z+'-'*(y+1)+'+'
    print(z)
    time.sleep(0.03)
    print('| ',cut('CAR_NO',15),'| ',\
            cut('CAR_CLASS',15),'| ',\
            cut('MODEL_NAME',20),'| ',\
            cut('CAR_COLOR',15),'| ',\
            cut('CAPACITY',15),'| ',\
            cut('DAILY_RENT',15),'| ',sep="")
    time.sleep(0.03)
    print(z)
    time.sleep(0.03)
    for y in range(0,len(l)):
        print('| ',end='')
        for x in range(0,len(l[y])):
            print(cut(l[y][x],sp[x]),end='')
            print('| ',end='')
        print('')
        time.sleep(0.03)
    print(z)
    
    #obtaining details & validation
    while True:
        cust_name=input('\n\tEnter your Full Name or \
enter 0 to go back: ') #full name
        if cust_name=='0':
            customer_portal()
            return
        if len(cust_name)!=0:
            break
        print_slow('\tPlease enter a name...')
        
    while True:
        cust_no=input('\n\tEnter your Phone Number: ') #phone number
        if len(cust_no)!=0 and cust_no.isdigit():
            break
        print_slow('\tPlease enter a phone number...')

    cur=cn.cursor()  #car_nos
    cur.execute("select car_no from cars where car_status='AVAILABLE'")
    l=cur.fetchall()
    while True:
        try:
            cars=input('\n\tEnter the car_nos of the cars you wish to rent \
separated by "," with no spaces: ')
            cars=cars.split(',')
            z='valid'
            for y in cars:
                x=(int(y),)
                if x not in l:
                    z='invalid'
            if z=='invalid':
                print_slow("\tPlease enter valid and available car_nos...")
                continue
            if len(set(cars))!=len(cars):
                print_slow('\tPlease enter unique entries only...')
                continue
            break
        except:
            print_slow('\tThere is some error, please enter car_nos again...')
            continue
        
    while True:   #days
        while True:
            days=input('\n\tEnter the no. of days you wish to borrow the car \
including today (max 15): ')
            if days.isdigit()==False:
                print_slow('\tPlease enter a number...')
                continue
            days=int(days)
            break
        if days in range(1,16):
            days=int(days)
            break
        print_slow("\tPlease enter valid no. of days...")

    while True:   #driver
        driver=input('\n\tWill you need a driver (y/n) \
[ Rs. 500 per day per car ]: ')
        if driver.lower() in ['y','n']:
            break
        print_slow('\tPlease enter valid answer...\n')

    #unique rent_id generation
    cur=cn.cursor()
    cur.execute('select rent_id from rentings;')
    l=cur.fetchall()
    while True:
        rent_id=random.randint(10000,100000)
        x=(rent_id,)
        if x in l:
            continue
        break
    
    #dates
    rent_date=datetime.datetime.now()
    return_date = rent_date + datetime.timedelta(days=days)
    rent_date=rent_date.strftime("%d-%m-%y")
    return_date=return_date.strftime("%d-%m-%y")

    #confirmation
    print_slow('\n\tEnter y to confirm your renting')
    print_slow('\tEnter anything else to cancel')
    an=input('\tAnswer : ')
    if an=='y':
        pass
    else:
        print_slow('\n\tRenting Cancelled....')
        print_slow('\n\tRedirecting to Customer Portal.... Press Enter')
        input()
        customer_portal()
        return

    #receipt table
    print_slow('\n\tRenting Confirmed, Redirecting to Receipt \
Table....Press Enter')
    input()

    os.system('cls')
    title(com_name)
    heading('CUSTOMER PORTAL')
    heading('RECEIPT TABLE')
    
    col,lin=os.get_terminal_size()
    L=[]
    n=30
    print(' '*n+'+'+'='*(col-2*n-2)+'+')
    L.append(com_name+' : RENT RECEIPT')
    L.append('='*(col-2*n-2))
    L.append('RENT-ID : '+str(rent_id))
    L.append('CUSTOMER NAME: '+cust_name.upper())
    L.append('-'*(col-2*n-2))
    t=datetime.datetime.now().strftime("%H:%M")
    L.append('RENT DATE & TIME: '+rent_date+' , '+t)
    L.append('RETURN DATE: '+return_date)
    L.append('DAYS RENTED: '+str(days))
    L.append('-'*(col-2*n-2))
    L.append('-:PROJECTED RENT:-')

    carz=[]
    total=0
    for car_no in cars:
        cur=cn.cursor()
        cur.execute('select daily_rent,model_name from cars where car_no={};'\
                    .format(car_no))
        x=cur.fetchall()
        model_name=x[0][1]
        x=x[0][0]
        rent=x*days
        total=total+(x*days)
        L.append('')
        L.append(model_name)
        L.append('CAR NO.'+str(y)+' --> '+str(x)+' * '+str(days)+' = '+\
                 str(x*days))
        if driver=='y':
            L.append('DRIVER --> 500 * '+str(days)+' = '+str(days*500))
            rent=rent+(days*500)
            total=total+(days*500)
        carz.append({'car_no':car_no,'rent':rent,'model':model_name})
    L.append('')
    L.append('-'*(col-2*n-2))
    L.append('TOTAL :- Rs.'+str(total))
    L.append('-'*(col-2*n-2))
    L.append('Please print this receipt and take it to our')
    L.append(com_name+' shop to get the cars')
    L.append('-'*(col-2*n-2))
    L.append('(:  HAVE A NICE DAY  :)')

    for y in L:
        sp=' '*n
        d1=' '*int((col-2*n-len(y)-2)/2)
        d2=' '*( col-2*n-2-len(y) - int((col-2*n-len(y)-2)/2) )
        print(sp+'|'+d1+y+d2+'|')
        time.sleep(0.1)
    print(' '*n+'+'+'='*(col-2*n-2)+'+')
    print('')

    #renting the cars
    cur=cn.cursor()
    for y in carz:
        q="insert into rentings values('{}','{}','{}','{}','{}','{}','{}','{}'\
,'{}');".format(rent_id,cust_name,cust_no,y['car_no'],y['model'],rent_date,\
                return_date,driver,y['rent'])
        cur.execute(q)
        q="update cars set rent_id={},car_status='{}' where car_no={};"\
           .format(rent_id,'RENTED',y['car_no'])
        cur.execute(q)
    cn.commit() 
    print_slow('\n\tCARS RENTED.... Press Enter to continue')
    input()

    #important note
    os.system('cls')
    title(com_name)
    heading('CUSTOMER PORTAL')
    heading('IMPORTANT NOTE')
    print('')
    print_slow('''
\t\tTHE CUSTOMER HAS TO TAKE THE RECEIPT TO THE OFFICE TO GET THE CARS!
\t\tTHE PRICE OF FUEL IS NOT INCLUDED IN THE RECEIPT!

\t\tTHE CARS CAN BE RETURED EARLIER, RENT WILL BE ADJUSTED!
\t\tDELAYED RETURNS WILL RESULT IN PENALTY!

\t\tIF ANY VEHICLE IS DAMAGED DUE TO CARELESSNESS OF CUSTOMER THE
\t\tCUSTOMER IS RESPONSIBLE TO PAY THE REPAIR EXPENSES!
''',0.002)
    
    print_slow('\t\tRedirecting to Customer Portal.... Press Enter')
    input()
    customer_portal()
    return
    
#RETURN CARS
def return_cars():
    os.system('cls')
    title(com_name)
    heading('CUSTOMER PORTAL')
    heading('RETURN CARS')

    cur=cn.cursor()
    cur.execute('select rent_id, cust_name,cust_phone_no,car_no,model_name \
from rentings order by return_date;')
    l=cur.fetchall()
    if len(l)==0:
        print_slow('\n\tNo cars to return...Press Enter to go back')
        input()
        customer_portal()
        return

    #printing table
    print('\tCurrent rentings: \n')
    sp=[10,20,15,10,20]
    z='+'
    for y in sp:
        z=z+'-'*(y+1)+'+'
    print(z)
    time.sleep(0.03)
    print('| '+cut('RENT_ID',10)+\
             '| '+cut('CUSTOMER_NAME',20)+\
             '| '+cut('PHONE NUMBER',15)+\
             '| '+cut('CAR_NO',10)+\
             '| '+cut('MODEL_NAME',20)+\
             '| ',sep='')
    time.sleep(0.03)
    print(z)
    time.sleep(0.03)
    for y in range(0,len(l)):
        print('| ',end='')
        for x in range(0,len(l[y])):
            print(cut(l[y][x],sp[x]),end='')
            print('| ',end='')
        print('')
        time.sleep(0.03)
    print(z)
    
    #validating
    rent_id=input('\n\tEnter the RENT_ID or enter "q" to go back: ')
    if rent_id in ['q','Q']:
        customer_portal()
        return
    if rent_id.isdigit()==False:
        print_slow('\n\tPlease enter a number......')
        time.sleep(0.5)
        return_cars()
        return
    cur=cn.cursor()
    cur.execute('select rent_id from rentings;')
    l=cur.fetchall()
    rent_id=int(rent_id)
    x=(rent_id,)
    if x not in l:
        print_slow('\n\tThis RENT_ID does not exist, enter again...')
        time.sleep(0.5)
        return_cars()
        return

    #confirmation
    print('\n\tEnter y to confirm your return')
    print('\tEnter anything else to cancel the return')
    an=input('\tAnswer : ')
    if an!='y':
        print_slow('\n\tReturn Cancelled....')
        print_slow('\n\tRedirecting to Customer Portal.... Press Enter')
        input()
        customer_portal()
        return
    print_slow('\n\tRedirecting to Bill Table.... Press Enter')
    input()

    #bill table
    os.system('cls')
    title(com_name)
    heading('CUSTOMER PORTAL')
    heading('BILL TABLE')

    #obtaining everything required for bill
    cur=cn.cursor()
    cur.execute('select cust_name,car_no,date_rented,driver,Cust_Phone_no,\
model_name from rentings where rent_id={};'.format(rent_id))
    l=cur.fetchall()
    cust_name=l[0][0]
    driver=l[0][3]
    phone=l[0][4]
    
    #dates
    rent_date    =  datetime.datetime.strptime(l[0][2],'%d-%m-%y')
    return_date  =  datetime.datetime.now()
    days         =  return_date-rent_date
    days         =  days.days+1
    rent_date    =  rent_date.strftime('%d-%m-%y')
    return_date  =  return_date.strftime('%d-%m-%y')

    #rent
    carz=[]
    for y in l:
        car_no=y[1]
        cur=cn.cursor()
        cur.execute('select daily_rent from cars where car_no={};'\
                    .format(car_no))
        rent=(cur.fetchall())[0][0]
        t={'car_no':car_no,'rent':rent,'model':y[5]}
        carz.append(t)
        del t

    #printing the bill
    col,lin=os.get_terminal_size()
    L=[]
    n=30
    total=0

    print(' '*n+'+'+'='*(col-2*n-2)+'+')
    L.append(com_name+' : BILL')
    L.append('='*(col-2*n-2))
    L.append('RENT-ID : '+str(rent_id))
    L.append('CUSTOMER NAME: '+cust_name.upper())
    L.append('-'*(col-2*n-2))
    L.append('RENT DATE: '+rent_date)
    t=datetime.datetime.now().strftime("%H:%M")
    L.append('RETURN DATE & TIME: '+return_date+' , '+t)
    L.append('DAYS RENTED: '+str(days))
    L.append('-'*(col-2*n-2))
    L.append('-:RENT TO BE PAID:-')
    
    for y in carz:
        L.append('')
        L.append(y['model'])
        L.append('CAR NO.'+str(y['car_no'])+' --> '+str(y['rent'])\
                 +' * '+str(days)+' = '+str(y['rent']*days))
        total = total + y['rent']*days
        if driver=='y':
            L.append('DRIVER --> 500 * '+str(days)+' = '+str(days*500))
            total = total + days*500
    L.append('')
    L.append('-'*(col-2*n-2))
    L.append('TOTAL :- Rs.'+str(total))
    L.append('-'*(col-2*n-2))
    L.append('Kindly pay this amount')
    L.append('And return the cars back')
    L.append('-'*(col-2*n-2))
    L.append('THANK YOU FOR CHOOSING US')
     
    for y in L:
        sp=' '*n
        d1=' '*int((col-2*n-len(y)-2)/2)
        d2=' '*( col-2*n-2-len(y) - int((col-2*n-len(y)-2)/2) )
        print(sp+'|'+d1+y+d2+'|')
        time.sleep(0.1)
        
    print(' '*n+'+'+'='*(col-2*n-2)+'+')
    print('')
    
    #updating sales table
    for y in carz:
        cur=cn.cursor()
        q="insert into sales values('{}','{}','{}','{}','{}','{}','{}','{}');"\
           .format(rent_id,y['car_no'],y['model'],cust_name,phone,rent_date\
                   ,return_date,(y['rent'])*days)
        cur.execute(q)
        cn.commit()

    #returning
    cur=cn.cursor()
    cur.execute('delete from rentings where rent_id={};'.format(rent_id))
    cur=cn.cursor()
    cur.execute("update cars set car_status='{}', rent_id={} where \
rent_id={};".format('AVAILABLE','NULL',rent_id))
    cn.commit()
    print_slow('\n\tCARS RETURNED....')
    print_slow('\n\tRedirecting to Customer Portal.... Press Enter')
    input('')
    customer_portal()
    return

#VIEW CARS CUSTOMER
def view_cars_customer():
    os.system('cls')
    title(com_name)
    heading('CUSTOMER PORTAL')
    heading('VIEW CARS')

    cur=cn.cursor()
    cur.execute('select car_no,car_class,model_name,car_color,\
capacity,daily_rent,car_status from cars order by Car_Class;')
    l=cur.fetchall()   
    if len(l)==0:
        print_slow('\n\tNo cars available in the store! Press enter to go \
back!')
        input()
        customer_portal
        return
    
    #printing table
    print('')
    sp=[15,15,20,15,15,15,15]
    z='+'
    for y in sp:
        z=z+'-'*(y+1)+'+'
    print(z)
    time.sleep(0.03)
    print('| ',cut('CAR_NO.',15),'| ',\
            cut('CAR_CLASS',15),'| ',\
            cut('MODEL_NAME',20),'| ',\
            cut('CAR_COLOR',15),'| ',\
            cut('CAPACITY',15),'| ',\
            cut('DAILY_RENT',15),'| ',\
            cut('CAR_STATUS',15),'|  ',sep="")
    time.sleep(0.03)
    print(z)
    time.sleep(0.03)
    for y in range(0,len(l)):
        print('| ',end='')
        for x in range(0,len(l[y])):
            print(cut(l[y][x],sp[x]),end='')
            print('| ',end='')
        print('')
        time.sleep(0.03)
    print(z)      
    input('\n\tPress ENTER to go back')
    customer_portal()
    return

#=========================== ADMIN PORTAL FUNCTONS ===========================

#ADMIN AUTHENTICATION
def admin_authentication():
    os.system('cls')
    title(com_name)
    heading('ADMIN AUTHENTICATION')
    Pass=getpass.getpass("\tEnter Password: ")

    #password
    cur=cn.cursor()
    cur.execute('select * from admins')
    l=cur.fetchall()
    passwd=l[0][0]
    if passwd==Pass:
        print_slow('\n\tAccess Granted ..... Press Enter')
        input('')
        admin_portal()
    else:
        print_slow('\n\tAccess Denied .....')
        print('\n\tPress Enter to try again \n\tOR \
Enter anything else to go back')
        z=input('')
        if len(z)==0:
            admin_authentication()
        else:
            main_menu()    
    return

#ADMIN PORTAL
def admin_portal():
    os.system('cls')
    title(com_name)
    heading('ADMIN PORTAL')
    print('''\
\t1       -->     Open Garage
\t2       -->     View Current Rentings
\t3       -->     View Sales Table
\t4       -->     View Sales Graph
\n\tEnter   -->     Back
    ''')
    ch=input('\tEnter the choice: ')
    if ch=='1':
        garage()
    elif ch=='2':
        view_current_rentings()
    elif ch=='3':
        view_sales_table()
    elif ch=='4':
        sales_graph()
    else:
        main_menu()
    return

#VIEW CURRENT RENTINGS
def view_current_rentings():
    os.system('cls')
    title(com_name)
    heading('ADMIN PORTAL')
    heading('CURRENT RENTINGS')

    cur=cn.cursor()
    cur.execute('select * from rentings order by return_date,rent_id;')
    l=cur.fetchall()
    if len(l)==0:
        print_slow('\n\tNo cars rented currently!, Press enter to go back')
        input()
        admin_portal()
        return

    #printing table
    sp=[8,17,15,7,20,12,12,6,10]
    z='+'
    for y in sp:
        z=z+'-'*(y+1)+'+'
    print(z)
    time.sleep(0.03)
    print('| '+cut('RENT_ID',8)+\
             '| '+cut('CUSTOMER_NAME',17)+\
             '| '+cut('PHONE NUMBER',15)+\
             '| '+cut('CAR_NO',7)+\
             '| '+cut('MODEL_NAME',20)+\
             '| '+cut('DATE_RENTED',12)+\
             '| '+cut('RETURN_DATE',12)+\
             '| '+cut('DRIVER',6)+\
             '| '+cut('TOTAL_RENT',10)+\
             '| ',sep='')
    time.sleep(0.03)
    print(z)
    time.sleep(0.03)
    for y in range(0,len(l)):
        print('| ',end='')
        for x in range(0,len(l[y])):
            print(cut(l[y][x],sp[x]),end='')
            print('| ',end='')
        print('')
        time.sleep(0.03)
    print(z)
    input('\n\tPress ENTER to go back')
    admin_portal()
    return

#VIEW SALES TABLE
def view_sales_table():
    os.system('cls')
    title(com_name)
    heading('ADMIN PORTAL')
    heading('SALES TABLE')

    cur=cn.cursor()
    cur.execute('select * from sales order by return_date desc,rent_id;')
    l=cur.fetchall()
    if len(l)==0:
        print_slow('\n\tNo sales to show!, Press enter to go back')
        input()
        admin_portal()
        return

    #printing table
    sp=[10,10,20,20,15,10,12,10]
    z='+'
    for y in sp:
        z=z+'-'*(y+1)+'+'
    print(z)
    time.sleep(0.03)
    print('| '+cut('RENT_ID',10)+\
             '| '+cut('CAR_NO',10)+\
             '| '+cut('MODEL NAME',20)+\
             '| '+cut('CUST_NAME',20)+\
             '| '+cut('PHONE_NUMBER',15)+\
             '| '+cut('RENT_DATE',10)+\
             '| '+cut('RETURN_DATE',12)+\
             '| '+cut('SALES',10)+\
             '| ',sep='')
    time.sleep(0.03)
    print(z)
    time.sleep(0.03)
    for y in range(0,len(l)):
        print('| ',end='')
        for x in range(0,len(l[y])):
            print(cut(l[y][x],sp[x]),end='')
            print('| ',end='')
        print('')
        time.sleep(0.03)
    print(z)
    input('\n\tPress ENTER to go back')
    admin_portal()
    return

#SALES_GRAPH
def sales_graph():
    os.system('cls')
    title(com_name)
    heading('ADMIN PORTAL')
    heading('SALES GRAPH')

    print('''\
\t1       -->     Car wise
\t2       -->     Date wise
\n\tEnter   -->     Back
    ''')
    ch=input('\tEnter the choice: ')
    if ch=='1':
        cur=cn.cursor()
        cur.execute('select model_name,sum(sales) from sales group by model_name;')
        data=cur.fetchall()
        cars,sales=[],[]
        for y in data:
            cars.append(y[0])
            sales.append(y[1])
        pl.barh(cars,sales,color='red')
        pl.xlabel('Cars')
        pl.ylabel('Sales in Rs.')
        pl.title(com_name+' - CAR WISE SALES')
        pl.show()
        sales_graph()
        return
    elif ch=='2':
        cur=cn.cursor()
        cur.execute('select return_date,sum(sales) from sales group by return_date;')
        data=cur.fetchall()
        date,sales=[],[]
        for y in data:
            date.append(y[0])
            sales.append(y[1])
        pl.plot(date,sales,'b',linewidth=3)
        pl.xlabel('Date')
        pl.ylabel('Sales in Rs.')
        pl.title(com_name+' - DATE WISE SALES')
        pl.show()
        sales_graph()
        return    
    else:
        admin_portal()
        return
            
#GARAGE
def garage():
    os.system('cls')
    title(com_name)
    heading('ADMIN PORTAL')
    heading('GARAGE')
    print('''\
\t1       -->     View Cars
\t2       -->     Add Car
\t3       -->     Remove Car
\n\tEnter   -->     Back
    ''')
    ch=input('\tEnter the choice: ')
    if ch=='1':
        view_cars_admin()
    elif ch=='2':
        add_car()
    elif ch=='3':
        remove_car()
    else:
        admin_portal()
    return

#VIEW CARS ADMIN
def view_cars_admin():
    os.system('cls')
    title(com_name)
    heading('ADMIN PORTAL')
    heading('GARAGE')
    heading('VIEW CARS')

    cur=cn.cursor()
    cur.execute('select * from cars order by Car_Class;')
    l=cur.fetchall()
    if len(l)==0:
        print_slow('\n\tGarage empty! Press enter to go back!')
        input()
        garage()
        return

    #printing table
    print('')
    sp=[10,15,20,15,10,15,15,10]
    z='+'
    for y in sp:
        z=z+'-'*(y+1)+'+'
    print(z)
    time.sleep(0.03)
    print('| ',cut('CAR_NO',10),'| ',\
            cut('CAR_CLASS',15),'| ',\
            cut('MODEL_NAME',20),'| ',\
            cut('CAR_COLOR',15),'| ',\
            cut('CAPACITY',10),'| ',\
            cut('DAILY_RENT',15),'| ',\
            cut('CAR_STATUS',15),'| ',\
            cut('RENT_ID',10),'| ',sep="")
    time.sleep(0.03)
    print(z)
    time.sleep(0.03)
    for y in range(0,len(l)):
        print('| ',end='')
        for x in range(0,len(l[y])):
            print(cut(l[y][x],sp[x]),end='') 
            print('| ',end='')
        print('')
        time.sleep(0.03)
    print(z)       
    input('\n\tPress ENTER to go back to Garage')
    garage()
    return
        
#ADD CAR
def add_car():
    os.system('cls')
    title(com_name)
    heading('ADMIN PORTAL')
    heading('GARAGE')
    heading('ADD CAR')

    #fetching details
    cur=cn.cursor()
    cur.execute('select car_no from cars;')
    l=cur.fetchall()
    while True:
        car_no=input('\n\tEnter the car number or enter "q" to go back: ')
        if car_no in ['q','Q']:
            garage()
            return
        elif car_no.isdigit()==False:
            print_slow('\tPlease enter a number...')
            continue
        if len(car_no)!=4:
            print_slow('\tPlease enter a 4-digit number...')
            continue
        car_no=int(car_no)
        x=(car_no,)
        if x in l:
            print_slow('\tThe car_no you entered is already in use..\
Enter again')
            continue
        break
    while True:
        car_class=input('\n\tEnter the car class: ')
        if len(car_class)!=0:
            break
        print_slow('\tPlease enter a car class')
    while True:
        model_name=input('\n\tEnter the model name: ')
        if len(model_name)!=0:
            break
        print_slow('\tPlease enter a model name')
    while True:
        car_color=input('\n\tEnter the car color: ')
        if len(car_color)!=0:
            break
        print_slow('\tPlease enter a car color')
    while True:
        capacity=input('\n\tEnter the capacity: ')
        if capacity.isdigit()==False:
            print_slow('\tPlease enter a number...')
            continue
        capacity=int(capacity)
        break
    while True:
        daily_rent=input('\n\tEnter the daily rent: ')
        if daily_rent.isdigit()==False:
            print_slow('\tPlease enter a number...')
            continue
        daily_rent=int(daily_rent)
        break
    
    #adding
    q="insert into cars(car_no,car_class,model_name,car_color,capacity,\
daily_rent) values('{}','{}','{}','{}','{}','{}');".format(car_no,\
car_class.upper(),model_name.upper(),car_color.upper(),capacity,daily_rent)
    cur=cn.cursor()
    cur.execute(q)
    print_slow('\n\tCAR ADDED..... \n')
    cn.commit()
    print_slow('\n\tRedirecting to Garage.... Press Enter')
    input('')
    garage()
    return

#REMOVE CAR
def remove_car():
    os.system('cls')
    title(com_name)
    heading('ADMIN PORTAL')
    heading('GARAGE')
    heading('REMOVE CAR')

    #printing cars
    print("\t You can only remove the cars which are'nt rented\n")
    cur=cn.cursor()
    cur.execute('select car_no,car_class,model_name,car_color,\
capacity, daily_rent, car_status from cars order by Car_Class;')
    l=cur.fetchall()
    print('')
    sp=[15,15,20,15,15,15,15]
    z='+'
    for y in sp:
        z=z+'-'*(y+1)+'+'
    print(z)
    time.sleep(0.03)
    print('| ',cut('CAR_NO',15),'| ',\
            cut('CAR_CLASS',15),'| ',\
            cut('MODEL_NAME',20),'| ',\
            cut('CAR_COLOR',15),'| ',\
            cut('CAPACITY',15),'| ',\
            cut('DAILY_RENT',15),'| ',\
            cut('CAR_STATUS',15),'| ',sep="")
    time.sleep(0.03)
    print(z)
    time.sleep(0.03)
    for y in range(0,len(l)):
        print('| ',end='')
        for x in range(0,len(l[y])):
            print(cut(l[y][x],sp[x]),end='')
            print('| ',end='')
        print('')
        time.sleep(0.03)
    print(z)

    #validating car_no
    cur=cn.cursor()
    cur.execute("select car_no from cars where car_status='AVAILABLE';")
    l=cur.fetchall()
    if len(l)==0:
        print_slow('\n\tNo cars can be removed currently!, Press enter to go\
back')
        input()
        garage()
        return
    while True:
        c_no=input('\n\tEnter the car_no of the car to be removed or \
enter "q" to go back: ')
        if c_no in ['q','Q']:
            garage()
            return
        if c_no.isdigit()==False:
            print_slow('\tPlease enter a number...')
            continue
        c_no=int(c_no)
        break
    x=(int(c_no),)
    if x not in l:
        print_slow('\n\tPlease enter valid & available car_no...')
        time.sleep(0.5)
        remove_car()
        
    #confirmation
    s=input('\tPlease confirm if you want to delete this car (y/n): ')
    if s=='y':
        pass
    else:
        print_slow('\n\tCar not removed, Redirecting to Garage...Press Enter')
        input()
        garage()
        return

    #removing
    cur=cn.cursor()
    q='delete from cars where Car_no={};'.format(c_no)
    cur.execute(q)
    print_slow('\n\tCAR REMOVED.....')
    cn.commit()
    print_slow('\tRedirecting to Garage....Press Enter')
    input()
    garage()

#================= START SCREEN, END SCREEN, CREDITS FUNCTIONS ==============

#PRINT CREDITS
def credit():
    os.system('cls')
    lc=[]
    lc.append(r'                                                           ')
    lc.append(r'                         -: CREATED BY :-                  ')
    lc.append(r'                     _________ _       _______  _______    ')
    lc.append(r'            |\     /|\__   __/| \   /\(  ___  )(  ____ \   ')
    lc.append(r'            | )   ( |   ) (   | |  / /| (   ) || (    \/   ')
    lc.append(r'            | |   | |   | |   | |_/ / | (___) || (_____    ')
    lc.append(r'            ( (   ) )   | |   |  _ (  |  ___  |(_____  )   ')
    lc.append(r'             \ \_/ /    | |   | | \ \ | (   ) |      ) |   ')
    lc.append(r'              \   /  ___) (___| |  \ \| )   ( |/\____) |   ')
    lc.append(r'               \_/   \_______/|_/   \/|/     \|\_______)   ')
    lc.append(r'                                                           ')
    lc.append(r'                  _______  _______  _______ _________      ')  
    lc.append(r'                 (       )(  ____ \(  ____ \\__   __/      ')
    lc.append(r'                 | () () || (    \/| (    \/   ) (         ')
    lc.append(r'                 | || || || (__    | (__       | |         ')
    lc.append(r'                 | |(_)| ||  __)   |  __)      | |         ')
    lc.append(r'                 | |   | || (      | (         | |         ') 
    lc.append(r'                 | )   ( || (____/\| (____/\   | |         ') 
    lc.append(r'                 |/     \|(_______/(_______/   )_(         ') 
    lc.append(r'                                                           ')
    lc.append(r'             ______   _______  _______  _______  _______   ')
    lc.append(r'            (  __  \ (  ____ )(  ____ \(  ___  )(       )  ')
    lc.append(r'            | (  \  )| (    )|| (    \/| (   ) || () () |  ')
    lc.append(r'            | |   ) || (____)|| (__    | (___) || || || |  ')
    lc.append(r'            | |   | ||     __)|  __)   |  ___  || |(_)| |  ')
    lc.append(r'            | |   ) || (\ (   | (      | (   ) || |   | |  ')
    lc.append(r'            | (__/  )| ) \ \__| (____/\| )   ( || )   ( |  ')
    lc.append(r'            (______/ |/   \__/(_______/|/     \||/     \|  ')
    lc.append(r'                                                           ')
    lc.append(r'                                                           ')
    lc.append(r'                                                           ')

    for y in lc:
         print(y)
         time.sleep(0.03)

    x=input('\tPRESS ENTER TO READ LICENSE & ACKNOWLEDGEMENT OR ENTER ANYTHIG \
TO GO BACK: ')
    if x=='':
         os.system('cls')
         time.sleep(0.5)
         print_slow(
         '''

                             LICENSE & ACKNOWLEDGEMENT              

         THIS PROGRAM IS MADE SOLELY FOR EDUCATINAL PURPOSE. THE PROGRAM SHA-
         -LL NOT BE USED FOR COMMERCIAL OR ANY OTHER PURPOSE. THE PROGRAM AND
         SOURCE CODE IS OPEN FOR USE. WHENEVER THE SOURCE CODE OR ANY PART OF
         SOURCE CODE IS USED OR COPIED, THE ORIGINAL CREATORS MUST BE ACKNOW-
         -EDGED!!!


         THE ASCII ART USED IN THE CREDITS, START AND END SCREEN IS MADE FROM
         'PATORJK WEBSITE'           LINK:  http://patorjk.com/software/taag/

         THANK YOU !!!   :)

                                                          - TEAM CARISTROCRAT         

                                          
         ''',0.003)
         input('\n\tPress Enter to go back')
         os.system('cls')
    return

#PRINT START SCREEN
def start(t):
    os.system('cls')
    col,row=os.get_terminal_size()
    row,col=row-1,col-1

    t1='connecting to our servers'
    t2='logging in to our servers'
    dot='.'*int((col-10-len(t)-len(t1)-len(t2))/4)
    s='|#'+dot + t1 + dot+'#| '+t+' |#'+dot + t2 + dot+'#|'
    l=len(s)

    a1=r"     _____     "
    a2=r"  __/__|__\__  "
    a3=r" /  _ VMD _  \ "
    a4=r"'--(_)---(_)--'"
     
    w1=r'__      _____ _    ___ ___  __  __ ___ '
    w2=r'\ \    / / __| |  / __/ _ \|  \/  | __|'
    w3=r' \ \/\/ /| _|| |_| (_| (_) | |\/| | _| '
    w4=r'  \_/\_/ |___|____\___\___/|_|  |_|___|'

    sp=' '*int((l-len(a4)-len(w3))/2)
    w1=sp+w1+sp
    w2=sp+w2+sp
    w3=sp+w3+sp
    w4=sp+w4+sp

    n=int((row-9)/2)-1
    for y in range(0,l+1):
        os.system('cls')
        for x in range(n):
             print(s[:y])
        print("")
        print("")
        print(w1[0:y]+a1)
        print(w2[0:y]+a2)
        print(w3[0:y]+a3)
        print(w4[0:y]+a4)
        print("="*l)
        print("")
        print("")
        for x in range(n):
            print(s[:y])
        time.sleep(0.01)
    input('')
    os.system('cls')
    return

#PRINT END SCREEN
def end(t):
    os.system('cls')
    col,row=os.get_terminal_size()
    row,col=row-1,col-1

    t1=' thank you '
    t2='logging off'
    dot='.'*int((col-10-len(t)-len(t1)-len(t2))/4)
    s='|#'+dot + t1 + dot+'#| '+t+' |#'+dot + t2 + dot+'#|'
    l=len(s)

    a1=r"     _____     "
    a2=r"  __/__|__\__  "
    a3=r" /  _ VMD _  \ "
    a4=r"'--(_)---(_)--'"
     
    w1=r"  ___  ___   ___  ___    _____   _____ "
    w2=r" / __|/ _ \ / _ \|   \  | _ ) \ / / __|"
    w3=r"| (_ | (_) | (_) | |) | | _ \\ V /| _| "
    w4=r" \___|\___/ \___/|___/  |___/ |_| |___|"

    sp=' '*(int((l-len(a4)-len(w3))/2)-2)
    w1=sp+w1+sp
    w2=sp+w2+sp
    w3=sp+w3+sp
    w4=sp+w4+sp
    ws=' '*len(w3)

    n=int((row-9)/2)-1
    for y in range(l,-1,-1):
        os.system('cls')
        for x in range(n):
            print(' '*(col-len(s[y:])-1)+s[y:])
        print("")
        print("")
        print(ws[0:y]+a1+w1[y:])
        print(ws[0:y]+a2+w2[y:])
        print(ws[0:y]+a3+w3[y:])
        print(ws[0:y]+a4+w4[y:])
        print("="*l)
        print("")
        print("")
        for x in range(n):
            print(' '*(col-len(s[y:])-1)+s[y:])
        time.sleep(0.01)
    input('')
    os.system('cls')
    return

#PROGRAM END
def program_end():
    cn.commit()
    cn.close()
    #end screen
    end(com_name)
    return
    
#======================== INITIATING THE PROGRAM =============================

#PROGRAM START
os.system('mode con lines=200 cols=200')
os.system('COLOR F0')

#START SCREEN
com_name='CARISTROCRAT - CAR RENTALS'
start(com_name)

#SQL OBTAINING PASSWORD
while True:
    os.system('cls')
    title(com_name)
    heading('SQL - PASSWORD')
    print("\n\n\n\t\tEnter your computer's MY_SQL password : ",end='')
    paas=getpass.getpass('')

    try:
        cn=mc.connect(host='localhost',user='root',passwd=paas,database='CARISTROCRAT')
    except:
        print_slow('\n\t\tConnection Failed... Enter password again..',0.01)
        time.sleep(0.5)
        continue
    print_slow('\n\t\tConnection Successful...Press Enter',0.01)
    input()
    break

main_menu()

#******************************code ends here ********************************
