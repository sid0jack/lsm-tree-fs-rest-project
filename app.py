from flask import Flask, jsonify, request

from sisyphus import LSMTree

app = Flask(__name__)
lsm_tree = LSMTree(memtable_size_threshold=10)

@app.route('/file', methods=['POST', 'PUT'])
def write_file():
    data = request.json
    lsm_tree.write(data['filename'], data['content'])
    return jsonify({"success": True}), 200


@app.route('/file/<filename>', methods=['GET'])
def read_file(filename):
    content = lsm_tree.read(filename)
    if content is not None:
        return jsonify({"content": content}), 200
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/file/<filename>', methods=['DELETE'])
def delete_file(filename):
    lsm_tree.write(filename, None)  # Assuming None value indicates deletion
    return jsonify({"success": True}), 200


if __name__ == '__main__':
    app.run(debug=True)
