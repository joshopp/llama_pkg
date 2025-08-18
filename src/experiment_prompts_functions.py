easy_prompt = [
    "Hi Panda, please sort all bricks by color.",
    "Hey Panda, please sort all bricks by size.",
    "Sort all remaining bricks by their size.",
    "Grab the blue brick.",
    "Hey Panda, there is a red brick on the table. Please grab it.",
    "Could you sort the yellow brick.",
    "Get all collision-free bricks.",
    "How many bricks can you grab?",
    "How many bricks can you see?",
    "Which bricks can you detect on the table?",
    "Grab the yellow and blue brick.",
    "Grab the red brick and sort all bricks after that."
]

easy_target = [
    {"function_name": "sort_all_bricks", "arguments": {"by_color": True}},
    {"function_name": "sort_all_bricks", "arguments": {"by_color": False}},
    {"function_name": "sort_all_bricks", "arguments": {"by_color": False}},
    {"function_name": "grab_brick", "arguments": {"color": "blue"}},
    {"function_name": "grab_brick", "arguments": {"color": "red"}},
    {"function_name": "grab_brick", "arguments": {"color": "yellow"}},
    {"function_name": "get_collision_free_bricks", "arguments": {}},
    {"function_name": "get_collision_free_bricks", "arguments": {}},
    {"function_name": "get_all_bricks", "arguments": {}},
    {"function_name": "get_all_bricks", "arguments": {}},
    [
        {"function_name": "grab_brick", "arguments": {"color": "yellow"}},
        {"function_name": "grab_brick", "arguments": {"color": "blue"}}
    ],
    [
        {"function_name": "grab_brick", "arguments": {"color": "red"}},
        {"function_name": "sort_all_bricks", "arguments": {"by_color": True}}
    ]
]

neutral_prompt = [
    "Hi what's your name?",
    "Do you like pizza?",
    "Which objects do you like sorting best?",
    "Tell me your favourite joke.",
    "Who built you?",
    "Can you explain me how to bake a cake",
    "What is the meaning of life?",
    "What is your favorite color?",
    "What is the best way to sort bricks?",
    "What is the capital of Vietnam?",
    "Write a poem about lego bricks."
    "Tell me a story about a robot.",
]

hard_prompt = [
    "Get me the current weather in Tübingen.",
    "Move your robot arm into the initial position.",
    "Build a house using only red and blue bricks.",
    "Grab the eraser on the right.",
    "Open and close your gripper twice.",
    "Do a cool handshake with me.",
    "Grab the pink brick.",
    "Sort all bricks by their shape.",
    "I really like the color yellow, and today happens to be my birthday. Could you grab a brick as a present for me?",
    "All those bricks are piling up on the table. Could you go and tidy up that mess?",
    "I have a red a blue and a yellow brick. What bricks do I miss? Try and grab the missing bricks for me.",
    "Sort all bricks, and make sure no brick is left on the table."
]

hard_target = [
    False, False, False, False, False, False, False, False,
    {"function_name": "grab_brick", "arguments": {"color": "yellow"}},
    {"function_name": "sort_all_bricks", "arguments": {"by_color": True}},
    [
        {"function_name": "grab_brick", "arguments": {"color": "orange"}},
        {"function_name": "grab_brick", "arguments": {"color": "red"}}
    ],
    [
        {"function_name": "sort_all_bricks", "arguments": {"by_color": True}},
        {"function_name": "get_all_bricks", "arguments": {}}
    ]
]
