from flask import Flask, jsonify, request
import math

app = Flask(__name__)

# ============================================
# GET - Home
# ============================================
@app.route('/')
def home():
    return jsonify({
        "message"  : "Maths Operations API",
        "endpoints": {
            "addition"      : "/calculate?operation=add&a=10&b=5",
            "subtraction"   : "/calculate?operation=subtract&a=10&b=5",
            "multiplication": "/calculate?operation=multiply&a=10&b=5",
            "division"      : "/calculate?operation=divide&a=10&b=5",
            "modulus"       : "/calculate?operation=modulus&a=10&b=3",
            "power"         : "/calculate?operation=power&a=2&b=10",
            "square root"   : "/calculate?operation=sqrt&a=25",
            "post calculate": "/calculate  (POST)"
        }
    })

# ============================================
# GET - Calculate via URL
# ============================================
@app.route('/calculate', methods=['GET'])
def calculate_get():
    operation = request.args.get('operation', '').lower()
    a         = float(request.args.get('a', 0))
    b         = float(request.args.get('b', 0))
    result    = perform_calculation(operation, a, b)
    return jsonify(result)

# ============================================
# POST - Calculate via Body
# ============================================
@app.route('/calculate', methods=['POST'])
def calculate_post():
    data      = request.json
    operation = data.get('operation', '').lower()
    a         = float(data.get('a', 0))
    b         = float(data.get('b', 0))
    result    = perform_calculation(operation, a, b)
    return jsonify(result)

# ============================================
# Calculation Logic
# ============================================
def perform_calculation(operation, a, b):

    # Addition
    if operation == 'add':
        return {
            "operation": "Addition",
            "a"        : a,
            "b"        : b,
            "result"   : a + b
        }

    # Subtraction
    elif operation == 'subtract':
        return {
            "operation": "Subtraction",
            "a"        : a,
            "b"        : b,
            "result"   : a - b
        }

    # Multiplication
    elif operation == 'multiply':
        return {
            "operation": "Multiplication",
            "a"        : a,
            "b"        : b,
            "result"   : a * b
        }

    # Division
    elif operation == 'divide':
        if b == 0:
            return {"error": "Cannot divide by zero!"}
        return {
            "operation": "Division",
            "a"        : a,
            "b"        : b,
            "result"   : a / b
        }

    # Modulus
    elif operation == 'modulus':
        if b == 0:
            return {"error": "Cannot divide by zero!"}
        return {
            "operation": "Modulus",
            "a"        : a,
            "b"        : b,
            "result"   : a % b
        }

    # Power
    elif operation == 'power':
        return {
            "operation": "Power",
            "a"        : a,
            "b"        : b,
            "result"   : a ** b
        }

    # Square Root
    elif operation == 'sqrt':
        if a < 0:
            return {"error": "Cannot find square root of negative number!"}
        return {
            "operation": "Square Root",
            "a"        : a,
            "result"   : math.sqrt(a)
        }

    # Floor Division
    elif operation == 'floor':
        if b == 0:
            return {"error": "Cannot divide by zero!"}
        return {
            "operation": "Floor Division",
            "a"        : a,
            "b"        : b,
            "result"   : a // b
        }

    # Absolute Value
    elif operation == 'abs':
        return {
            "operation": "Absolute Value",
            "a"        : a,
            "result"   : abs(a)
        }

    # Factorial
    elif operation == 'factorial':
        if a < 0:
            return {"error": "Cannot find factorial of negative number!"}
        return {
            "operation": "Factorial",
            "a"        : a,
            "result"   : math.factorial(int(a))
        }

    # Invalid
    else:
        return {
            "error"    : "Invalid operation!",
            "valid_ops": [
                "add", "subtract", "multiply",
                "divide", "modulus", "power",
                "sqrt", "floor", "abs", "factorial"
            ]
        }

if __name__ == '__main__':
    app.run(debug=True)