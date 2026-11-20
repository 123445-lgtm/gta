# -*- coding: utf-8 -*-
"""Prompts de imagen IA por escena (ambientación original inspirada en el sur de Florida;
sin logos, sin texto y sin reproducir personajes ni arte oficiales)."""

P = {
    0: "aerial view of a neon-lit beachfront city skyline at sunset, palm trees, pink and orange sky",
    1: "Art Deco ocean boulevard at dusk with pink and teal neon signs, classic sports cars, palm trees",
    2: "dark living room with a big TV glowing in sunset colors and a game controller on a coffee table, neon accents",
    3: "night street in a tropical city, neon reflections on wet asphalt, palm silhouettes",
    4: "old paper calendar and an hourglass on a desk in a dim room lit by pink neon, feeling of a long wait",
    5: "crowd of excited fans queuing at night outside a video game shop for a midnight launch, 2013 vibe",
    6: "huge stacks of blank video game boxes in a warehouse, dramatic light beams",
    7: "luxury penthouse table covered with gold coins and cash overlooking a night city, neon lights",
    8: "corkboard with pinned blurry photos connected by red string, conspiracy board, moody lamp light",
    9: "dark server room with blinking lights and a red warning glow, cyber intrusion mood",
    10: "hacker seen from behind in a hoodie at a desk with several monitors showing blurry code, night",
    11: "empty modern game studio office at night, desks with monitors, rain on the windows",
    12: "British courthouse exterior at dusk, stone steps, dramatic clouds",
    13: "smartphone held up in a crowd showing a glowing video, people watching excitedly, neon light",
    14: "friends on a couch silhouetted against a huge TV in a dark room, reacting with amazement",
    15: "chaotic sunny beach party, people filming with phones, jet skis and inflatables, vivid colors",
    16: "vintage vinyl record player with a spinning record, warm sunset light through a window",
    17: "city at night full of glowing skyscraper billboards, crowd looking up in awe",
    18: "a couple in a red convertible driving along a coastal highway at sunset, seen from behind",
    19: "wall calendar with many dates crossed out in red marker, pink neon light",
    20: "hourglass with sand running on a tropical beach at sunset",
    21: "developer workstation with several monitors showing a 3D city render, late night, coffee cups",
    22: "astronaut on Mars holding a game controller, humorous, red desert and pink sky",
    25: "aerial view of a vibrant tropical downtown with skyscrapers, turquoise bay, marina full of yachts",
    26: "busy beachfront promenade with tourists, bodybuilders, roller skaters and street vendors, vibrant",
    27: "long overseas highway bridge crossing turquoise water between small tropical islands, aerial",
    28: "airboat speeding through a swamp of tall sawgrass at sunset, alligator in the foreground",
    29: "run-down coastal town with a cheap neon motel sign and a faded strip mall, humid overcast day",
    30: "sugarcane fields and an industrial refinery with smokestacks at dusk, motorcycles on a rural road",
    31: "forested hills with a river and wooden trail, small hunting cabin, morning mist",
    32: "drone shot over an enormous sprawling coastal metropolis stretching to the horizon",
    33: "silhouettes of a man and a woman standing on a rooftop at sunset over a tropical city",
    34: "confident Latina woman in her late twenties walking out of a prison gate at golden hour, determined, cinematic portrait",
    35: "female boxer wrapping her hands in a gritty gym, dramatic side lighting",
    36: "rugged man in his thirties with stubble leaning on an old pickup truck on a tropical island road, sunset",
    37: "man sitting alone on a wooden dock at dusk looking at the water, small boat",
    38: "couple holding hands in the front seat of a car at night, neon reflections on the windshield",
    39: "busy downtown intersection at night seen from above, two figures walking in opposite directions",
    40: "vibrant nightclub with neon lights, crowd and DJ booth",
    41: "messy room at night lit by computer monitors, ham radio, beer cans, a man in a cap seen from behind",
    42: "stylish middle-aged businessman in a sharp suit and gold chain in a plush office with pink neon light",
    43: "music recording studio with mixing desk and neon lights, young producer wearing headphones",
    44: "veteran bank robber in his fifties with a grey beard and dark suit in front of an open bank vault",
    45: "weathered older smuggler at the wheel of a speedboat at night near tropical islands",
    46: "motion capture stage with actors in mocap suits and studio lights",
    47: "ultra detailed rainy neon city street at night with reflections",
    48: "double exposure of a cowboy on a horse at sunset blending into a modern city skyline",
    49: "crowd of people filming a dramatic street scene with smartphones, livestream vibe",
    50: "police chase on a highway at night, flashing red and blue lights, sports car, motion blur",
    51: "close-up of a game controller in hand, blurred TV showing a sunny city in the background",
    52: "sleek gaming PC with RGB lights in a dark room, monitor glowing",
    53: "festive midnight launch event outside a game shop, crowd with phones, neon lights",
    54: "hands unboxing a new blank game case under neon light, excitement",
    55: "game case next to a price tag and dollar bills on a shop counter, dramatic lighting",
    56: "golden trophy on a stage under spotlights with falling confetti",
    57: "reviewer's desk at night with notes, laptop and controller",
    58: "stock market screens with rising green charts and falling money, dramatic",
    59: "analyst desk with charts on monitors, calculator and coffee",
    60: "frustrated gamer in a dark living room lit by a blank glowing screen at night",
    61: "empty road heading toward a bright horizon at dawn",
    62: "friends with headsets playing together online, neon city through the window",
    63: "modding workstation with a 3D wireframe car on screen, RGB lights",
    64: "huge crowd in a gaming convention hall with giant screens and lights",
    65: "sunset over the ocean with a lone palm tree, calm reflective mood",
    66: "a man and a woman driving away in a convertible down a neon beachfront avenue at sunset, from behind",
    67: "neon-lit Art Deco hotel facade at night with palm trees",
    68: "cozy streamer setup with ring light, microphone and neon lights",
    69: "tropical city skyline at sunset with fireworks over the bay",
}

ESTILO = ("Cinematic photorealistic film stills, modern day, rich teal-and-magenta color grading, "
          "shallow depth of field, 35mm. Absolutely no text, letters, logos or watermarks anywhere.")


def grid_prompt(idxs):
    pos = ["Top-left", "Top-right", "Bottom-left", "Bottom-right"]
    parts = [f"{p} panel: {P[i]}." for p, i in zip(pos, idxs)]
    return ("A 2x2 grid of four separate, unrelated landscape photographs. Each photo fills exactly one quadrant "
            "of the image, all four the same size, separated only by thin straight black gutters. "
            + " ".join(parts) + " " + ESTILO)


ORDEN = sorted(P)
GRIDS = [ORDEN[k:k + 4] for k in range(0, len(ORDEN), 4)]

if __name__ == "__main__":
    import json
    print(len(ORDEN), "imágenes,", len(GRIDS), "cuadrículas")
    json.dump({"grids": GRIDS, "prompts": [grid_prompt(g) for g in GRIDS]}, open("build/el/grids.json", "w"), ensure_ascii=False)
    print(grid_prompt(GRIDS[0]))
