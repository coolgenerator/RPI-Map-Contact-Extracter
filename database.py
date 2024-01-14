import mariadb
import sys
import datetime

'''
company status:
0 - active
1 - temporarily closed
2 - permanently closed
'''

class Database:
    def __init__(self):
        try:
            self.conn = mariadb.connect( \
            user="root", \
            password="Gooshinflatable", \
            host="localhost", \
            database="GOOSH", \
            autocommit=True)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor() 
    # add info
    def add_company(self, CompanyName, RateNum, Address='', State='', ZipCode='', Category='', Description='', DirectLink='', Status='0', Keyword='', Rate=''):
        # cmd = '''INSERT INTO COMPANY(CompanyName, Address, State, ZipCode, Category, Description, DirectLink, Status, Keyword, Rating, RateNum) VALUES("''' + CompanyName + '''", "''' + Address + '''", "''' + State + '''", "''' + ZipCode + '''", "''' + Category + '''", "''' + Description + '''", "''' + DirectLink + '''", ''' + Status + ''', "''' + Keyword + '''", "''' + Rate + '''", "''' + str(RateNum) + '''");'''
        self.cur.execute("INSERT INTO COMPANY(CompanyName, Address, State, ZipCode, Category, Description, DirectLink, Status, Keyword, Rating, RateNum) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",(CompanyName, Address, State, ZipCode, Category, Description, DirectLink, Status, Keyword, Rate, str(RateNum)))

    def add_website(self, CompanyID, Website, Category='', Status='0'):
        # cmd = "INSERT INTO WEBSITE(CompanyID, Website, Category, Status) VALUES(" + str(CompanyID) + ", '" + Website + "', '" + Category + "', " + Status + ");"
        self.cur.execute("INSERT INTO WEBSITE(CompanyID, Website, Category, Status) VALUES(%s,%s,%s,%s);",(str(CompanyID), Website, Category, Status))

    def add_email(self, CompanyID, WebsiteID, Email, Contactor='', Status='0'):
        # cmd = "INSERT INTO EMAIL(CompanyID, WebsiteID, Email, Contactor, Status) VALUES(" + str(CompanyID) + ", " + str(WebsiteID) + ", '" + Email + "', '" + Contactor + "', " + Status + ");"
        self.cur.execute("INSERT INTO EMAIL(CompanyID, WebsiteID, Email, Contactor, Status) VALUES(%s,%s,%s,%s,%s);",(str(CompanyID),str(WebsiteID),Email,Contactor,Status))

    def add_phone(self, CompanyID, Phone, Contactor='', Status='0'):
        # cmd = "INSERT INTO PHONE(CompanyID, Phone, Contactor, Status) VALUES(" + str(CompanyID) + ", '" + Phone + "', '" + Contactor + "', " + Status + ");"
        self.cur.execute("INSERT INTO PHONE(CompanyID, Phone, Contactor, Status) VALUES(%s,%s,%s,%s);",(str(CompanyID),Phone,Contactor,Status))

    def add_contact_history(self, Times, CompanyID, Date, FromEmailID='', Comment='', Status='0'):
        # cmd = "INSERT INTO CONTACTHISTORY(Times, CompanyID, FromEmailID, Date, Comment, Status) VALUES(" + Times + ", " + str(CompanyID) + ", " + str(FromEmailID) + ", '" + Date + "', '" + Comment + "', " + Status + ");"
        self.cur.execute("INSERT INTO CONTACTHISTORY(Times, CompanyID, FromEmailID, Date, Comment, Status) VALUES(%s,%s,%s,%s,%s,%s);",(Times,str(CompanyID),str(FromEmailID),Date,Comment,Status))

    def add_from_email(self, FromEmailID, Email):
        # cmd = "INSERT INTO FROMEMAIL(FromEmailID, Email) VALUES(" + str(FromEmailID) + ", '" + Email + "');"
        self.cur.execute("INSERT INTO FROMEMAIL(FromEmailID, Email) VALUES(%s,%s);",(str(FromEmailID),Email))

    # update info


    # find info
    def get_company_ID(self, company):
        # cmd = '''SELECT CompanyID FROM COMPANY WHERE CompanyName="'''+company+'''";'''
        self.cur.execute("SELECT CompanyID FROM COMPANY WHERE CompanyName=%s;",(company,))
        return self.cur.fetchone()[0]
    
    def get_website_ID(self, website):
        # cmd = "SELECT WebsiteID FROM WEBSITE WHERE Website='"+website+"';"
        self.cur.execute("SELECT WebsiteID FROM WEBSITE WHERE Website=%s;",(website,))
        return self.cur.fetchone()[0]
    

    # check existance
    def check_company_by_name(self, company, address): # True if the company does not exist
        # cmd = '''SELECT EXISTS(SELECT * FROM COMPANY WHERE CompanyName="'''+company+'''" AND Address="'''+address+'''")'''
        self.cur.execute("SELECT EXISTS(SELECT * FROM COMPANY WHERE CompanyName=%s AND Address=%s)",(company, address))
        # print(self.cur.fetchall()[0][0])
        if self.cur.fetchone()[0] == 0:
            return True
        else:
            return False
        
    def check_email_by_company_name(self, company, email):
        # cmd = '''SELECT EXISTS(SELECT * FROM EMAIL INNER JOIN COMPANY ON EMAIL.CompanyID = COMPANY.CompanyID WHERE Email="'''+email+'''" AND CompanyName="'''+company+'''");'''
        self.cur.execute('''SELECT EXISTS(SELECT * FROM EMAIL INNER JOIN COMPANY ON EMAIL.CompanyID = COMPANY.CompanyID WHERE Email=%s AND CompanyName=%s);''',(email, company))
        if self.cur.fetchone()[0] == 0:
            return True
        else:
            return False
        
    def check_phone_by_company_name(self, company, phone):
        # cmd = '''SELECT EXISTS(SELECT * FROM PHONE INNER JOIN COMPANY ON PHONE.CompanyID = COMPANY.CompanyID WHERE Phone="'''+phone+'''" AND CompanyName="'''+company+'''");'''
        self.cur.execute('''SELECT EXISTS(SELECT * FROM PHONE INNER JOIN COMPANY ON PHONE.CompanyID = COMPANY.CompanyID WHERE Phone=%s AND CompanyName=%s);''',(phone, company))
        if self.cur.fetchone()[0] == 0:
            return True
        else:
            return False
    
    def check_website_by_company_name(self, company, website):
        # cmd = '''SELECT EXISTS(SELECT * FROM WEBSITE INNER JOIN COMPANY ON WEBSITE.CompanyID = COMPANY.CompanyID WHERE Website="'''+website+'''" AND CompanyName="'''+company+'''")'''
        self.cur.execute('''SELECT EXISTS(SELECT * FROM WEBSITE INNER JOIN COMPANY ON WEBSITE.CompanyID = COMPANY.CompanyID WHERE Website=%s AND CompanyName=%s)''',(website, company))
        if self.cur.fetchone()[0] == 0:
            return True
        else:
            return False
    
    # logger
    def check_status(self, keyword):
        # check = '''SELECT TimesID, Time FROM LOGGER WHERE County='Autauga' AND Keyword="'''+keyword+'''" AND Time=(SELECT MAX(Time) FROM LOGGER WHERE Keyword="'''+keyword+'''" AND County="Autauga")'''
        self.cur.execute('''SELECT TimesID, Time FROM LOGGER WHERE County='Autauga' AND Keyword=%s AND Time=(SELECT MAX(Time) FROM LOGGER WHERE Keyword=%s AND County="Autauga")''',(keyword,keyword))
        latestData = self.cur.fetchone()
        print(latestData)
        if(latestData == None):
            times = 1
            print('No data')
            return True, times, ''
        times = latestData[0]
        dateDifferences = datetime.datetime.now() - latestData[1]
        
        # cmd = '''SELECT County FROM LOGGER WHERE TimesID='''+str(times)+''' AND Time=(SELECT MAX(Time) FROM LOGGER WHERE TimesID='''+str(times)+''' AND Keyword="'''+keyword+'''")'''
        self.cur.execute('''SELECT County FROM LOGGER WHERE TimesID=%s AND Time=(SELECT MAX(Time) FROM LOGGER WHERE TimesID=%s AND Keyword=%s)''', (str(times),str(times),keyword))
        county = self.cur.fetchone()[0]
        times +=1
        if dateDifferences.days < 30 and county == "Chesterfield":
            return False, times, ''
        return True, times, county

    def log(self, times, keyword, county):
        self.cur.execute('''INSERT INTO LOGGER VALUES(%s,%s,%s,%s)''',(times,keyword,county,datetime.datetime.now()))
    
    
    # close connection
    def close_DB(self):
        self.conn.close()