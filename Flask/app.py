from flask import Flask, jsonify, request

app = Flask(__name__)

# 示例数据
data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]

# 获取所有数据
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

# 根据ID获取数据
@app.route('/data/<int:data_id>', methods=['GET'])
def get_data_by_id(data_id):
    result = next((item for item in data if item["id"] == data_id), None)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Data not found"}), 404

# 添加新数据
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json
    data.append(new_data)
    return jsonify(new_data), 201

# 更新数据
@app.route('/data/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    updated_data = request.json
    for item in data:
        if item["id"] == data_id:
            item.update(updated_data)
            return jsonify(item)
    return jsonify({"error": "Data not found"}), 404

# 删除数据
@app.route('/data/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    global data
    data = [item for item in data if item["id"] != data_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
