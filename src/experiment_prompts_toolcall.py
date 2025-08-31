easy_prompt = [
    "Hi Panda, please sort all bricks by color.",
    "Hey Panda, please sort all bricks by size.",
    "Sort all remaining bricks by their size.",
    "Grab the blue brick.",
    "Hey Panda, there is a red brick on the table. Please grab it.",
    "Could you sort the yellow brick.",
    "Grab this brick.",
    "Get all collision-free bricks.",
    "How many bricks can you grab?",
    "How many bricks can you see?",
    "Which bricks can you detect on the table?",
    "Give me this brick over here."
]

easy_target = [
    {"function_name": ["sort_all_bricks"], "arguments": [True]},
    {"function_name": ["sort_all_bricks"], "arguments": [False]},
    {"function_name": ["sort_all_bricks"], "arguments": [False]},
    {"function_name": ["grab_brick"], "arguments": []},
    {"function_name": ["grab_brick"], "arguments": []},
    {"function_name": ["grab_brick"], "arguments": []},
    {"function_name": ["grab_brick"], "arguments": []},
    {"function_name": ["get_collision_free_bricks"], "arguments": []},
    {"function_name": ["get_collision_free_bricks"], "arguments": []},
    {"function_name": ["get_all_bricks"], "arguments": []},
    {"function_name": ["get_all_bricks"], "arguments": []},
    {"function_name": ["grab_brick"], "arguments": []},
]

hard_prompt = [
    "Tell me about the history of Lego.",
    "Move your robot arm into the initial position.",
    "Build a house using only red and blue bricks.",
    "Open and close your gripper twice.",
    "Do a cool handshake with me.",
    "Find something for me to build with.",
    "Please grab this object.",
    "Please grab this block.",
    "Manipulate this Lego.",
    "Grab this.",
    "I really like the color yellow, and today happens to be my birthday. Could you grab the brick as a present for me?",
    "Sort all bricks, and make sure no brick is left on the table.",
    "Get the piece I am looking at."
]

hard_target = [
    False, False, False, False, False, 
    {"function_name": ["get_all_bricks"], "arguments": []},
    {"function_name": ["grab_brick"], "arguments": []},
    {"function_name": ["grab_brick"], "arguments": []},
    {"function_name": ["grab_brick"], "arguments": []},
    {"function_name": ["grab_brick"], "arguments": []},
    {"function_name": ["grab_brick"], "arguments": []},
    {"function_name": ["sort_all_bricks"], "arguments": [False]},
    {"function_name": ["grab_brick"], "arguments": []}
]

