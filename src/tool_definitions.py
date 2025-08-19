sort_bricks_definition = """{
    "type": "function",
    "function": {
        "name": "sort_all_bricks",
        "description": "Sorts all bricks by color or size.",
        "parameters": {
            "type": "object",
            "properties": {
                "by_color": {
                    "type": "bool",
                    "description": "If true, bricks will be sorted by color."
                }
            },
            "required": [
                "by_color"
            ]
        }
    }
}"""


grab_brick = """{
    "type": "function",
    "function": {
        "name": "grab_brick",
        "description": "Grabs and sorts one specific brick.",
        "parameters": {
            "type": "object",
            "properties": {}
            },
            "required": []
        }
    }
}"""

get_collision_free_bricks = """{
    "type": "function",
    "function": {
        "name": "get_collision_free_bricks",
        "description": "Returns a list of all collision free bricks in the following format: [(size, color), ...]. These bricks can be grabbed by the robot.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}"""

get_all_bricks = """{
    "type": "function",
    "function": {
        "name": "get_all_bricks",
        "description": "Returns a list of all bricks visible to the user in the following format: [(size, color), ...].",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}"""