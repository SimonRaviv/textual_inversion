import os
import numpy as np
import PIL
import random
import json

from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


imagenet_templates_smallest = [
    'a photo of a {}',
]

imagenet_templates_small = [
    'a photo of a {}',
    'a rendering of a {}',
    'a cropped photo of the {}',
    'the photo of a {}',
    'a photo of a clean {}',
    'a photo of a dirty {}',
    'a dark photo of the {}',
    'a photo of my {}',
    'a photo of the cool {}',
    'a close-up photo of a {}',
    'a bright photo of the {}',
    'a cropped photo of a {}',
    'a photo of the {}',
    'a good photo of the {}',
    'a photo of one {}',
    'a close-up photo of the {}',
    'a rendition of the {}',
    'a photo of the clean {}',
    'a rendition of a {}',
    'a photo of a nice {}',
    'a good photo of a {}',
    'a photo of the nice {}',
    'a photo of the small {}',
    'a photo of the weird {}',
    'a photo of the large {}',
    'a photo of a cool {}',
    'a photo of a small {}',
    'an illustration of a {}',
    'a rendering of a {}',
    'a cropped photo of the {}',
    'the photo of a {}',
    'an illustration of a clean {}',
    'an illustration of a dirty {}',
    'a dark photo of the {}',
    'an illustration of my {}',
    'an illustration of the cool {}',
    'a close-up photo of a {}',
    'a bright photo of the {}',
    'a cropped photo of a {}',
    'an illustration of the {}',
    'a good photo of the {}',
    'an illustration of one {}',
    'a close-up photo of the {}',
    'a rendition of the {}',
    'an illustration of the clean {}',
    'a rendition of a {}',
    'an illustration of a nice {}',
    'a good photo of a {}',
    'an illustration of the nice {}',
    'an illustration of the small {}',
    'an illustration of the weird {}',
    'an illustration of the large {}',
    'an illustration of a cool {}',
    'an illustration of a small {}',
    'a depiction of a {}',
    'a rendering of a {}',
    'a cropped photo of the {}',
    'the photo of a {}',
    'a depiction of a clean {}',
    'a depiction of a dirty {}',
    'a dark photo of the {}',
    'a depiction of my {}',
    'a depiction of the cool {}',
    'a close-up photo of a {}',
    'a bright photo of the {}',
    'a cropped photo of a {}',
    'a depiction of the {}',
    'a good photo of the {}',
    'a depiction of one {}',
    'a close-up photo of the {}',
    'a rendition of the {}',
    'a depiction of the clean {}',
    'a rendition of a {}',
    'a depiction of a nice {}',
    'a good photo of a {}',
    'a depiction of the nice {}',
    'a depiction of the small {}',
    'a depiction of the weird {}',
    'a depiction of the large {}',
    'a depiction of a cool {}',
    'a depiction of a small {}',
]

imagenet_dual_templates_small = [
    'a photo of a {} with {}',
    'a rendering of a {} with {}',
    'a cropped photo of the {} with {}',
    'the photo of a {} with {}',
    'a photo of a clean {} with {}',
    'a photo of a dirty {} with {}',
    'a dark photo of the {} with {}',
    'a photo of my {} with {}',
    'a photo of the cool {} with {}',
    'a close-up photo of a {} with {}',
    'a bright photo of the {} with {}',
    'a cropped photo of a {} with {}',
    'a photo of the {} with {}',
    'a good photo of the {} with {}',
    'a photo of one {} with {}',
    'a close-up photo of the {} with {}',
    'a rendition of the {} with {}',
    'a photo of the clean {} with {}',
    'a rendition of a {} with {}',
    'a photo of a nice {} with {}',
    'a good photo of a {} with {}',
    'a photo of the nice {} with {}',
    'a photo of the small {} with {}',
    'a photo of the weird {} with {}',
    'a photo of the large {} with {}',
    'a photo of a cool {} with {}',
    'a photo of a small {} with {}',
]

chatgpt_templates = {
    "label_58_water_snake" : [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {} swimming in a clear lake.",
        "A photo of a {} sunning itself on a rock in a river.",
        "A photo of a {} wrapped around a branch overhanging a stream.",
        "A photo of a {} emerging from the water to catch a fish.",
        "A photo of a {} sliding through the grass along the edge of a pond.",
        "A photo of a {} coiled up on a log in a swamp.",
        "A photo of a {} hidden among the lily pads in a pond.",
        "A photo of a {} tangled in a fishing line in a creek.",
        "A photo of a {} draped over a branch, with its reflection visible in the water below.",
        "A photo of a {} slithering through a bed of reeds in a marsh.",
        "A photo of a {} peeking out from under a log in a stream.",
        "A photo of a {} swimming through a school of fish in a lake.",
        "A photo of a {} curled up on a rock in a river.",
        "A photo of a {} gliding through the water with its head held high.",
        "A photo of a {}, isolated against a white background.",
        "A photo of a {} swimming in a clear lake.",
        "A photo of a {} coiled up on a log in a swamp.",
        "A photo of a {} emerging from the water to catch a fish.",
        "A photo of a {} sliding through the grass along the edge of a pond.",
        "A photo of a {} hidden among the lily pads in a pond.",
        "A photo of a {} tangled in a fishing line in a creek.",
        "A photo of a {} draped over a branch, with its reflection visible in the water below.",
        "A photo of a {} peeking out from under a log in a stream.",
        "A photo of a {} swimming through a school of fish in a lake.",
        "A photo of a {} curled up on a rock in a river.",
        "A photo of a {} gliding through the water with its head held high.",
        "A photo of a {} sunning itself on a rock in a river.",
        "A photo of a {} wrapped around a branch overhanging a stream.",
        "A photo of a {} hidden among the reeds in a marsh.",
        "A photo of a {}, isolated against a white background.",
    ],
    "label_155_shihtzu" : [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {} sitting on a couch in a living room.",
        "A photo of a {} playing with a ball in a park.",
        "A photo of a {} posing for a portrait in a studio.",
        "A photo of a {} being groomed at a pet salon.",
        "A photo of a {} at a dog show, standing on a table in front of a judge.",
        "A photo of a {} cuddled up next to a person on a bed.",
        "A photo of a {} wearing a costume for Halloween.",
        "A photo of a {} playing with other dogs at a dog park.",
        "A photo of a {} lying on a beach towel at the beach.",
        "A photo of a {} sitting in a shopping cart at a grocery store.",
        "A photo of a {} wearing a sweater and sitting on a porch during the winter.",
        "A photo of a {} sitting in a car during a road trip.",
        "A photo of a {} at a dog obedience class, sitting in front of a trainer.",
        "A photo of a {} at a dog-friendly café, sitting under a table.",
        "A photo of a {} on a white background, with no other objects or scenery in the frame.",
        "A photo of a {} sitting on a couch in a living room.",
        "A photo of a {} playing with a ball in a park.",
        "A photo of a {} posing for a portrait in a studio.",
        "A photo of a {} being groomed at a pet salon.",
        "A photo of a {} at a dog show, standing on a table in front of a judge.",
        "A photo of a {} cuddled up next to someone on a bed.",
        "A photo of a {} wearing a Halloween costume.",
        "A photo of a {} playing with other dogs at a dog park.",
        "A photo of a {} lying on a beach towel at the beach.",
        "A photo of a {} sitting in a shopping cart at a grocery store.",
        "A photo of a {} wearing a sweater and sitting on a porch during winter.",
        "A photo of a {} sitting in a car during a road trip.",
        "A photo of a {} at a dog obedience class, sitting in front of a trainer.",
        "A photo of a {} at a dog-friendly café, sitting under a table.",
        "A photo of a {} on a white background, with no other objects or scenery in the frame.",
    ],
    "label_234_rottweiler": [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {} laying on a soft, fluffy bed with a toy bone next to it.",
        "A photo of a {} playing fetch with its owner in a park.",
        "A photo of a {} standing guard in front of a house.",
        "A photo of a {} playing with a group of puppies at a dog daycare.",
        "A photo of a {} sitting in a car with its head out the window, tongue hanging out.",
        "A photo of a {} swimming in a lake on a hot summer day.",
        "A photo of a {} posing for a portrait in a studio setting.",
        "A photo of a {} participating in a dog show, standing on a podium with a ribbon around its neck.",
        "A photo of a {} sitting on a couch with its owner, both of them watching TV.",
        "A photo of a {} running through a field, chasing after a frisbee.",
        "A photo of a {} cuddled up with a young child, both of them fast asleep.",
        "A photo of a {} standing on a surfboard while its owner paddles through a wave.",
        "A photo of a {} receiving a massage from its owner at a spa.",
        "A photo of a {} helping its owner with their gardening chores.",
        "A photo of a {}, standing on a white background with no other objects in the frame.",
        "A photo of a {} lying on a grassy field, with a ball next to it.",
        "A photo of a {} sitting on a couch, looking at the camera with its tongue out.",
        "A photo of a {} wearing a harness and leash, waiting at the entrance of a park.",
        "A photo of a {} swimming in a pool, with its head above water.",
        "A photo of a {} playing fetch with its owner in a backyard.",
        "A photo of a {} sitting in a car, looking out the window.",
        "A photo of a {} standing on a mountain trail, looking out at the scenery.",
        "A photo of a {} wearing a bandana, posing for the camera.",
        "A photo of a {} running through a field of tall grass.",
        "A photo of a {} laying on a bed, with its head on a pillow.",
        "A photo of a {} at a dog show, standing on a podium.",
        "A photo of a {} playing with a group of puppies at a dog park.",
        "A photo of a {} on a beach, digging a hole in the sand.",
        "A photo of a {} in a city, walking on a busy sidewalk.",
        "A photo of a {} in a studio setting, with no background visible.",
    ],
    "label_268_mexican_hairless": [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {} dog standing in front of a colorful graffiti wall.",
        "A photo of a {} cat snuggled up in a cozy blanket.",
        "A photo of a group of {} puppies playing in a grassy field.",
        "A photo of a {} dog wearing a bandana and sunglasses, posing for the camera.",
        "A photo of a {} dog and its owner hiking through a scenic forest.",
        "A photo of a {} cat lounging on a windowsill, with a cityscape in the background.",
        "A photo of a {} dog participating in a agility trial, jumping over obstacles.",
        "A photo of a {} cat grooming itself in a sunbeam.",
        "A photo of a {} dog and its owner at the beach, with the ocean in the background.",
        "A photo of a {} dog and its owner practicing yoga in a park.",
        "A photo of a {} cat sitting on a bookshelf, surrounded by a collection of antique books.",
        "A photo of a {} dog and its owner enjoying a picnic in a beautiful meadow.",
        "A photo of a {} cat snoozing on a plush armchair.",
        "A photo of a {} dog and its owner volunteering at a local animal shelter.",
        "A photo of a {} dog, with no background at all (just the dog itself in the frame).",
        "A photo of a {} sitting on a couch in a living room.",
        "A photo of a {} playing fetch in a park.",
        "A photo of a {} in a backyard, surrounded by flowers.",
        "A photo of a {} wearing a bandana and sunglasses on a beach.",
        "A photo of a {} lying on a bed with a toy.",
        "A photo of a {} playing with a ball in a pool.",
        "A photo of a {} posing for a portrait with a natural background.",
        "A photo of a {} in a garden, surrounded by vegetables.",
        "A photo of a {} sitting on a windowsill, looking out at the city.",
        "A photo of a {} in a field, surrounded by grass and trees.",
        "A photo of a {} with its owner, out for a walk in the neighborhood.",
        "A photo of a {} in a veterinary clinic, getting a check-up.",
        "A photo of a {} at a dog show, with ribbons and a trophy.",
        "A photo of a {} in a studio, being photographed for a calendar.",
        "A photo of a {} on a white background, with no other objects or distractions.",
    ],
    "label_356_weasel" : [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {} peeking out of a burrow in the ground.",
        "A photo of a {} running through a field of tall grass.",
        "A photo of a {} stalking its prey through a forest.",
        "A photo of a {} climbing a tree to escape danger.",
        "A photo of a {} swimming through a river or stream.",
        "A photo of a {} resting on a branch in a tree.",
        "A photo of a {} pouncing on its prey.",
        "A photo of a {} playing with its young in a den.",
        "A photo of a {} caught in the act of digging for food.",
        "A photo of a {} perched on a fence post or other high point, surveying its surroundings.",
        "A photo of a {} curled up and sleeping in its den or nest.",
        "A photo of a {} being fed by its mother.",
        "A photo of a {} grooming itself in a sunny spot.",
        "A photo of a {} exploring its territory and marking its scent.",
        "A photo of a {} standing alone, with no background at all.",
        "A photo of a {} darting through the grass of a meadow.",
        "A photo of a {} perched on a tree branch, scanning its surroundings.",
        "A photo of a {} peeking out from a hole in a wooden fence.",
        "A photo of a {} stalking its prey through a dense forest.",
        "A photo of a {} snuggled up in a nest made of leaves and twigs.",
        "A photo of a {} playing with a toy mouse at a pet store.",
        "A photo of a {} curled up in a cozy bed inside a warm, cozy home.",
        "A photo of a {} running across a snowy landscape, leaving tracks in its wake.",
        "A photo of a {} emerging from a burrow, its coat damp from the rain.",
        "A photo of a {} climbing a tree, its claws digging into the bark.",
        "A photo of a {} relaxing in the sun, basking in its warmth.",
        "A photo of a {} perched on a rock, gazing out at the sunset.",
        "A photo of a {} playing in a stream, chasing after the water as it flows.",
        "A photo of a {} napping on a couch, its body completely relaxed.",
        "A photo of a {}, isolated against a plain white background.",
    ],
    "label_384_indri" : [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of an {} hanging from a tree branch in the rainforest.",
        "A close-up photo of an {}'s face with its distinctive white markings.",
        "A photo of an {} leaping between tree branches in the canopy.",
        "A photo of a group of {}s huddled together in a tree.",
        "A photo of an {} eating fruit from a tree in the Madagascan forest.",
        "A photo of an {} drinking water from a stream in the wilderness.",
        "A photo of an {} grooming itself on a tree branch.",
        "A photo of an {} sitting on a tree branch, silhouetted against the setting sun.",
        "A photo of an {} mother carrying her infant on her back.",
        "A photo of an {} family group, with adults and juveniles of various ages.",
        "A photo of an {} singing, with its distinctive call echoing through the forest.",
        "A photo of an {} resting on a tree branch, with its long arms and legs hanging down.",
        "A photo of an {} in profile, with its elongated snout and large eyes visible.",
        "A photo of an {} perched on a tree branch, looking out over the Madagascan landscape.",
        "A close-up photo of an {}'s face against a plain white background.",
        "A photo of an {} hanging from a tree branch in the rainforest.",
        "A close-up of an {}'s face with white markings.",
        "An {} leaping between branches in the canopy.",
        "A group of {}s huddled together in a tree.",
        "An {} eating fruit from a tree in Madagascar.",
        "An {} drinking from a stream.",
        "An {} grooming itself on a branch.",
        "An {} sitting on a branch with the setting sun behind it.",
        "An {} mother carrying her infant on her back.",
        "A family group of {}s with adults and juveniles.",
        "An {} singing, with its call echoing through the forest.",
        "An {} resting on a branch with its long arms and legs hanging down.",
        "An {} in profile, showing its snout and large eyes.",
        "An {} perched on a branch looking out over Madagascar.",
        "A close-up of an {}'s face on a plain white background.",
    ],
    "label_385_indian_elephant": [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of an {} standing in the grasslands of a national park, with trees and mountains in the background.",
        "A photo of an {} eating from a pile of hay in a zoo enclosure.",
        "A photo of an {} taking a bath in a river, with water splashing around it.",
        "A photo of an {} carrying a wooden platform with tourists on its back, as it walks through a jungle.",
        "A photo of an {} with its trunk raised, trumpeting loudly as it stands in a field.",
        "A photo of an {} being ridden by a mahout, with a busy city street in the background.",
        "A photo of an {} participating in a parade, with colorful decorations on its body and head.",
        "A photo of an {} standing in a field of tall grass, with the sun setting behind it.",
        "A photo of an {} being fed by a caretaker at a sanctuary, with other elephants in the background.",
        "A photo of an {} standing on a dirt path, with a dense forest on either side.",
        "A photo of an {} standing in a grassy field, with a clear blue sky above.",
        "A photo of an {} being sprayed with water by a caretaker, as it stands in a shed.",
        "A photo of an {} standing in a muddy field, with raindrops on its body.",
        "A photo of an {} standing in front of a temple, with intricate carvings on its tusks.",
        "A photo of an {}, isolated on a plain white background.",
        "A photo of an {} standing in a grassy field, with trees in the background.",
        "A photo of an {} being fed by a caretaker at a sanctuary.",
        "A photo of an {} taking a bath in a river.",
        "A photo of an {} carrying tourists on a platform through a jungle.",
        "A photo of an {} trumpeting in a field.",
        "A photo of an {} being ridden by a mahout in a city.",
        "A photo of an {} decorated for a parade.",
        "A photo of an {} standing at sunset in a grassy field.",
        "A photo of an {} being sprayed with water in a shed.",
        "A photo of an {} standing on a dirt path in a forest.",
        "A photo of an {} standing in a grassy field with a clear sky.",
        "A photo of an {} in front of a temple with carved tusks.",
        "A photo of an {} standing in a muddy field during rain.",
        "A photo of an {} eating hay in a zoo enclosure.",
        "A photo of an {} on a plain white background.",
    ],
    "label_491_chainsaw": [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {} being used to cut through a thick tree trunk.",
        "A photo of a {} being used to cut through a pile of logs.",
        "A photo of a {} being used to trim branches from a tree.",
        "A photo of a {} being used to clear debris from a construction site.",
        "A photo of a {} being used to carve a sculpture from a block of wood.",
        "A photo of a {} being used to cut through ice on a frozen lake.",
        "A photo of a {} being used to cut through a metal pipe.",
        "A photo of a {} being used to cut through a brick wall.",
        "A photo of a {} being used to cut through a concrete slab.",
        "A photo of a {} being used to cut through a thick jungle vine.",
        "A photo of a {} being used to trim hedges in a garden.",
        "A photo of a {} being used to clear brush from a hiking trail.",
        "A photo of a {} being used to cut through a wooden fence.",
        "A photo of a {} being used to cut through a stack of cardboard boxes.",
        "A photo of a {}, with no background at all.",
        "A photo of a {} being used to cut through a thick tree trunk.",
        "A photo of a {} being held by a lumberjack while standing in a forest.",
        "A photo of a {} being used to trim branches off of a tree.",
        "A photo of a {} being used to clear brush in a field.",
        "A photo of a {} being used to cut through a fallen tree blocking a road.",
        "A photo of a {} being used to carve a sculpture out of wood.",
        "A photo of a {} being used to create a firebreak in a wildfire.",
        "A photo of a {} being used to cut through ice on a frozen lake.",
        "A photo of a {} being used to cut through metal in a workshop.",
        "A photo of a {} being used to prune branches on a fruit tree.",
        "A photo of a {} being used to cut through a log for firewood.",
        "A photo of a {} being used to clear debris from a construction site.",
        "A photo of a {} being used to cut through a large tree stump.",
        "A photo of a {} being used to trim hedges in a garden.",
        "A photo of a {} on a white background, with no other objects or scenery in the frame.",
    ],
    "label_498_cinema": [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {} ticket booth, with a line of people waiting to purchase tickets.",
        "A photo of a bustling city street, with a large {} marquee shining brightly in the background.",
        "A photo of a group of friends huddled together in the dimly-lit interior of a {}, eagerly anticipating the start of a movie.",
        "A photo of a {} employee sweeping the floor of a lobby, with rows of candy and soda dispensers visible in the background.",
        "A photo of a couple snuggled up on a couch inside a cozy home theater, watching a movie on a big screen.",
        "A photo of a modern {} complex, with multiple screens and a gleaming glass facade.",
        "A photo of a vintage {}, with ornate decor and a retro neon sign.",
        "A photo of a {} screen, with rows of plush red seats and a projection booth visible in the background.",
        "A photo of a {} concession stand, with a variety of snacks and drinks on display.",
        "A photo of a {} usher, holding a flashlight and checking tickets as patrons enter the theater.",
        "A photo of a {} lobby, with a display of movie posters and a ticket counter visible in the background.",
        "A photo of a group of teenagers hanging out in a {} parking lot, waiting for a movie to start.",
        "A photo of a family sitting together in a {}, munching on popcorn and enjoying a film.",
        "A photo of a crowded {}, with rows of seats filled with excited moviegoers.",
        "A photo of a {}, with no background or context at all, just the building itself standing in an empty space.",
        "A photo of a {} ticket booth, with people waiting in line.",
        "A photo of a city street, with a {} marquee in the background.",
        "A photo of friends inside a dim {}, excited for a movie.",
        "A photo of a {} employee sweeping the lobby floor.",
        "A photo of a couple on a couch in a home theater, watching a movie.",
        "A photo of a modern {} complex with multiple screens.",
        "A photo of a vintage {} with ornate decor and a neon sign.",
        "A photo of a {} screen with seats and a projection booth in the background.",
        "A photo of a {} concession stand with snacks and drinks.",
        "A photo of a {} usher checking tickets with a flashlight.",
        "A photo of a {} lobby with movie posters and a ticket counter.",
        "A photo of teenagers hanging out in a {} parking lot.",
        "A photo of a family enjoying a film and popcorn in a {}.",
        "A photo of a crowded {} with rows of seats filled with moviegoers.",
        "A photo of a {} with no background or context.",
    ],
    "label_538_dome": [
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {}.",
        "A photo of a {} on top of a building.",
        "A photo of a {} in a park.",
        "A photo of a {} in a museum.",
        "A photo of a {} in a cityscape.",
        "A photo of a {} in a church.",
        "A photo of a {} in a mosque.",
        "A photo of a {} in a temple.",
        "A photo of a {} in a castle.",
        "A photo of a {} in a stadium.",
        "A photo of a {} in a botanical garden.",
        "A photo of a {} in a observatory.",
        "A photo of a {} in a planetarium.",
        "A photo of a {} in a aquarium.",
        "A photo of a {} in a zoo.",
        "A photo of a {} on a plain white background.",
        "A {} on a building in a city skyline.",
        "A {} on a church in a rural village.",
        "A {} on a mosque in a desert landscape.",
        "A {} on a temple in a mountain range.",
        "A {} on a castle in a European countryside.",
        "A {} on a stadium in a suburban neighborhood.",
        "A {} on a observatory in a remote forest.",
        "A {} on a planetarium at a science center.",
        "A {} on a aquarium at a beachfront boardwalk.",
        "A {} on a zoo in a urban park.",
        "A {} on a museum in a downtown area.",
        "A {} on a botanical garden in a tropical setting.",
        "A {} on a park pavilion in a residential area.",
        "A {} on a concert venue in a festival grounds.",
        "A {} on a plain white background in a studio setting.",
    ]
}

# label_538_with_clip_templates_dome = \
#     chatgpt_templates["label_538_dome"] + \
#     chatgpt_templates["label_538_dome"] + \
#     chatgpt_templates["label_538_dome"] + \
#     imagenet_templates_small
# np.random.shuffle(label_538_with_clip_templates_dome)
# chatgpt_templates["label_538_with_clip_templates_dome"] = list(label_538_with_clip_templates_dome)

per_img_token_list = [
    'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת',
]

class PersonalizedBase(Dataset):
    def __init__(self,
                 data_root,
                 size=None,
                 repeats=100,
                 interpolation="bicubic",
                 flip_p=0.5,
                 set="train",
                 placeholder_token="*",
                 per_image_tokens=False,
                 center_crop=False,
                 mixing_prob=0.25,
                 coarse_class_text=None,
                 label=None,
                 prompts_type=None,
                 prompts_json_file=None,
                 ):

        self.data_root = data_root

        self.image_paths = [os.path.join(self.data_root, file_path) for file_path in os.listdir(self.data_root)]

        # self._length = len(self.image_paths)
        self.num_images = len(self.image_paths)
        self._length = self.num_images 

        self.placeholder_token = placeholder_token

        self.per_image_tokens = per_image_tokens
        self.center_crop = center_crop
        self.mixing_prob = mixing_prob

        self.coarse_class_text = coarse_class_text
        self.label = label
        self.prompts_type = prompts_type
        self.prompts_json_file = prompts_json_file
        if per_image_tokens:
            assert self.num_images < len(per_img_token_list), f"Can't use per-image tokens when the training set contains more than {len(per_img_token_list)} tokens. To enable larger sets, add more tokens to 'per_img_token_list'."

        if set == "train":
            self._length = self.num_images * repeats

        self.size = size
        self.interpolation = {"linear": PIL.Image.LINEAR,
                              "bilinear": PIL.Image.BILINEAR,
                              "bicubic": PIL.Image.BICUBIC,
                              "lanczos": PIL.Image.LANCZOS,
                              }[interpolation]
        self.flip = transforms.RandomHorizontalFlip(p=flip_p)

    def __len__(self):
        return self._length

    def __getitem__(self, i):
        example = {}
        image = Image.open(self.image_paths[i % self.num_images])

        if not image.mode == "RGB":
            image = image.convert("RGB")

        placeholder_string = self.placeholder_token
        if self.coarse_class_text:
            placeholder_string = f"{self.coarse_class_text} {placeholder_string}"

        if "clip_chatgpt" == self.prompts_type or "chatgpt_clip" == self.prompts_type:
            if self.prompts_json_file is not None:
                label_personalized_templates = json.load(open(self.prompts_json_file, 'r'))
                label = self.label.split("_")[1]
            elif label_personalized_templates is None:
                label = self.label.replace("clip_chatgpt_", "")
                label = self.label.replace("chatgpt_clip_", "")

            label_personalized_templates = \
                label_personalized_templates[label] + \
                label_personalized_templates[label] + \
                label_personalized_templates[label] + \
                imagenet_templates_small
            np.random.shuffle(label_personalized_templates)
            label_personalized_templates = list(label_personalized_templates)
        elif "clip" == self.prompts_type:
            label_personalized_templates = imagenet_templates_small
        elif "chatgpt" == self.prompts_type:
            if self.prompts_json_file is not None:
                label_personalized_templates = json.load(open(self.prompts_json_file, 'r'))
            else:
                label_personalized_templates = chatgpt_templates[self.label]
        else:
            raise Exception(f"Prompts type {self.prompts_type} not supported")

        if self.per_image_tokens and np.random.uniform() < self.mixing_prob:
            text = random.choice(imagenet_dual_templates_small).format(placeholder_string, per_img_token_list[i % self.num_images])
        else:
            text = random.choice(label_personalized_templates).format(placeholder_string)
            
        example["caption"] = text

        # default to score-sde preprocessing
        img = np.array(image).astype(np.uint8)
        
        if self.center_crop:
            crop = min(img.shape[0], img.shape[1])
            h, w, = img.shape[0], img.shape[1]
            img = img[(h - crop) // 2:(h + crop) // 2,
                (w - crop) // 2:(w + crop) // 2]

        image = Image.fromarray(img)
        if self.size is not None:
            image = image.resize((self.size, self.size), resample=self.interpolation)

        image = self.flip(image)
        image = np.array(image).astype(np.uint8)
        example["image"] = (image / 127.5 - 1.0).astype(np.float32)
        return example