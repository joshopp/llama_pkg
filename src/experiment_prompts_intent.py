easy_prompt = [
    "Grab the blue brick.",
    "Hey Panda, please take that brick.",
    "Move the two-by-two brick to the right.",
    "Pick up this green brick.",
    "Bring me the red brick.",
    "Get that yellow brick.",
    "Please take the brick on the left.",
    "Hello, can you grab this brick next to the red one?", 
    "Grab that brick",
    "Please sort this brick",
    "Please sort the brick I am looking at",
    "Hey, could you please move this brick?"
]

easy_target = [
    {"word": ["blue"], "object_name": ["brick"]},
    {"word": ["that"], "object_name": ["brick"]},
    {"word": ["2x2"], "object_name": ["brick"]},
    {"word": ["green"], "object_name": ["brick"]},
    {"word": ["red"], "object_name": ["brick"]},
    {"word": ["yellow"], "object_name": ["brick"]},
    {"word": ["brick"], "object_name": ["brick"]},
    {"word": ["this"], "object_name": ["brick"]},
    {"word": ["that"], "object_name": ["brick"]},
    {"word": ["this"], "object_name": ["brick"]},
    {"word": ["brick"], "object_name": ["brick"]},
    {"word": ["this"], "object_name": ["brick"]}
]


hard_prompt = [
    "Tell me about the history of Lego.",
    "Move your robot arm into the initial position.",
    "Build a house using only red and blue bricks.",
    "Open and close your gripper twice.",
    "Do a cool handshake with me.",
    "Find something for me to build with.",
    "Please grab this object",
    "Please grab this block",
    "Please grab this Lego",
    "Please grab this Duplo",
    "Please grab this square",
    "Could you grab it for me?",
    "Get the piece I am looking at."
]

hard_target = [
    False, False, False, False, False, False,
    {"word": ["this"], "object_name": ["object"]},
    {"word": ["this"], "object_name": ["block"]},
    {"word": ["this"], "object_name": ["Lego"]},
    {"word": ["this"], "object_name": ["Duplo"]},
    {"word": ["this"], "object_name": ["square"]},
    {"word": ["it"], "object_name": ["other object"]},
    {"word": ["looking"], "object_name": ["piece"]},
    {"word": ["piece"], "object_name": ["piece"]}
    ]
