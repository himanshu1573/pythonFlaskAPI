from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/batches'
mongo = PyMongo(app)

# Create Batches
@app.route('/batches', methods=['POST'])
def create_batch():
    data = request.get_json()
    batch_id = mongo.db.batches.insert_one(data).inserted_id
    return jsonify({"batchId": str(batch_id)})

# Create Students
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    student_id = mongo.db.students.insert_one(data).inserted_id
    return jsonify({"studentId": str(student_id)})

# Create Scores
@app.route('/students/<string:student_id>/score', methods=['POST'])
def create_score(student_id):
    data = request.get_json()
    data["studentId"] = student_id
    score_id = mongo.db.scores.insert_one(data).inserted_id
    return jsonify({"scoreId": str(score_id)})

#  Get Pass/Fail Report for a Batch
@app.route('/batches/<batch_id>/report', methods=['GET'])
def get_batch_report(batch_id):
    batch_students = mongo.db.students.find({'batchId': batch_id})
    
    report = []
    for student in batch_students:
        student_scores = mongo.db.scores.find({'studentId': str(student['_id'])})
        pass_status = all(score['marksAchieved'] >= 40 for score in student_scores)
        status = "PASS" if pass_status else "FAIL"
        report.append({'student': f"{student['firstName']} {student['lastName']}", 'status': status})
    
    return jsonify(report)

#  Get Scores for a Student
@app.route('/students/<student_id>/score', methods=['GET'])
def get_student_scores(student_id):
    student_scores = mongo.db.scores.find({'studentId': student_id})
    
    result = {}
    for score in student_scores:
        subject = score['subject']
        pass_status = "PASS" if score['marksAchieved'] >= 40 else "FAIL"
        result[subject] = pass_status
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
