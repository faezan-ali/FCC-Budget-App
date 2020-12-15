class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []
#assemble string output
    def __str__(self):
        line1 = "{:*^30}\n".format(self.name)
        line2 = ""
        line3 ="Total: {:.2f}".format(self.get_balance())
        for dict in self.ledger:
            templist =[]
            for item in dict.values():
                if item != None:
                    templist.append(item)
            line2 = line2 + "{:23.23s}{:7.2f}\n".format(templist[1], templist[0])
        return line1 + line2 + line3


    def deposit(self, amount, description=None):
        if description == None:
            description = ""
        amount = float(amount)
        tempdict = {"amount":amount, "description":description}
        self.ledger.append(tempdict)


    def withdraw(self, amount, description=None):
        if description == None:
            description = ""
        if self.check_funds(amount) is False:
            return False
        amount = -float(amount)
        self.ledger.append({"amount":amount, "description":description})
        return True


    def get_balance(self):
        sum = 0
        for transaction in self.ledger:
            amount = transaction["amount"]
            sum += amount
        return sum


    def transfer(self, amount, budgetobj):
        if self.check_funds(amount) is False:
            return False
        self.withdraw(amount, "Transfer to "+ budgetobj.name)
        budgetobj.deposit(amount, "Transfer from "+ self.name)
        return True


    def check_funds(self, amount):
        if self.get_balance() < float(amount):
            return False
        return True



def create_spend_chart(categories):
    from math import floor
    spending, percentage_spending, catnames = [], [], []
    title_lines = ""
    maxnamelen = 0
    for budget_category in categories:
        category_spending = []
        catlen = len(budget_category.name)
        catnames.append(budget_category.name)
#find max length of category names
        if catlen > maxnamelen:
            maxnamelen = catlen
#iterate through budget category ledgers to get withdrawals only
        for dict in budget_category.ledger:
            for item in dict.values():
                if type(item) == float and item < 0:
                    category_spending.append(item)
        spending.append(category_spending)
    spending = [sum(lst) for lst in spending]
#calculate percentage spending for each category
    percentage_spending = [(i/sum(spending))*100 for i in spending]
    percentage_spending = [(floor(i/10)*10) for i in percentage_spending]
#assemble bar chart output
    length = len(categories)
    title = "Percentage spent by category"
    line_x = ""
    chart = ""
    categorychart = ""
    for x in range(100,-1,-10):
        line_x = "{:3}|".format(x)
        for i in percentage_spending:
            if x <= i:
                line_x += " o "
            else:
                line_x += "   "
        chart += line_x +" \n"
    dash_line = "    -"
    for  y in range(length):
        dash_line += "---"
    for z in range(0, maxnamelen):
        categorychart += "    "
        for nam in catnames:
            if z > len(nam)-1:
                categorychart += "   "
            else:
                categorychart += " "+nam[z]+" "
        categorychart += " \n"


    return title +"\n"+ chart + dash_line + "\n"  + categorychart.rstrip("\n")
