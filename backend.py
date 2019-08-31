import datetime
import traceback

def viewrecipe(day,meal):
    
    #cur.execute("SELECT * FROM recipe WHERE name=(SELECT name from recipecatalog rc,schedule s WHERE rc.recipeid=s.recipeid AND day=%s AND meal=%s)",(day,meal,))
    f = open("schedule.txt", "r")
    l=list()
    recipe_id=0
    count=0
    for line in f:
     count+=1
    f.seek(0,0)
    for line in f:
     if(count>1):
      ll=[]
      for x in line.strip().split('|'):
        ll.append(x)
      if(ll[0]==day and ll[2]==meal):
        recipe_id=ll[1]
        break
    f.close()
    
    recipe_name=""
    f = open("recipecatalog.txt", "r")
    l=list()
    count=0
    for line in f:
     count+=1
    f.seek(0,0)
    for line in f:
     if(count>1):
      ll=[]
      for x in line.strip().split('|'):
       ll.append(x)
      if(ll[0]==recipe_id):
        recipe_name=ll[1]
    f.close()
    
    f = open("index_recipe.txt", "r")
    l=list()
    count=0
    for line in f:
      count+=1
    f.seek(0,0)
    ll=[]
    for line in f:
     if(count>1):
      ll=line.strip().split('|')
      if(ll[0]==recipe_name):
        l.append(ll[1])
    
    f.close()
    f = open("recipe.txt", "r")
    m=[]
    n=[]
    y=0
    for x in l:
      y=int(x)
      f.seek(y,0)
      m=f.readline().strip().split('|')
      n.append(m)
    f.close()
    return n


def nvalue(ing):
    #cur.execute("SELECT * FROM nutrition WHERE ingredient=%s", (ing,))
    f = open("index_nutrition.txt", "r")
    l=list()
    count=0
    for line in f:
      count+=1
    f.seek(0,0)
    for line in f:
     if(count>1):
      x,pos=line.strip().split('|')
      if(x==ing):
        break
    f.close()

    f = open("nutrition.txt", "r")
       
    f.seek(int(pos),0)
    m=f.readline().strip().split('|')
    l.append(m)
    f.close()
    return l
       
def viewingredient(ingred):
    #cur.execute("SELECT * FROM ingredients WHERE name=%s ",(ingred,))
    f = open("index_ingredients.txt", "r")
    l=list()
    count=0
    for line in f:
      count+=1
    f.seek(0,0)
    for line in f:
     if(count>1):
      x,pos=line.strip().split('|')
      if(x==ingred):
        break
    f.close()

    f = open("ingredients.txt", "r")
    y=int(pos)   
    print(y)
    f.seek(y,0)
    
    m=f.readline().strip().split('|')
    l.append(m)
    f.close()
    return l
  

def shopdetail(day,meal):
    #cur.execute("SELECT DISTINCT shopid,s.name,address,phone from shop s,ingredients i WHERE s.family=i.family AND i.name IN(SELECT ingredient from recipe WHERE name=(SELECT name from recipecatalog rc,schedule s WHERE rc.recipeid=s.recipeid AND day=%s AND meal=%s))",(day,meal,))

    f = open("schedule.txt", "r")
    l=list()
    count=0
    for line in f:
     count+=1
    f.seek(0,0)
    for line in f:
     if(count>1):
      t=()
      for x in line.strip().split('|'):
        t=t+(x,)
      if(t[0]==day and t[2]==meal):
        recipe_id=t[1]
        break
    f.close()
    
    f = open("recipecatalog.txt", "r")
    l=list()
    count=0
    for line in f:
     count+=1
    f.seek(0,0)
    for line in f:
     if(count>1):
      t=()
      for x in line.strip().split('|'):
       t=t+(x,)
      if(t[0]==recipe_id):
        recipe_name=t[1]
    f.close()
    
    f = open("recipe.txt", "r")
    l=list()
    count=0
    for line in f:
      count+=1
    f.seek(0,0)
    for line in f:
     if(count>1):
      t=()
      for x in line.strip().split('|'):
       t=t+(x,)
      if(t[0]==recipe_name):
       l.append(t[1])
    f.close()
    
    f = open("ingredients.txt", "r")
    l_family=list()
    count=0
    for line in f:
      count+=1
    f.seek(0,0)
    for line in f:
     if(count>1):
      t=()
      for x in line.strip().split('|'):
       t=t+(x,)
      for i in l:
        if(t[0]==i):
          l_family.append(t[4])
    f.close()
    
    final_l_family=list() 
    
    for i in l_family:
     try:
      for j in final_l_family:
        if(i==j):
         raise Exception   
      final_l_family.append(i)
     except:
       continue
    
    f = open("shop.txt", "r")
    l_shop=list()
    count=0
    for line in f:
      count+=1
    f.seek(0,0)
    for line in f:
     if(count>1):
      t=()
      for x in line.strip().split('|'):
       t=t+(x,)
      for i in final_l_family:
       if(t[4]==i):
        l_shop.append(t)
    f.close()
    
    return l_shop
    

def update(name,quantity):
    try:
        
     #cur.execute("UPDATE ingredients SET quantity=%s WHERE name=%s",(quantity,name,))
     ingredients= open("ingredients.txt", "r")
     count=0
     for line in ingredients:
      count+=1
     ingredients.seek(0,0)
     data=ingredients.readlines()
     ingredients.seek(0,0)
     for line in ingredients:
       count+=1 
     ingredients.seek(0,0)
     index=0
     for line in ingredients:
      if(count>1):
       if name in line:
         m=line.strip().split('|')
         buying_date=m[2]
         expiry_date=m[3]
         family=m[4]
         break
       index+=1
     data[index]=name+"|"+str(quantity)+"|"+buying_date+"|"+expiry_date+"|"+family+"\n"
     ingredients= open("ingredients.txt", "w")
     ingredients.writelines(data)
     ingredients.close()
    except Exception :
     #traceback.print_exc()
     return "Not Done"
    return "Done"


def updateingredientaftershopping(name,quantity,buying_date ,expiry_date,family):
    try:
     
     #cur.execute("UPDATE ingredients SET quantity=quantity+%s, buying_date=%s ,expiry_date=%s ,family=%s  WHERE name=%s",(quantity,buying_date ,expiry_date,family,name,))
     ingredients= open("ingredients.txt", "r")
     count=0
     for line in ingredients:
      count+=1
     ingredients.seek(0,0)
     data=ingredients.readlines()
     ingredients.seek(0,0)
     for line in ingredients:
       count+=1 
     ingredients.seek(0,0)
     index=0
     for line in ingredients:
      if(count>1):
       if name in line:
         break
       index+=1
     data[index]=name+"|"+str(quantity)+"|"+buying_date+"|"+expiry_date+"|"+family+"\n"
     ingredients= open("ingredients.txt", "w")
     ingredients.writelines(data)
     ingredients.close()
    except Exception :
     #traceback.print_exc()
     return "Not Done"
    return "Done"

def schedulechange(name,day,meal):
    try:
     #cur.execute("UPDATE schedule set recipeid=(SELECT recipeid from recipecatalog WHERE name=%s) WHERE day=%s AND meal=%s",(name,day,meal,))
     recipecatalog = open("recipecatalog.txt", "r")
     count=0
     for line in recipecatalog:
      count+=1
     recipecatalog.seek(0,0)
     for line in recipecatalog:
      if(count>1):
       t=()
       for x in line.strip().split('|'):
        t=t+(x,)
       if(t[1]==name):   
         recipe_id=t[0]
         break
     recipecatalog.close()
     schedule= open("schedule.txt", "r")
     data=schedule.readlines()
     schedule.seek(0,0)
     for line in schedule:
       count+=1 
     schedule.seek(0,0)
     index=0
     for line in schedule:
      if(count>1):
       if day in line and meal in line:
         break
       index+=1
     data[index]=day+"|"+recipe_id+"|"+meal+"\n"
     schedule= open("schedule.txt", "w")
     schedule.writelines(data)
     schedule.close()
    except Exception :
     #traceback.print_exc()
     return "Not Done"
    return "Done"



def expiryreminder(date1,date2):
    
  #cur.execute('SELECT name FROM ingredients WHERE expiry_date BETWEEN (%s) AND (%s)',(date1,date2,))
  f = open("ingredients.txt", "r")
  l=list()
  count=0
  for line in f:
    count+=1
  f.seek(0,0)
  for line in f:
   if(count>1):
    t=()
    for x in line.strip().split('|'):
     t=t+(x,)
    m=t[3].split('-')
    d=datetime.datetime(int(m[0]),int(m[1]),int(m[2])) 
    d1=datetime.datetime.strptime(date1,'%Y-%m-%d') 
    d2=datetime.datetime.strptime(date2,'%Y-%m-%d') 
    if(d>=d1 and d<=d2):
     l.append(t)
    count-=1
  f.close()
  return l


def show1():
 
  #cur.execute("SELECT * FROM ingredients")
  f = open("ingredients.txt", "r")
  l=list()
  count=0
  for line in f:
    count+=1
  f.seek(0,0)
  for line in f:
   if(count>1):
    t=()
    for x in line.strip().split('|'):
     t=t+(x,)
    l.append(t)
  f.close()
  return l
  

def show2():
  
  #cur.execute("SELECT * FROM recipe")
  f = open("recipe.txt", "r")
  l=list()
  count=0
  for line in f:
    count+=1
  f.seek(0,0)
  for line in f:
   if(count>1):
    t=()
    for x in line.strip().split('|'):
     t=t+(x,)
    l.append(t)
  f.close()
  return l
  

def show3():
  
  #cur.execute("SELECT * FROM schedule")
  f = open("schedule.txt", "r")
  l=list()
  count=0
  for line in f:
    count+=1
  f.seek(0,0)
  for line in f:
   if(count>1):
    t=()
    for x in line.strip().split('|'):
     t=t+(x,)
    l.append(t)
  f.close()
  return l
  

def show4():
 
  #cur.execute("SELECT * FROM nutrition")
  f = open("nutrition.txt", "r")
  l=list()
  count=0
  for line in f:
    count+=1
  f.seek(0,0)
  for line in f:
   if(count>1):
    t=()
    for x in line.strip().split('|'):
     t=t+(x,)
    l.append(t)
  f.close()
  return l
  

def show5():
  
  #cur.execute("SELECT * FROM shop")
  f = open("shop.txt", "r")
  l=list()
  count=0
  for line in f:
    count+=1
  f.seek(0,0)
  for line in f:
   if(count>1):
    t=()
    for x in line.strip().split('|'):
     t=t+(x,)
    l.append(t)
  f.close()
  return l


def show6():
  
  #cur.execute("SELECT * FROM recipecatalog")
  f = open("recipecatalog.txt", "r")
  l=list()
  count=0
  for line in f:
    count+=1
  f.seek(0,0)
  for line in f:
   if(count>1):
    t=()
    for x in line.strip().split('|'):
     t=t+(x,)
    l.append(t)
  f.close()
  return l

'''

print(viewrecipe("mon","breakfast"))
print(nvalue("Paneer"))
print(viewingredient("Paneer"))
print(shopdetail("mon","breakfast"))
print(update("Paneer",250))
print(updateingredientaftershopping("Paneer",200,"2018-01-01","2018-02-01","dairy"))
print(schedulechange("mon",2,"breakfast"))
print(expiryreminder("2018-01-01","2018-11-01"))
print(noofingredients())
print(show1())
print(show2())
print(show3())
print(show4())
print(show5())
print(show6())
'''
print(viewingredient("Paneer"))


