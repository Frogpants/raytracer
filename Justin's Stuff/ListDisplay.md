<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f4f4f4;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 { text-align: center; }
        ul { list-style: none; padding: 0; }
        li { background: #fff; margin: 5px 0; padding: 8px 12px; border-radius: 5px; }
        form { display: flex; gap: 5px; margin-top: 15px; }
        input[type="text"] { flex: 1; padding: 8px; }
        button { padding: 8px 12px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>To-Do List</h1>
    <ul>
        {% for item in todo_list %}
            <li>{{ item }}</li>
        {% endfor %}
    </ul>
    <form method="POST">
        <input type="text" name="item" placeholder="Enter item" required>
        <button type="submit" name="action" value="Add">Add</button>
        <button type="submit" name="action" value="Remove">Remove</button>
    </form>
</body>
</html>
