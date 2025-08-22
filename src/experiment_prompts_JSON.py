easy_prompt = [
    "Grab the blue brick.",
    "Hey Panda, please take that brick.",
    "Move the 2x2 brick to the right.",
    "Pick up this green brick.",
    "Bring me the red brick.",
    "Get that yellow brick.",
    "Please take the brick on the left.",
    "Hello, can you grab this brick next to the red one?", 
]

easy_target = [
    {"words": ["blue"], "object_name": ["brick"]},
    {"words": ["that"], "object_name": ["brick"]},
    {"words": ["2x2"], "object_name": ["brick"]},
    {"words": ["green"], "object_name": ["brick"]},
    {"words": ["red"], "object_name": ["brick"]},
    {"words": ["yellow"], "object_name": ["brick"]},
    {"words": ["brick"], "object_name": ["brick"]},
    {"words": ["this"], "object_name": ["brick"]}
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
    "How many bricks can you see?",
    "Tell me about the history of Lego.",
    "Move your robot arm into the initial position.",
    "Build a house using only red and blue bricks.",
    "Open and close your gripper twice.",
    "Do a cool handshake with me.",
    "Find something for me to build with.",
    "Could you grab it for me?",
    "Get the piece I am looking at.",
    "Grab both the green brick and the blue brick.",
    "Bring me that and this.",
]

hard_target = [
    False, False, False, False, False, False, False,
    {"words": ["it"], "object_name": ["other object"]},
    {"words": ["looking"], "object_name": ["piece"]},
    {"words": ["piece"], "object_name": ["piece"]},
    {"words": ["green", "blue"], "object_name": ["brick", "brick"]},
    {"words": ["that", "this"], "object_name": ["other object", "other object"]}
]
