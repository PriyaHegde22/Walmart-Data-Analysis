from flask import Blueprint,request,jsonify
from sqlalchemy.sql import text
from db import db 
import datetime

dashboard_blueprint = Blueprint('dashboard_blueprint',__name__)

# Today's visitors
@dashboard_blueprint.route('/today-visitors')
def todayVisitors():
    currentDate = datetime.datetime.today().strftime("%Y-%m-%d")
    sqlTodayVisitors = text('SELECT COUNT(*) AS today_visitors FROM visitors_log WHERE date = "'+currentDate+'"')
    resultData = db.engine.execute(sqlTodayVisitors)
    rawData = resultData.fetchall()
    
    jsonData = jsonify([dict(row) for row in rawData])
    return jsonData

# Overall visitors
@dashboard_blueprint.route('/overall-visitors')
def overallVisitors():

    sqlOverallVisitors = text('SELECT COUNT(*) AS overall_visitors FROM visitors_log')
    resultData = db.engine.execute(sqlOverallVisitors)
    rawData = resultData.fetchall()
    
    jsonData = jsonify([dict(row) for row in rawData])
    return jsonData

#Male visitors today
@dashboard_blueprint.route('/male-today-visitors')
def maleVisitors():
    currentDate = datetime.datetime.today().strftime("%Y-%m-%d")
    sqlMaleVisitors = text('SELECT COUNT(*) AS male_visitors FROM visitors_log WHERE date = "'+currentDate+'" AND gender=1')
    resultData = db.engine.execute(sqlMaleVisitors)
    rawData = resultData.fetchall()
    
    jsonData = jsonify([dict(row) for row in rawData])
    return jsonData

#Female visitors today
@dashboard_blueprint.route('/female-today-visitors')
def femaleVisitors():
    currentDate = datetime.datetime.today().strftime("%Y-%m-%d")
    sqlFemaleVisitors = text('SELECT COUNT(*) AS female_visitors FROM visitors_log WHERE date = "'+currentDate+'" AND gender=2')
    resultData = db.engine.execute(sqlFemaleVisitors)
    rawData = resultData.fetchall()
    
    jsonData = jsonify([dict(row) for row in rawData])
    return jsonData

#table data 
@dashboard_blueprint.route('/table-data')
def tableData():
    currentDate = datetime.datetime.today().strftime("%Y-%m-%d")
    txtLable = ''
    x = ''
    for a in range(1,6):
        if a == 1:
            txtLable = 'Kids'
        elif a == 2:
            txtLable = 'Teenagers'
        elif a == 3:
            txtLable = 'Youngsters'
        elif a == 4:
            txtLable = 'Adult'
        elif a == 5:
            txtLable = 'Senior Citizen'
            
        for g in range(1,3):
            #today's visitors
            sqlTodayVisitors = text('SELECT COUNT(*) AS today_visitors FROM visitors_log WHERE date = "'+currentDate+'" AND gender = '+str(g)+' AND age_group = '+str(a)+'')
            resultData = db.engine.execute(sqlTodayVisitors)
            rawData = resultData.fetchall()
            ageGroupGenderToday = rawData[0].today_visitors
            
             #overall visitors
            sqlOverallVisitors = text('SELECT COUNT(*) AS overall_visitors FROM visitors_log WHERE gender = '+str(g)+' AND age_group = '+str(a)+'')
            resultOData = db.engine.execute(sqlOverallVisitors)
            rawOData = resultOData.fetchall()
            ageGroupGenderOverall = rawOData[0].overall_visitors
            
            gText = ''
            if g == 1:
                gText = "Male"
            elif g == 2:
                gText = "Female"
                
            x+= '{"gender":"'+gText+'","age_group":"'+txtLable+'","today_visitors":"'+str(ageGroupGenderToday)+'","overall_visitors":"'+str(ageGroupGenderOverall)+'"},'
            
        #End of inner for loop
        
    #end of outer for loop
    x = x[:-1]
    jsonData = '['+x+']'
    return jsonData
#Graph
@dashboard_blueprint.route('/graph-data')
def graph_data():
    x = ''
    for m in range(1,13):
        sqlMonthData = text('SELECT COUNT(*) AS monthly_visitors FROM visitors_log WHERE MONTH(date)="'+str(m)+'"')
        resultData = db.engine.execute(sqlMonthData)
        rawData = resultData.fetchall()
        totalMonthlyVisitors = rawData[0].monthly_visitors
        
        x+= '{"month":"'+str(totalMonthlyVisitors)+'"},'
        
    x = x[:-1]
    
    jsonData = '['+x+']'
    return jsonData