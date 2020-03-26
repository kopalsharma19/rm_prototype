from pymongo import MongoClient
from datetime import datetime
from flask import Flask, render_template, request, url_for,redirect
import os 
from bson import ObjectId   
from flask_pymongo import PyMongo
from FlaskWebProject6 import app
#from flask_apscheduler import APScheduler 
from threading import Timer

app.config["MONGO_URI"] = "mongodb://WorkAmp%5FMVP:ampitup%40futurex@workamp-mvp-shard-00-00-buabm.mongodb.net:27017,workamp-mvp-shard-00-01-buabm.mongodb.net:27017,workamp-mvp-shard-00-02-buabm.mongodb.net:27017/test?ssl=true&replicaSet=WorkAmp-MVP-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)

client = MongoClient("mongodb://WorkAmp%5FMVP:ampitup%40futurex@workamp-mvp-shard-00-00-buabm.mongodb.net:27017,workamp-mvp-shard-00-01-buabm.mongodb.net:27017,workamp-mvp-shard-00-02-buabm.mongodb.net:27017/test?ssl=true&replicaSet=WorkAmp-MVP-shard-0&authSource=admin&retryWrites=true&w=majority")
#client.server_info()    
db = client.get_database('Demo01')
records = db['Daily Activities']
washroom_checklist = db['Washroom Checklist']
fridge_checklist = db['Fridge Checklist']
huddle_checklist = db['Huddle Room Checklist']
meeting_checklist = db['Meeting Room Checklist']
monthly_checklist = db["Monthly Checklist"]
weekly_checklist = db["Weekly Checklist"]
pantry = db["Pantry"]
fnb = db["fnb"]
office_supp = db["Office Supplies"]
housekeeping = db["Housekeeping"]
finance = db["Finance"]



def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('admin')


@app.route('/')

@app.route('/admin_dash')
def admin_dash():
    wrem = washroom_checklist.find({"Status":"None"}).count()
    frem = fridge_checklist.find({"Status":"None"}).count()
    hrem = huddle_checklist.find({"Status":"None"}).count()
    mrem = meeting_checklist.find({"Status":"None"}).count()
    rem = wrem+frem+hrem+mrem

    pantryc = pantry.find({"Quantity":""}).count()
    fnbc = fnb.find({"Quantity":""}).count()
    office_suppc = office_supp.find({"Quantity":""}).count()
    housekeepingc = housekeeping.find({"Quantity":""}).count()
    totalc = pantryc+fnbc+office_suppc+housekeepingc


    monrem = monthly_checklist.find({"Status":"None"}).count()
    taskrem = records.find({"done":"no"}).count()
    return render_template('admin_dash.html', rem=rem,totalc = totalc, monrem = monrem,taskrem= taskrem)


@app.route('/rec_expense_dash')
def rec_expense_dash():
    wrem = washroom_checklist.find({"Status":"None"}).count()
    frem = fridge_checklist.find({"Status":"None"}).count()
    hrem = huddle_checklist.find({"Status":"None"}).count()
    mrem = meeting_checklist.find({"Status":"None"}).count()
    rem = wrem+frem+hrem+mrem

    pantryc = pantry.find({"Quantity":""}).count()
    fnbc = fnb.find({"Quantity":""}).count()
    office_suppc = office_supp.find({"Quantity":""}).count()
    housekeepingc = housekeeping.find({"Quantity":""}).count()
    totalc = pantryc+fnbc+office_suppc+housekeepingc


    monrem = monthly_checklist.find({"Status":"None"}).count()
    taskrem = records.find({"done":"no"}).count()

    return render_template('rec_expense_dash.html', rem=rem,totalc = totalc, monrem = monrem,taskrem= taskrem)

@app.route("/rec_expense_dashfunc", methods=['POST'])    
def rec_expense_dashfunc():
    finance.insert_one({"Title":request.form['Title'],"Amount":request.form['amount'],"Category":request.form.get('category'),"Subcategory":request.form.get('categorysub'),"Date of Payment":request.form['date'],"Invoice ID":request.form['invoice'],"GST no":request.form['gst'],"Payment Mode":request.form.get('payment')})

    redir=redirect_url()        
    return redirect(redir)  










@app.route('/checklist_dash')
def checklist_dash():
    wrem = washroom_checklist.find({"Status":"None"}).count()
    frem = fridge_checklist.find({"Status":"None"}).count()
    hrem = huddle_checklist.find({"Status":"None"}).count()
    mrem = meeting_checklist.find({"Status":"None"}).count()
    return render_template('checklist_dash.html',wrem = wrem, frem = frem, hrem = hrem, mrem = mrem)

@app.route("/checklist")
def checklist():
    washroom_list = washroom_checklist.find()
    return render_template('checklist.html',washroom_list = washroom_list)


@app.route("/okaydrop", methods=['POST'])    
def okaydrop():    


    flush = request.form.get("Flush")
    taps = request.form.get("Taps")
    cleanliness_water = request.form.get("Cleanliness of water from taps")
    door = request.form.get("Door mechanism of all cubicles")
    smell = request.form.get("Smell")
    mirror = request.form.get("Mirror")
    handshower = request.form.get("Handshower leakage and mechanism")

    if(str(flush)=="Okay"):
        washroom_checklist.update({"Item":"Flush"}, {"$set": {"Status":"Okay"}})
    elif(str(flush)=="Not Okay"):
        washroom_checklist.update({"Item":"Flush"}, {"$set": {"Status":"Not Okay"}})

    if(str(taps)=="Okay"):
        washroom_checklist.update({"Item":"Taps"}, {"$set": {"Status":"Okay"}})
    elif(str(taps)=="Not Okay"):
        washroom_checklist.update({"Item":"Taps"}, {"$set": {"Status":"Not Okay"}})

    if(str(cleanliness_water)=="Okay"):
        washroom_checklist.update({"Item":"Cleanliness of water from taps"}, {"$set": {"Status":"Okay"}})
    elif(str(cleanliness_water)=="Not Okay"):
        washroom_checklist.update({"Item":"Cleanliness of water from taps"}, {"$set": {"Status":"Not Okay"}})

    if(str(door)=="Okay"):
        washroom_checklist.update({"Item":"Door mechanism of all cubicles"}, {"$set": {"Status":"Okay"}})
    elif(str(door)=="Not Okay"):
        washroom_checklist.update({"Item":"Door mechanism of all cubicles"}, {"$set": {"Status":"Not Okay"}})

    if(str(smell)=="Okay"):
        washroom_checklist.update({"Item":"Smell"}, {"$set": {"Status":"Okay"}})
    elif(str(smell)=="Not Okay"):
        washroom_checklist.update({"Item":"Smell"}, {"$set": {"Status":"Not Okay"}})

    if(str(mirror)=="Okay"):
        washroom_checklist.update({"Item":"Mirror"}, {"$set": {"Status":"Okay"}})
    elif(str(mirror)=="Not Okay"):
        washroom_checklist.update({"Item":"Mirror"}, {"$set": {"Status":"Not Okay"}})

    if(str(handshower)=="Okay"):
        washroom_checklist.update({"Item":"Handshower leakage and mechanism"}, {"$set": {"Status":"Okay"}})
    elif(str(handshower)=="Not Okay"):
        washroom_checklist.update({"Item":"Handshower leakage and mechanism"}, {"$set": {"Status":"Not Okay"}})
    else:
        pass

    washroom_checklist.update_many({'Status': 'Okay'}, {"$set": { "done": "yes" }})
        
    if(washroom_checklist.find({"Item":"Flush"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Flush","done":"no","checklist": "yes"})
    if(washroom_checklist.find({"Item":"Taps"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Taps","done":"no"})
    if(washroom_checklist.find({"Item":"Cleanliness of water from taps"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Cleanliness of water from taps","done":"no"})
    if(washroom_checklist.find({"Item":"Door mechanism of all cubicles"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Door mechanism of all cubicles","done":"no"})
    if(washroom_checklist.find({"Item":"Smell"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Smell","done":"no"})
    if(washroom_checklist.find({"Item":"Mirror"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Mirror","done":"no"})
    if(washroom_checklist.find({"Item":"Handshower leakage and mechanism"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Handshower leakage and mechanism","done":"no"})
    else:
        pass

    return redirect(url_for('admin'))

@app.route("/checklist_dash_weekly")
def checklist_dash_weekly():
    pantryc = pantry.find({"Quantity":""}).count()
    fnbc = fnb.find({"Quantity":""}).count()
    office_suppc = office_supp.find({"Quantity":""}).count()
    housekeepingc = housekeeping.find({"Quantity":""}).count()

    return render_template('checklist_dash_weekly.html',pantryc = pantryc, fnbc = fnbc, office_suppc = office_suppc, housekeepingc = housekeepingc)


@app.route("/checklist_weekly")
def checklist_weekly():
    pantry_list = pantry.find()
    return render_template('checklist_weekly.html',pantry_list = pantry_list)

@app.route("/inventory", methods = ['POST'])
def inventory():

    pantry.update({"Item":"Plate"}, {"$set": {"Quantity":request.form['Plate']}})
    pantry.update({"Item":"Spoon"}, {"$set": {"Quantity":request.form['Spoon']}})
    pantry.update({"Item":"Fork"}, {"$set": {"Quantity":request.form['Fork']}})
    pantry.update({"Item":"Bowl"}, {"$set": {"Quantity":request.form['Bowl']}})
    pantry.update({"Item":"Cup"}, {"$set": {"Quantity":request.form['Cup']}})
    pantry.update({"Item":"Mug"}, {"$set": {"Quantity":request.form['Mug']}})
    pantry.update({"Item":"Knife"}, {"$set": {"Quantity":request.form['Knife']}})
    pantry.update({"Item":"Glass"}, {"$set": {"Quantity":request.form['Glass']}})
    pantry.update({"Item":"Serving Tray"}, {"$set": {"Quantity":request.form['Serving Tray']}})
    pantry.update({"Item":"Water Jar"}, {"$set": {"Quantity":request.form['Water Jar']}})
    pantry.update({"Item":"Microwave"}, {"$set": {"Quantity":request.form['Microwave']}})
    pantry.update({"Item":"Induction"}, {"$set": {"Quantity":request.form['Induction']}})
    pantry.update({"Item":"Fridge"}, {"$set": {"Quantity":request.form['Fridge']}})
    pantry.update({"Item":"Infused Water Dispenser"}, {"$set": {"Quantity":request.form['Infused Water Dispenser']}})
    pantry.update({"Item":"Aquaguard"}, {"$set": {"Quantity":request.form['Aquaguard']}})
    pantry.update({"Item":"Coffee Machine"}, {"$set": {"Quantity":request.form['Coffee Machine']}})
    pantry.update({"Item":"Paper cup"}, {"$set": {"Quantity":request.form['Paper cup']}})
    pantry.update({"Item":"Stirrer"}, {"$set": {"Quantity":request.form['Stirrer']}})
    pantry.update({"Item":"Tissue Paper"}, {"$set": {"Quantity":request.form['Tissue Paper']}})
    pantry.update({"Item":"Disposable cutlery"}, {"$set": {"Quantity":request.form['Disposable cutlery']}})

    redir=redirect_url()        
    return redirect(redir)  


 


@app.route("/checklist_month")
def checklist_month():
    monthly_list = monthly_checklist.find()
    return render_template('checklist_month.html',monthly_list = monthly_list)

@app.route("/okaydrop_month", methods=['POST'])    
def okaydrop_month():    


    pest = request.form.get("Pest control")
    electrical_equip = request.form.get("Electrical equip")
    lift = request.form.get("Lift")
    plumbing = request.form.get("Plumbing")
    cp = request.form.get("Carpentary/Polishing")
    deepc = request.form.get("Deep Cleaning")
    

    if(str(pest)=="Okay"):
        monthly_checklist.update({"Title":"Pest control"}, {"$set": {"Status":"Okay"}})
    elif(str(pest)=="Not Okay"):
        monthly_checklist.update({"Title":"Pest control"}, {"$set": {"Status":"Not Okay"}})

    if(str(electrical_equip)=="Okay"):
        monthly_checklist.update({"Title":"Electrical Equip"}, {"$set": {"Status":"Okay"}})
    elif(str(electrical_equip)=="Not Okay"):
        monthly_checklist.update({"Title":"Electrical Equip"}, {"$set": {"Status":"Not Okay"}})

    if(str(lift)=="Okay"):
        monthly_checklist.update({"Title":"Lift"}, {"$set": {"Status":"Okay"}})
    elif(str(lift)=="Not Okay"):
        monthly_checklist.update({"Title":"Lift"}, {"$set": {"Status":"Not Okay"}})

    if(str(plumbing)=="Okay"):
        monthly_checklist.update({"Title":"Plumbing"}, {"$set": {"Status":"Okay"}})
    elif(str(plumbing)=="Not Okay"):
        monthly_checklist.update({"Title":"Plumbing"}, {"$set": {"Status":"Not Okay"}})

    if(str(cp)=="Okay"):
        monthly_checklist.update({"Title":"Carpentary/Polishing"}, {"$set": {"Status":"Okay"}})
    elif(str(cp)=="Not Okay"):
        monthly_checklist.update({"Title":"Carpentary/Polishing"}, {"$set": {"Status":"Not Okay"}})

    if(str(deepc)=="Okay"):
        monthly_checklist.update({"Title":"Deep Cleaning"}, {"$set": {"Status":"Okay"}})
    elif(str(deepc)=="Not Okay"):
        monthly_checklist.update({"Title":"Deep Cleaning"}, {"$set": {"Status":"Not Okay"}})
    else:
        pass
        
    if(monthly_checklist.find({"Title":"Pest Control"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Pest Control","done":"no","checklist": "yes"})
    if(monthly_checklist.find({"Title":"Electrical Equip"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Electrical Equip","done":"no"})
    if(monthly_checklist.find({"Title":"Lift"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Lift","done":"no"})
    if(monthly_checklist.find({"Title":"Plumbing"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Plumbing","done":"no"})
    if(monthly_checklist.find({"Title":"Carpentary/Polishing"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Carpentary/Polishing","done":"no"})
    if(monthly_checklist.find({"Title":"Deep Cleaning"})[0]["Status"]=="Not Okay"):
        records.insert_one({"Activity":"Deep Cleaning","done":"no"})
    else:
        pass

    return redirect(url_for('admin'))

@app.route('/admin_task')
def admin_task():
    recordsc = records.find({"done":"no"}).count()
    return render_template('admin_task.html',recordsc = recordsc)

@app.route('/admin')
def admin():
    records_list = records.find({"done":"no"})
    return render_template('admin.html',records_list = records_list)

   
@app.route("/done")    
def done ():    
    #Done-or-not ICON    
    id=request.values.get("_id")    
    task=records.find({"_id":ObjectId(id)})    
    if(task[0]["done"]=="yes"):    
        records.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})    
    else:    
        records.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})    
    redir=redirect_url()        
    return redirect(redir)  


@app.route("/lead")
def lead():
    done = records.find({"done":"yes"}).count()
    total = records.find().count()
    per = (done/total)*100

    return render_template('lead.html', per = per)

    
if __name__=='__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)

#delete_rec = {
#    'Activity':'Delete',
#    'Status':'1'}
#records.insert_one(delete_rec)
#records.delete_one({'Status':'1'})



