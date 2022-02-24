from flask import Flask, request

app = Flask(__name__)

#Doctor Data
Doctors = [
    {
        "ID": 1,
       "firstName": "John",
        "lastName": "Smith"
    }
]

##Apointment Data
Appointments = [
    {
        "ID" : 101,
        "patientFirstName" : "Robert", 
        "patientLastName" : "Smith",
        "appointmentDate" : "02/24/2022",
        "appointmentTime" : "11:00AM",
        "doctorID": 1,
        "kind" : "New Patient"
    },
    {
        "ID" : 102,
        "patientFirstName" : "Roberta", 
        "patientLastName" : "Smith",
        "appointmentDate" : "02/24/2022",
        "appointmentTime" : "11:30AM",
        "doctorID": 1,
        "kind" : "New Patient"
    },
    {
        "ID" : 103,
        "patientFirstName" : "Robertson", 
        "patientLastName" : "Smith",
        "appointmentDate" : "02/24/2022",
        "appointmentTime" : "11:15AM",
        "doctorID": 1,
        "kind" : "New Patient"
    }
]

def getDocID(params):
    for doc in Doctors:
        if params["firstName"] == doc["firstName"] and params["lastName"] == doc["lastName"]:
            docID = doc["ID"]
@app.route('/')
def index():
    return "Hello"

@app.route('/getAllDoctors', methods=['GET'])
def getAllDoctors():
    return {"Doctors": Doctors}

@app.route('/getAppt', methods=['GET'])
def getApptByDocAndDay():
    params = request.args

    docID = getDocID(params)
    results = []

    for appt in Appointments:
        if appt["doctorID"] == docID and appt["appointmentDate"] == params["date"]:
            results.append(appt)

    return {"appoinements": results}

@app.route('/deleteAppt', methods=['DELETE'])
def deleteAppt():
    params = request.args

    for i in range(0,len(Appointments)):
        if params["apptID"] == Appointments[i]["ID"]:
            del Appointments[i]
            break

    return {"Appointments" : Appointments}

@app.route('/createNewAppt', methods=['POST'])
def createNewAppt():
    params = request.args
    
    if params["appointmentTime"] is not None:
        #extract minutes from appointment time by spliting the time string then removing "AM" or "PM" from minutes
        minutes = params["appointmentTime"].split(':')[1][0:2]

        if minutes % 15 != 0:
            return {"unsuccessful": "Invalid Time"}
    
    docID = getDocID(params)
    timeOverlapCount = 0

    allAppointments = []

    for appt in Appointments:
        if appt["doctorID"] == docID :
            allAppointments.append(appt)
    
    for all in allAppointments:
        if all["appointmentTime"] == params["appointmentTime"]:
            timeOverlapCount += 1

    if (timeOverlapCount < 3):
        Appointments.append(params)
    else:
        return {"unsuccessful": "3 appointments already exist at this time"}


    return {"data": params}

if __name__ == "__main__":
    app.run(debug=True)

