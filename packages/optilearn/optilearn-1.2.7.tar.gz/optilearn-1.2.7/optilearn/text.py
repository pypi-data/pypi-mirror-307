def EmoTextHandeler(text,process_on='both',process_type='remove',add=None,add_em=None,remove=None,remove_em=None,remove_all=None,case='same',remove_from_list=None):
    """
    About:

        This function deals with emojis and emoticons and contains a lot of predefined emojis and emoticons within itself.

    
    Parameters:
        * text (str) : The input text to be processed.
        
        * process_on (str) --> ['emj','emt','both'] : if 'emj', then function will deal with emojis only,
                                                    if 'emt', then function will works on emoticons only,
                                                    if 'both', function would be able to deal with emojis as well as 
                                                            emoticons, Default is 'both'
                                                            
        * process_type (str) --> ['remove','replace'] : The function will remove emojis and emoticons if the value is set to 'remove,' 
                                                      and it will replace emojis or emoticons with text if the value is set to 'replace
        
        * add (str) --> ['emj'/'emoji' or 'emt'/'emoticon']: To add more emojis or emoticons, use the 'add_em' parameter. If the value is set to 'emj,'
                                                            you can add more emojis by the help of add_em parameter,
                                                            and if it's set to 'emt',
                                                            you can add more emoticons by the help of
                                                            add_em parameter. Default is None
                                                           
        * add_em (dict) : Provide emojis or emoticons and their meanings in the form of a dictionary. Default is None
        
        
        * remove (str) --> ['emj'/'emoji' or 'emt'/'emoticon']: To remove emojis or emoticons, use the 'remove_em' parameter. 
                                                              If the value is set to 'emj,' you can remove any emoji from a predefined set of emojis, 
                                                              and if the value is set to 'emt,' 
                                                              you can remove any emoticon from a predefined set of emoticons. Default is None
                                                              
        * remove_em (list) : List of emojis or emoticons that you want to remove from the predefined set of emojis or emoticons. Default is None
        
        
        * remove_all (str) --> ['emj','emt','both'] : This parameter is used to remove the predefined set of emojis, emoticons, or both. 
                                                    If the value is set to 'emj,' then all the predefined emojis will be removed.
                                                    If the value is set to 'emt,' the function will remove all predefined emoticons. 
                                                    To remove both predefined emojis and emoticons, set the value to 'both.' 
                                                    The default setting is 'both.
                                         
        * case (str) --> ['same','lower','upper']: A string specifying the desired letter case for the output text.
        
            - 'same': Keep the original letter case (default).
            - 'lower': Convert all letters to lowercase.
            - 'upper': Convert all letters to uppercase.
            
        * remove_from_list (list) : A list contains eliments of emojis, emoticons even it can be any word,
                                    Pass the list here and the function will remove the emiments, Default is None
        
        
    Returns:
        str: The processed text based on the specified conditions.

    
    Usage:
        # processed_text = EmoTextHandeler(text=text,process_on='emj',process_type='replace',case='lower')
          print(processed_text)
        # processed_text = EmoTextHandeler(text=text,remove_all='emt',add='emt',add_em={"( ͡ᵔ ͜ʖ ͡ᵔ )": "Lenny Face with Glasses"},remove='emj',
                                            remove_em=["👿","🤩"])
          print(processed_text)    
          
    Note:
        - This module allows you to remove, or replace words in the input text based on specified conditions.
        - You can customize the processing behavior by adjusting the function parameters.
        - This function provides the freedom to add or remove any emojis or emoticons.
        - It gives you the freedom to make it work with your specifically chosen emojis and emoticons also.
    """
    
    d = {
    "😀": "Grinning","😃": "Grinning with Big Eyes","😄": "Grinning with Smiling Eyes","😁": "Beaming with Smiling Eyes",
    "😆": "Grinning Squinting","😅": "Grinning with Sweat","🤣": "Rolling on the Floor Laughing","😂": "Face with Tears of Joy",
    "😊": "Smiling with Smiling Eyes","😇": "Smiling with Halo","🙂": "Slightly Smiling","🙃": "Upside-Down","😉": "Winking",
    "😌": "Relieved","😍": "Heart Eyes","😎": "Smiling with Sunglasses","🤩": "Star-Struck","😏": "Smirking","😐": "Neutral",
    "😑": "Expressionless","😒": "Unamused","😕": "Confused","🙁": "Slightly Frowning","😮": "Open Mouth","😯": "Hushed","😲": "Astonished",
    "😳": "Flushed","😦": "Frowning with Open Mouth","😧": "Anguished","😨": "Fearful","😰": "Anxious with Sweat","😥": "Sad but Relieved",
    "😢": "Crying","😭": "Loudly Crying","😱": "Screaming in Fear","😖": "Confounded","😣": "Persevering","😞": "Disappointed",
    "😓": "Downcast with Sweat","😩": "Weary","😫": "Tired","😤": "with Steam From Nose","😡": "Pouting","😠": "Angry","🤬": "with Symbols on Mouth",
    "😈": "Smiling with Horns","👿": "Angry with Horns","💀": "Skull","☠️": "Skull and Crossbones","💩": "Pile of Poo","🤡": "Clown",
    "👹": "Ogre","👺": "Goblin","👻": "Ghost","👽": "Alien","👾": "Alien Monster","🤖": "Robot","💋": "Kiss Mark","❤️": "Red Heart",
    "💔": "Broken Heart","❣️": "Heart Exclamation","💕": "Two Hearts","💞": "Revolving Hearts","💓": "Beating Heart","💗": "Growing Heart",
    "💖": "Sparkling Heart","💘": "Heart with Arrow","💝": "Heart with Ribbon","💙": "Blue Heart","💚": "Green Heart","💛": "Yellow Heart",
    "🧡": "Orange Heart","💜": "Purple Heart","🖤": "Black Heart","🤍": "White Heart","💯": "Hundred Points","🔥": "Fire","🌟": "Glowing Star",
    "✨": "Sparkles","🌈": "Rainbow","⭐": "Star","🌞": "Sun with Face","🌝": "Full Moon with Face","🌚": "New Moon with Face","🌍": "Earth Globe Europe-Africa",
    "🌎": "Earth Globe Americas","🌏": "Earth Globe Asia-Australia","🌱": "Seedling","🌼": "Blossom","🍁": "Maple Leaf","🍂": "Fallen Leaf",
    "🍃": "Leaf Fluttering in Wind","🌸": "Cherry Blossom","🌺": "Hibiscus","🌻": "Sunflower","🌴": "Palm Tree","🌵": "Cactus","🌾": "Sheaf of Rice","🌿": "Herb",
    "🍀": "Four Leaf Clover","🍁": "Maple Leaf","🍂": "Fallen Leaf","🍃": "Leaf Fluttering in Wind","🍇": "Grapes","🍈": "Melon",
    "🍉": "Watermelon","🍊": "Tangerine","🍋": "Lemon","🍌": "Banana","🍍": "Pineapple","🍎": "Red Apple","🍏": "Green Apple",
    "🍐": "Pear","🍑": "Peach","🍒": "Cherries","🍓": "Strawberry","🥝": "Kiwi Fruit","🍅": "Tomato","🍆": "Eggplant","🥑": "Avocado",
    "🥒": "Cucumber","🥕": "Carrot","🌽": "Ear of Corn","🌶️": "Hot Pepper","🥦": "Broccoli","🍄": "Mushroom","🥜": "Peanuts",
    "🌰": "Chestnut","🍞": "Bread","🥐": "Croissant","🥖": "Baguette Bread","🥨": "Pretzel","🥯": "Bagel","🥞": "Pancakes",
    "🧀": "Cheese Wedge","🍖": "Meat on Bone","🍗": "Poultry Leg","🥩": "Cut of Meat","🥓": "Bacon","🍔": "Hamburger","🍟": "French Fries",
    "🍕": "Pizza","🌭": "Hot Dog","🥪": "Sandwich","🍱": "Bento Box","🍲": "Pot of Food","🍛": "Curry Rice","🍜": "Steaming Bowl",
    "🍝": "Spaghetti","🍠": "Roasted Sweet Potato","🍢": "Oden","🍣": "Sushi","🍤": "Fried Shrimp","🍥": "Fish Cake with Swirl",
    "🍡": "Dango","🍦": "Soft Ice Cream","🍧": "Shaved Ice","🍨": "Ice Cream","🍩": "Doughnut","🍪": "Cookie","🎂": "Birthday Cake",
    "🍰": "Shortcake","🧁": "Cupcake","🥧": "Pie","🍫": "Chocolate Bar","🍬": "Candy","🍭": "Lollipop","🍮": "Custard","🍯": "Honey Pot",
    "🍼": "Baby Bottle","🥤": "Cup with Straw","🍺": "Beer Mug","🍻": "Clinking Beer Mugs","🥂": "Clinking Glasses","🥃": "Tumbler Glass","🍸": "Cocktail Glass",
    "🍹": "Tropical Drink","🍾": "Bottle with Popping Cork","🥄": "Spoon","🍽️": "Fork and Knife with Plate","🍴": "Fork and Knife",
    "☕": "Hot Beverage","🍵": "Teacup without Handle","🍶": "Sake","🥢": "Chopsticks","🥄": "Spoon","🔪": "Kitchen Knife",
    "🏺": "Amphora","🍽️": "Fork and Knife with Plate","🧊": "Ice Cube","🥤": "Cup with Straw","🥢": "Chopsticks","🍽️": "Fork and Knife with Plate",
    "🧂": "Salt","🥄": "Spoon","🍽️": "Fork and Knife with Plate","🧇": "Waffle","🧆": "Falafel","🥙": "Stuffed Flatbread","🌮": "Taco",
    "🌯": "Burrito","🍔": "Hamburger","🍟": "French Fries","🍕": "Pizza","🥪": "Sandwich","🍱": "Bento Box","🥗": "Green Salad",
    "🌞": "Sun","🌝": "Full Moon","🌚": "New Moon","🌛": "First Quarter Moon","🌜": "Last Quarter Moon","🌙": "Crescent Moon",
    "🌎": "Earth Globe Americas","🌍": "Earth Globe Europe-Africa","🌏": "Earth Globe Asia-Australia","🌧️": "Rain Cloud","⛈️": "Cloud with Lightning and Rain",
    "🌩️": "Cloud with Lightning","🌦️": "Sun Behind Rain Cloud","🌥️": "Sun Behind Large Cloud","🌤️": "Sun Behind Small Cloud",
    "❄️": "Snowflake","🌨️": "Cloud with Snow","☃️": "Snowman","🌬️": "Wind Face","💨": "Dashing Away","🌪️": "Tornado","🌫️": "Fog",
    "🌧️": "Rain Cloud","⛈️": "Cloud with Lightning and Rain","🌩️": "Cloud with Lightning","🌦️": "Sun Behind Rain Cloud","🌥️": "Sun Behind Large Cloud",
    "🌤️": "Sun Behind Small Cloud","🌫️": "Fog","❄️": "Snowflake","🌨️": "Cloud with Snow","☃️": "Snowman","🌬️": "Wind Face","💨": "Dashing Away",
    "🌪️": "Tornado","🌊": "Water Wave","🏄‍♂️": "Man Surfing","🏄‍♀️": "Woman Surfing","🏊‍♂️": "Man Swimming","🏊‍♀️": "Woman Swimming","🚣‍♂️": "Man Rowing Boat",
    "🚣‍♀️": "Woman Rowing Boat","🏆": "Trophy","🥇": "1st Place Medal","🥈": "2nd Place Medal","🥉": "3rd Place Medal","🏅": "Sports Medal",
    "🎖️": "Military Medal","🏵️": "Rosette","🎗️": "Reminder Ribbon","🎫": "Ticket","🎟️": "Admission Tickets","🎪": "Circus Tent",
    "🤹‍♀️": "Woman Juggling","🤹‍♂️": "Man Juggling","🎭": "Performing Arts","🎨": "Artist Palette","🎰": "Slot Machine","🎲": "Game Die",
    "🎯": "Direct Hit","🎳": "Bowling","🎮": "Video Game","🎰": "Slot Machine","🎲": "Game Die","🎳": "Bowling",
    "🥁": "Drum","🎷": "Saxophone","🎸": "Guitar","🎻": "Violin","🎺": "Trumpet","🎹": "Musical Keyboard","🎼": "Sheet Music",
    "🎧": "Headphone","🎤": "Microphone","🎬": "Clapper Board","🎥": "Movie Camera","📷": "Camera","📸": "Camera with Flash",
    "📽️": "Film Projector","📺": "Television","📻": "Radio","🎙️": "Studio Microphone","🎚️": "Level Slider","🎛️": "Control Knobs",
    "⏸️": "Pause Button","⏹️": "Stop Button","⏺️": "Record Button","📀": "DVD","💿": "Optical Disc","📼": "Videocassette",
    "🔊": "Loudspeaker","🔉": "Speaker Medium Volume","🔈": "Speaker Low Volume","🔇": "Muted Speaker","🔔": "Bell","🕭": "Bell with Slash",
    "📢": "Loudspeaker","📣": "Megaphone","🕯️": "Candle","💡": "Light Bulb","🔦": "Flashlight","🏮": "Red Paper Lantern","🪔": "Candle",
    "🧯": "Fire Extinguisher","🗑️": "Wastebasket","🧹": "Broom","🧺": "Basket","🧻": "Roll of Paper","🧼": "Soap","🧽": "Sponge",
    "🧴": "Lotion Bottle","🛁": "Bathtub","🚿": "Shower","🪒": "Razor","🧻": "Roll of Paper","🚽": "Toilet","🚪": "Door",
    "🪑": "Chair","🛋️": "Couch and Lamp","🪓": "Axe","🪔": "Diya Lamp","🪕": "Banjo","🪁": "Kite","🥎": "Softball","🥏": "Flying Disc",
    "🥍": "Lacrosse","🧿": "Nazar Amulet","🧩": "Puzzle Piece","🧸": "Teddy Bear","🧺": "Basket","💢":"Anger or Frustration",
    "💤":"Sleeping","💦":"Sweat droplets or spelling water","☮":"Peace","🕉":"Om","🕳":"Hole","🆚":"versus","♾":"Infinity",
    "⚛":"Atom","☢":"Radioactive","🚭":"No smoking","⚠":"Warning","♻":"Recycling","▶":"Play","⏸":"Pause","📈":"Increasing",
    "📉":"Decreasing","📕":"Red book","📒":"Yellow book","📗":"Green book","📊":"Bar chart","🐶":"Dog","🐱":"Cat","👀":"Eyes","🦊":"Fox","🦄":"Unicorn","🐔":"Chicken","🐲":"Dragon","🦓":"Zebra","🐨":"Koala",
    "🐼":"Panda","🐸":"Frog","🦝":"Raccoon","🐮":"Cow","🐷":"Pig","🐗":"Boar","🐭":"Mouse","🐹":"Hamster","🦒":"Giraffe",
    "🐟":"Fish","🦀":"Crab","🦠":"Microbe","🕷":"Spider","🕸":"Spider web","🦷":"Tooth","🦴":"Bone","🧠":"Brain","👣":"Footprints",
    "👅":"Tongue","👄":"Mouth","👸":"Princess","🤴":"Prince","👵":"Old woman","👼":"Baby angel","👮":"Female police officer","👮":"Male police officer",
    "🕵":"Detective","🕵":"Detective","👷":"Construction worker","👷🏻‍♀️":"Construction worker","👨🏻‍🏫":"Teacher","👰":"Bride",
    "🤰":"Preagnant","🛀":"Taking bath","🤝":"Handshake","👌🏻":"Perfect","🔑":"Key","🧬":"DNA","💊":"Pill","💣":"Bomb",
    "🔬":"Microscope","🖨":"Printer","💻":"Laptop","🔗":"Link","🚬":"Cigarette","🔋":"Battery","🔌":"Electric plug",
    "✂":"Scissiors","📌":"Pushpin","⌚":"Watch","⚰":"Coffin","📺":"TV"}
    
    d1 = {
    ":-)": "Smile",":-(": "Frown",":-D": "Big Grin",":-P": "Sticking Out Tongue",";-)": "Wink",":-|": "Indifferent",":-/": "Skeptical",
    ":-*": "Kiss",":-O": "Surprised",":-X": "Sealed Lips","<3": "Heart","^_^": "Happy","T_T": "Crying",":-]": "Happy",":-[": "Sad",
    ":-||": "Angry",":')": "Tears of Joy",":-B": "Nerd",":3": "Cute Face",":|]": "Robot",":-#": "Braces",":-&": "Sick",":-%": "Confused",":->": "Sarcastic",":-\\": "Shrug",
    ":')-<": "Crying with a Mustache",":-o)": "Clown","(^_^)": "Joyful","(-_-)": "Disapproval","(*_*)": "Amazement","(-.-)": "Sigh",
    "(@_@)": "Dazed","(/_\)": "Distressed","(\*_\*)": "Excited","(\^.^)": "Happy","(;_;)": "Tearful","(+_+)": "Agitated","(-.-;)": "Worried",
    "(o_o)": "Surprised","(>_>)": "Shifty Eyes","(-'_'-)": "Nervous","(*^_^*)": "Blushing","(^o^)": "Cheerful","(#^.^#)": "Pleased",
    "(;^_^)/": "Joy","(/o\\)": "Tension","(^_-)": "Wink","(T_T)/": "Bowing","(@.@)": "Staring","(~o~)": "Drooling","(-_-)zzz": "Sleeping",
    "(>_>)<": "Evil Grin","(*_*)>": "Hypnotized","d[-_-]b": "Listening to Music","(^0^)/": "Excited","(*_*;)": "Embarrassed","(o^^)o": "Applause",
    "(@_@;": "Dizzy","(^o^;)": "Sweating","(-_-)/": "Salute","(@o@)/": "Cheers",":-Oo": "Surprised","(^_-)b": "Thumbs Up","O_O": "Wide-Eyed",
    "(o_o)": "Staring","(=_=)": "Bored","(>_<)": "Angry","(o_0)": "Confused","(-.-')": "Annoyance","(-_-)ゞ": "Sigh","(^,^)": "Giggling",
    "(-_-メ)": "Dissatisfied","(^_~)": "Winking","(-_-)凸": "Flipping the Bird","(o_ _)o": "Apology","(°ロ°)": "Disapproval","(◠‿◠✿)": "Cuteness Overload","( ͡° ͜ʖ ͡°)": "Lenny Face",
    "( ͡ᵔ ͜ʖ ͡ᵔ )": "Lenny Face with Glasses","(ง •̀_•́)ง": "Ready to Fight","¯_(ツ)_/¯": "Shrugging","( •_•)>⌐■-■": "Deal With It",
    "ಠ_ಠ": "Disapproval or Disbelief","(¬‿¬)": "Smirking","(¬_¬)": "Sarcasm","(☞ﾟヮﾟ)☞": "Finger Guns","(つ◕_◕)つ": "Sending a Hug",
    "( ͡~ ͜ʖ ͡°)": "Lenny Face with a Wink","(ง'̀-'́)ง": "Getting Ready for a Challenge","(¬‿¬) ": "Flirting","¯_(⊙_ʖ⊙)_/¯": "Confused Lenny Face",
    "(´・ω・)っ": "Kawaii Face","(••) ( ••)>⌐■-■ (⌐■_■)": "Sunglasses Deal With It","(¬‿¬) ": "Smirking with Style","(つ•̀ω•́)つ*:･ﾟ✧": "Sending Positive Vibes"}
    
    d2 = {
    "😀": "Grinning","😃": "Grinning with Big Eyes","😄": "Grinning with Smiling Eyes","😁": "Beaming with Smiling Eyes",
    "😆": "Grinning Squinting","😅": "Grinning with Sweat","🤣": "Rolling on the Floor Laughing","😂": "Face with Tears of Joy",
    "😊": "Smiling with Smiling Eyes","😇": "Smiling with Halo","🙂": "Slightly Smiling","🙃": "Upside-Down","😉": "Winking",
    "😌": "Relieved","😍": "Heart Eyes","😎": "Smiling with Sunglasses","🤩": "Star-Struck","😏": "Smirking","😐": "Neutral",
    "😑": "Expressionless","😒": "Unamused","😕": "Confused","🙁": "Slightly Frowning","😮": "Open Mouth","😯": "Hushed","😲": "Astonished",
    "😳": "Flushed","😦": "Frowning with Open Mouth","😧": "Anguished","😨": "Fearful","😰": "Anxious with Sweat","😥": "Sad but Relieved",
    "😢": "Crying","😭": "Loudly Crying","😱": "Screaming in Fear","😖": "Confounded","😣": "Persevering","😞": "Disappointed",
    "😓": "Downcast with Sweat","😩": "Weary","😫": "Tired","😤": "with Steam From Nose","😡": "Pouting","😠": "Angry","🤬": "with Symbols on Mouth",
    "😈": "Smiling with Horns","👿": "Angry with Horns","💀": "Skull","☠️": "Skull and Crossbones","💩": "Pile of Poo","🤡": "Clown",
    "👹": "Ogre","👺": "Goblin","👻": "Ghost","👽": "Alien","👾": "Alien Monster","🤖": "Robot","💋": "Kiss Mark","❤️": "Red Heart",
    "💔": "Broken Heart","❣️": "Heart Exclamation","💕": "Two Hearts","💞": "Revolving Hearts","💓": "Beating Heart","💗": "Growing Heart",
    "💖": "Sparkling Heart","💘": "Heart with Arrow","💝": "Heart with Ribbon","💙": "Blue Heart","💚": "Green Heart","💛": "Yellow Heart",
    "🧡": "Orange Heart","💜": "Purple Heart","🖤": "Black Heart","🤍": "White Heart","💯": "Hundred Points","🔥": "Fire","🌟": "Glowing Star",
    "✨": "Sparkles","🌈": "Rainbow","⭐": "Star","🌞": "Sun with Face","🌝": "Full Moon with Face","🌚": "New Moon with Face","🌍": "Earth Globe Europe-Africa",
    "🌎": "Earth Globe Americas","🌏": "Earth Globe Asia-Australia","🌱": "Seedling","🌼": "Blossom","🍁": "Maple Leaf","🍂": "Fallen Leaf",
    "🍃": "Leaf Fluttering in Wind","🌸": "Cherry Blossom","🌺": "Hibiscus","🌻": "Sunflower","🌴": "Palm Tree","🌵": "Cactus","🌾": "Sheaf of Rice","🌿": "Herb",
    "🍀": "Four Leaf Clover","🍁": "Maple Leaf","🍂": "Fallen Leaf","🍃": "Leaf Fluttering in Wind","🍇": "Grapes","🍈": "Melon",
    "🍉": "Watermelon","🍊": "Tangerine","🍋": "Lemon","🍌": "Banana","🍍": "Pineapple","🍎": "Red Apple","🍏": "Green Apple",
    "🍐": "Pear","🍑": "Peach","🍒": "Cherries","🍓": "Strawberry","🥝": "Kiwi Fruit","🍅": "Tomato","🍆": "Eggplant","🥑": "Avocado",
    "🥒": "Cucumber","🥕": "Carrot","🌽": "Ear of Corn","🌶️": "Hot Pepper","🥦": "Broccoli","🍄": "Mushroom","🥜": "Peanuts",
    "🌰": "Chestnut","🍞": "Bread","🥐": "Croissant","🥖": "Baguette Bread","🥨": "Pretzel","🥯": "Bagel","🥞": "Pancakes",
    "🧀": "Cheese Wedge","🍖": "Meat on Bone","🍗": "Poultry Leg","🥩": "Cut of Meat","🥓": "Bacon","🍔": "Hamburger","🍟": "French Fries",
    "🍕": "Pizza","🌭": "Hot Dog","🥪": "Sandwich","🍱": "Bento Box","🍲": "Pot of Food","🍛": "Curry Rice","🍜": "Steaming Bowl",
    "🍝": "Spaghetti","🍠": "Roasted Sweet Potato","🍢": "Oden","🍣": "Sushi","🍤": "Fried Shrimp","🍥": "Fish Cake with Swirl",
    "🍡": "Dango","🍦": "Soft Ice Cream","🍧": "Shaved Ice","🍨": "Ice Cream","🍩": "Doughnut","🍪": "Cookie","🎂": "Birthday Cake",
    "🍰": "Shortcake","🧁": "Cupcake","🥧": "Pie","🍫": "Chocolate Bar","🍬": "Candy","🍭": "Lollipop","🍮": "Custard","🍯": "Honey Pot",
    "🍼": "Baby Bottle","🥤": "Cup with Straw","🍺": "Beer Mug","🍻": "Clinking Beer Mugs","🥂": "Clinking Glasses","🥃": "Tumbler Glass","🍸": "Cocktail Glass",
    "🍹": "Tropical Drink","🍾": "Bottle with Popping Cork","🥄": "Spoon","🍽️": "Fork and Knife with Plate","🍴": "Fork and Knife",
    "☕": "Hot Beverage","🍵": "Teacup without Handle","🍶": "Sake","🥢": "Chopsticks","🥄": "Spoon","🔪": "Kitchen Knife",
    "🏺": "Amphora","🍽️": "Fork and Knife with Plate","🧊": "Ice Cube","🥤": "Cup with Straw","🥢": "Chopsticks","🍽️": "Fork and Knife with Plate",
    "🧂": "Salt","🥄": "Spoon","🍽️": "Fork and Knife with Plate","🧇": "Waffle","🧆": "Falafel","🥙": "Stuffed Flatbread","🌮": "Taco",
    "🌯": "Burrito","🍔": "Hamburger","🍟": "French Fries","🍕": "Pizza","🥪": "Sandwich","🍱": "Bento Box","🥗": "Green Salad",
    "🌞": "Sun","🌝": "Full Moon","🌚": "New Moon","🌛": "First Quarter Moon","🌜": "Last Quarter Moon","🌙": "Crescent Moon",
    "🌎": "Earth Globe Americas","🌍": "Earth Globe Europe-Africa","🌏": "Earth Globe Asia-Australia","🌧️": "Rain Cloud","⛈️": "Cloud with Lightning and Rain",
    "🌩️": "Cloud with Lightning","🌦️": "Sun Behind Rain Cloud","🌥️": "Sun Behind Large Cloud","🌤️": "Sun Behind Small Cloud",
    "❄️": "Snowflake","🌨️": "Cloud with Snow","☃️": "Snowman","🌬️": "Wind Face","💨": "Dashing Away","🌪️": "Tornado","🌫️": "Fog",
    "🌧️": "Rain Cloud","⛈️": "Cloud with Lightning and Rain","🌩️": "Cloud with Lightning","🌦️": "Sun Behind Rain Cloud","🌥️": "Sun Behind Large Cloud",
    "🌤️": "Sun Behind Small Cloud","🌫️": "Fog","❄️": "Snowflake","🌨️": "Cloud with Snow","☃️": "Snowman","🌬️": "Wind Face","💨": "Dashing Away",
    "🌪️": "Tornado","🌊": "Water Wave","🏄‍♂️": "Man Surfing","🏄‍♀️": "Woman Surfing","🏊‍♂️": "Man Swimming","🏊‍♀️": "Woman Swimming","🚣‍♂️": "Man Rowing Boat",
    "🚣‍♀️": "Woman Rowing Boat","🏆": "Trophy","🥇": "1st Place Medal","🥈": "2nd Place Medal","🥉": "3rd Place Medal","🏅": "Sports Medal",
    "🎖️": "Military Medal","🏵️": "Rosette","🎗️": "Reminder Ribbon","🎫": "Ticket","🎟️": "Admission Tickets","🎪": "Circus Tent",
    "🤹‍♀️": "Woman Juggling","🤹‍♂️": "Man Juggling","🎭": "Performing Arts","🎨": "Artist Palette","🎰": "Slot Machine","🎲": "Game Die",
    "🎯": "Direct Hit","🎳": "Bowling","🎮": "Video Game","🎰": "Slot Machine","🎲": "Game Die","🎳": "Bowling",
    "🥁": "Drum","🎷": "Saxophone","🎸": "Guitar","🎻": "Violin","🎺": "Trumpet","🎹": "Musical Keyboard","🎼": "Sheet Music",
    "🎧": "Headphone","🎤": "Microphone","🎬": "Clapper Board","🎥": "Movie Camera","📷": "Camera","📸": "Camera with Flash",
    "📽️": "Film Projector","📺": "Television","📻": "Radio","🎙️": "Studio Microphone","🎚️": "Level Slider","🎛️": "Control Knobs",
    "⏸️": "Pause Button","⏹️": "Stop Button","⏺️": "Record Button","📀": "DVD","💿": "Optical Disc","📼": "Videocassette",
    "🔊": "Loudspeaker","🔉": "Speaker Medium Volume","🔈": "Speaker Low Volume","🔇": "Muted Speaker","🔔": "Bell","🕭": "Bell with Slash",
    "📢": "Loudspeaker","📣": "Megaphone","🕯️": "Candle","💡": "Light Bulb","🔦": "Flashlight","🏮": "Red Paper Lantern","🪔": "Candle",
    "🧯": "Fire Extinguisher","🗑️": "Wastebasket","🧹": "Broom","🧺": "Basket","🧻": "Roll of Paper","🧼": "Soap","🧽": "Sponge",
    "🧴": "Lotion Bottle","🛁": "Bathtub","🚿": "Shower","🪒": "Razor","🧻": "Roll of Paper","🚽": "Toilet","🚪": "Door",
    "🪑": "Chair","🛋️": "Couch and Lamp","🪓": "Axe","🪔": "Diya Lamp","🪕": "Banjo","🪁": "Kite","🥎": "Softball","🥏": "Flying Disc",
    "🥍": "Lacrosse","🧿": "Nazar Amulet","🧩": "Puzzle Piece","🧸": "Teddy Bear","🧺": "Basket","💢":"Anger or Frustration",
    "💤":"Sleeping","💦":"Sweat droplets or spelling water","☮":"Peace","🕉":"Om","🕳":"Hole","🆚":"versus","♾":"Infinity",
    "⚛":"Atom","☢":"Radioactive","🚭":"No smoking","⚠":"Warning","♻":"Recycling","▶":"Play","⏸":"Pause","📈":"Increasing",
    "📉":"Decreasing","📕":"Red book","📒":"Yellow book","📗":"Green book","📊":"Bar chart","🐶":"Dog","🐱":"Cat","👀":"Eyes","🦊":"Fox","🦄":"Unicorn","🐔":"Chicken","🐲":"Dragon","🦓":"Zebra","🐨":"Koala",
    "🐼":"Panda","🐸":"Frog","🦝":"Raccoon","🐮":"Cow","🐷":"Pig","🐗":"Boar","🐭":"Mouse","🐹":"Hamster","🦒":"Giraffe",
    "🐟":"Fish","🦀":"Crab","🦠":"Microbe","🕷":"Spider","🕸":"Spider web","🦷":"Tooth","🦴":"Bone","🧠":"Brain","👣":"Footprints",
    "👅":"Tongue","👄":"Mouth","👸":"Princess","🤴":"Prince","👵":"Old woman","👼":"Baby angel","👮":"Female police officer","👮":"Male police officer",
    "🕵":"Detective","🕵":"Detective","👷":"Construction worker","👷🏻‍♀️":"Construction worker","👨🏻‍🏫":"Teacher","👰":"Bride",
    "🤰":"Preagnant","🛀":"Taking bath","🤝":"Handshake","👌🏻":"Perfect","🔑":"Key","🧬":"DNA","💊":"Pill","💣":"Bomb",
    "🔬":"Microscope","🖨":"Printer","💻":"Laptop","🔗":"Link","🚬":"Cigarette","🔋":"Battery","🔌":"Electric plug",
    "✂":"Scissiors","📌":"Pushpin","⌚":"Watch","⚰":"Coffin","📺":"TV",
    ":-)": "Smile",":-(": "Frown",":-D": "Big Grin",":-P": "Sticking Out Tongue",";-)": "Wink",":-|": "Indifferent",":-/": "Skeptical",
    ":-*": "Kiss",":-O": "Surprised",":-X": "Sealed Lips","<3": "Heart","^_^": "Happy","T_T": "Crying",":-]": "Happy",":-[": "Sad",
    ":-||": "Angry",":')": "Tears of Joy",":-B": "Nerd",":3": "Cute Face",":|]": "Robot",":-#": "Braces",":-&": "Sick",":-%": "Confused",":->": "Sarcastic",":-\\": "Shrug",
    ":')-<": "Crying with a Mustache",":-o)": "Clown","(^_^)": "Joyful","(-_-)": "Disapproval","(*_*)": "Amazement","(-.-)": "Sigh",
    "(@_@)": "Dazed","(/_\)": "Distressed","(\*_\*)": "Excited","(\^.^)": "Happy","(;_;)": "Tearful","(+_+)": "Agitated","(-.-;)": "Worried",
    "(o_o)": "Surprised","(>_>)": "Shifty Eyes","(-'_'-)": "Nervous","(*^_^*)": "Blushing","(^o^)": "Cheerful","(#^.^#)": "Pleased",
    "(;^_^)/": "Joy","(/o\\)": "Tension","(^_-)": "Wink","(T_T)/": "Bowing","(@.@)": "Staring","(~o~)": "Drooling","(-_-)zzz": "Sleeping",
    "(>_>)<": "Evil Grin","(*_*)>": "Hypnotized","d[-_-]b": "Listening to Music","(^0^)/": "Excited","(*_*;)": "Embarrassed","(o^^)o": "Applause",
    "(@_@;": "Dizzy","(^o^;)": "Sweating","(-_-)/": "Salute","(@o@)/": "Cheers",":-Oo": "Surprised","(^_-)b": "Thumbs Up","O_O": "Wide-Eyed",
    "(o_o)": "Staring","(=_=)": "Bored","(>_<)": "Angry","(o_0)": "Confused","(-.-')": "Annoyance","(-_-)ゞ": "Sigh","(^,^)": "Giggling",
    "(-_-メ)": "Dissatisfied","(^_~)": "Winking","(-_-)凸": "Flipping the Bird","(o_ _)o": "Apology","(°ロ°)": "Disapproval","(◠‿◠✿)": "Cuteness Overload","( ͡° ͜ʖ ͡°)": "Lenny Face",
    "( ͡ᵔ ͜ʖ ͡ᵔ )": "Lenny Face with Glasses","(ง •̀_•́)ง": "Ready to Fight","¯_(ツ)_/¯": "Shrugging","( •_•)>⌐■-■": "Deal With It",
    "ಠ_ಠ": "Disapproval or Disbelief","(¬‿¬)": "Smirking","(¬_¬)": "Sarcasm","(☞ﾟヮﾟ)☞": "Finger Guns","(つ◕_◕)つ": "Sending a Hug",
    "( ͡~ ͜ʖ ͡°)": "Lenny Face with a Wink","(ง'̀-'́)ง": "Getting Ready for a Challenge","(¬‿¬) ": "Flirting","¯_(⊙_ʖ⊙)_/¯": "Confused Lenny Face",
    "(´・ω・)っ": "Kawaii Face","(••) ( ••)>⌐■-■ (⌐■_■)": "Sunglasses Deal With It","(¬‿¬) ": "Smirking with Style","(つ•̀ω•́)つ*:･ﾟ✧": "Sending Positive Vibes"}

    import numpy as np
    import pandas as pd
    import string
    
    tt=[]
    
    if remove_all == 'emj' or remove_all =='emoji':
        d.clear()
        #d1.clear()
        #d2.clear()
        print('All predefine emojies has been removed')
    elif remove_all == 'emt' or remove_all=='emoticon':
        d1.clear()
        print('All predefine emoticons has been removed')
    elif remove_all == 'both':
        d.clear()
        d1.clear()
        d2.clear()
        print('All predefine emojies and emoticons has been removed')
    elif remove_all not in('emj','emoji','emt','emoticon','both',None):
        raise ValueError("'remove_all' parameter can be set to either 'emj' or 'emoji', 'emt' or 'emoticon', or 'both'.")
        
    if add =='emj' or add == 'emoji' and add_em != None:
        d.update(add_em)
        d2.update(add_em)
    elif add =='emt' or add =='emoticon' and add_em != None:
        d1.update(add_em)
        d2.update(add_em)
    elif add =='emj' or add=='emoji' or add=='emt' or add=='emoticon' and add_em == None:
        raise ValueError("didn't find and dict to add")
    elif add not in(None,'emj','emt','emoji','emoticon'):
        raise ValueError("add value must be ether 'emj' or 'emt' | can be passed full form of 'emj' or 'emt'")
        
    if remove_em != None and remove == 'emj' or remove =='emoji':
        for i in remove_em:
            d.pop(i)
            d2.pop(i)
    elif remove_em != None and remove == 'emt' or remove =='emoticon':
        for i1 in remove_em:
            d1.pop(i1)
            d2.pop(i1)
    elif remove_em != None and remove == 'both':
        for i2 in remove_em:
            d2.pop(i2)
    elif remove not in(None,'emj','emt','emoji','emoticon','both'):
        raise ValueError("remove value must be ether 'emj' or 'emt' or 'both'")
            
    text1=text
    for chr1 in d2:
        text1=text1.replace(chr1,' ' + chr1 + ' ')
    for t in text1.split():
        tt.append(t)
        
    if remove_from_list == None:
        
        if process_type == 'remove' and process_on == 'both':
            text1=' '.join([word for word in tt if word not in d2])
            if case == 'same':
                return text1
            elif case == 'lower':
                return text1.lower()
            elif case == 'upper':
                return text1.upper()
            else:
                raise ValueError("case value can be 'same','lower' or 'upper'")

        elif process_type == 'remove' and process_on == 'emj':
            text1=' '.join([word1 for word1 in tt if word1 not in d])
            if case == 'same':
                return text1
            elif case == 'lower':
                return text1.lower()
            elif case == 'upper':
                return text1.upper()
            else:
                raise ValueError("case value can be 'same','lower' or 'upper'")

        elif process_type == 'remove' and process_on == 'emt':
            text1=' '.join([word2 for word2 in tt if word2 not in d1])
            if case == 'same':
                return text1
            elif case == 'lower':
                return text1.lower()
            elif case == 'upper':
                return text1.upper()
            else:
                raise ValueError("case value can be 'same','lower' or 'upper'")

        elif process_type == 'replace' and process_on == 'both':
            for ii in tt:
                if ii in d2:
                    tt[tt.index(ii)]=d2[ii]
            text1=' '.join([w for w in tt])
            if case == 'same':
                return text1
            elif case == 'lower':
                return text1.lower()
            elif case == 'upper':
                return text1.upper()
            else:
                raise ValueError("case value can be 'same','lower' or 'upper'")

        elif process_type == 'replace' and process_on =='emj' or process_on =='emoji':
            for ii1 in tt:
                if ii1 in d:
                    tt[tt.index(ii1)]=d[ii1]
            text1=' '.join([w1 for w1 in tt])
            if case == 'same':
                return text1
            elif case == 'lower':
                return text1.lower()
            elif case == 'upper':
                return text1.upper()
            else:
                raise ValueError("case value can be 'same','lower' or 'upper'")

        elif process_type == 'replace' and process_on =='emt' or process_on =='emoticon':
            for ii2 in tt:
                if ii2 in d1:
                    tt[tt.index(ii2)]=d1[ii2]
            text1=' '.join([w2 for w2 in tt])
            if case == 'same':
                return text1
            elif case == 'lower':
                return text1.lower()
            elif case == 'upper':
                return text1.upper()
            else:
                raise ValueError("case value can be 'same','lower' or 'upper'")
                
    elif remove_from_list != None:
        if process_type == 'remove' and process_on == 'both':
            text1=' '.join([word for word in tt if word not in d2])
            for chr2 in remove_from_list:
                text1=text1.replace(chr2, ' ' + chr2 + ' ')
            text1=' '.join([em for em in text1.split() if em not in remove_from_list])
            if case == 'same':
                return text1
            elif case == 'lower':
                return text1.lower()
            elif case == 'upper':
                return text1.upper()
            else:
                raise ValueError("case value can be 'same','lower' or 'upper'")
        

def word_tokenizer(text,output_case='same',del_words=None,punc_tokenize=True,include_slash=True,smart_recognition=True,sp_character_tokens=False):

    """
    Tokenizes input text based on specified parameters and returns a list of tokens.

    This function provides a flexible tokenization process, allowing for customization
    in terms of case handling, punctuation inclusion, special character recognition,
    and more. It can handle URLs and email addresses appropriately, preserving their
    integrity during tokenization.

    Parameters:
    -----------
    ** text : str
           The input text to be tokenized.

    ** output_case : str, optional
          Specifies the case format for the output tokens. Options include:
          - 'same' (default): Tokens are returned as they are in the input text.
          - 'lower': Tokens are converted to lowercase.
          - 'upper': Tokens are converted to uppercase.

    ** del_words : (list,tuple,set), optional
          A list of words to be excluded from the tokenization process. If None, no words
          are excluded. Default is None.

    ** punc_tokenize : bool, optional
          Determines whether to include punctuation in the tokens. If True, punctuation
          marks are treated as separate tokens. If False, punctuation marks are ignored.
          Default is True.

    ** include_slash : bool, optional
          Specifies whether to include slashes (both forward '/' and backward '\\') as tokens.
          If True, slashes are included. If False, slashes are excluded from the tokens.
          Default is True.

    ** smart_recognition : bool, optional
          If True, applies a more sophisticated tokenization that recognizes certain patterns
          such as contractions, possessives, and special cases. Default is True.

    ** sp_character_tokens : bool, optional
          If True, treats special characters (e.g., emojis, symbols) as separate tokens.
          Default is False.

    Returns:
    --------
    list
        A list of tokens based on the specified parameters.


    ## Examples:
    ------------
    Basic Usage:
    ------------
    >>> text = "This is a sample sentence."
    >>> del_words = ['is', 'a']
    >>> word_tokenizer(text, output_case='lower', del_words=del_words)
    ['this', 'sample', 'sentence']

    Handling Punctuation:
    ---------------------
    >>> text = "Complex-tokenization example, with punctuation!"
    >>> word_tokenizer(text, punc_tokenize=False)
    ['Complex-tokenization', 'example', 'with', 'punctuation']

    Recognizing URLs:
    -----------------
    >>> text = "Visit our website at https://www.example.com."
    >>> word_tokenizer(text)
    ['Visit', 'our', 'website', 'at', 'https',':','//www.example.com', '.']

    Recognizing Email Addresses:
    ----------------------------
    >>> text = "Please contact us at example@gmail.com."
    >>> word_tokenizer(text)
    ['Please', 'contact', 'us', 'at', 'example','@','gmail.com', '.']

    Including Special Characters:
    -----------------------------
    >>> text = "Hello world! 😊"
    >>> word_tokenizer(text, sp_character_tokens=True)
    ['Hello', 'world', '!', '😊']

    Excluding Slashes:
    ------------------
    >>> text = "Use backslash \\ or forward slash /."
    >>> word_tokenizer(text, include_slash=False)
    ['Use', 'backslash', 'or', 'forward', 'slash', '.']
    """

    slash =["/","\\"]
    pun=["!","'",'"',"#","$","%","&","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","|","~","\\"]

    def token_02(text1):
      pun=["!","'s",'"',"#","$","%","&","(",")","*","+",",",":",";","<",">","?","@","[","]","`","{","}","|","n't","'d","'m","'S","'D","'M"] #
      pun_1=["."]
      pun_2=["'d","'m","'S","'D","'M","'s","'t","0",
           "1","2","3","4","5","6","7","8","9"]
      #alpha=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
      text=text1

      for char in pun:
        text=text.replace(char, ' ' + char + ' ')

      tok=[]
      for word in text.split():
        tok.append(word)         # 1st token
      #print(tok)

      ind=[]
      tok1=[]
      for i in tok:
        if len(i) > 1 and i[-1] in pun_1:
          ind.append(tok.index(i))
          i=i.replace(".","")
          tok1.append(i)          # 2nd token
        else:                     # do
          tok1.append(i)
      ex=1
      for ii in ind:
        tok1.insert(ii+ex,".")
        ex+=1
      #print(tok1)

      add_str="~~~"
      add_str1="~~~~"
      add_str2="~~~~~"
      add_str3="~~~~~~"
      add_str4="~~~~~~~"
      add_str5="~~~~~~~~"
      tok2=[]
      for i2 in tok1:
        if i2 == "'s" :
          i2=add_str
          tok2.append(i2)
        elif i2 == "'d":
          i2= add_str1
          tok2.append(i2)
        elif i2 == "'m":
          i2=add_str2
          tok2.append(i2)
        elif i2 == "'S":
          i2= add_str3
          tok2.append(i2)
        elif i2 == "'D":
          i2= add_str4
          tok2.append(i2)
        elif i2 == "M":
          i2= add_str5
          tok2.append(i2)         # 3rd token
        else:                     # do
          tok2.append(i2)

      tok3=[]
      ind1=[]
      ind2=[]
      ind3=[]
      ind4=[]
      for i3 in tok2:
        if i3[0] == "'": # or i3[-1] == "'":
          ind1.append(i3)
        if i3[-1] == "'":
          ind2.append(i3)
        if len(i3) > 1 and i3[-2] == "'" and i3[-2::] not in pun_2:
          ind3.append(i3)
      #print(ind1)
      #print(ind2)
      #print(ind3)
      ex1=0
      for ii1 in ind1:
        tok2.insert(tok2.index(ii1)+ex1,"'")
      ex2=1
      for ii2 in ind2:
        tok2.insert(tok2.index(ii2)+ex2,"'")
      #print(tok2)
      ex3=1
      for ii3 in ind3:
        tok2.insert(tok2.index(ii3)+ex3,"'")
      ex4=2
      for ii4 in ind3:
        tok2.insert(tok2.index(ii4)+ex4,ii4[-1])
      #print(tok2)

      for i7 in tok2:                                                                           ###
        if len(i7) > 2 and i7[-3] == "'" and i7[-1] == "'" and i7[-3::] not in pun_2:           ###
          ind4.append(i7)                                                                       ###
      ex5=1                                                                                     ###
      for ii5 in ind4:                                                                          ###
        tok2.insert(tok2.index(ii5)+ex5,"'")                                                     ###
      #print(tok2)                                                                              ###
      ex6=2                                                                                     ###
      for ii6 in ind4:                                                                          ###
        tok2.insert(tok2.index(ii6)+ex6,ii6[-2])                                                  ###
      #print(tok2)                                                                              ###
      #print(tok2)


      tok5=[]
      #for i8 in tok2:
        #if len(i8) >2 and "'" in i8 and i8[-1] == "'" and i8[-3] == "'" :
          #i8 = i8.replace(i8[-3:-1],'')
          #tok5.append(i8)
        #elif len(i8) > 1 and "'" in i8 and i8[-1] != "'" and i8[-2] == "'":
          #i8 = i8.replace(i8[-2::],'')
          #tok5.append(i8)
        #elif len(i8) >= 3 and "'" in i8 and "'" not in i8[-3::]:
          #if i8[0] == "'":
            #i8=i8.replace("'",'/')
            #tok5.append(i8)
        #else:
          #tok5.append(i8)
      #print(tok5)
      for i8 in tok2:
        if len(i8) >=3 and i8[0] == "'":
          tok5.append(i8[1::])
        elif len(i8) >= 3 and i8[-1] == "'":
          tok5.append(i8[0:-1])
        else:
          tok5.append(i8)
      #print(tok5)



      for i4 in tok5:
        if len(i4) > 3 and i4[-2] == "'": #i4[-1] == "'":
          #i4=i4.replace("'","")
          tok3.append(i4[0:-2])                    # 4 th token
        #elif len(i4) >1 and i4[-1] == "'" :
          #i4=i4.replace("'","")
          #tok3.append(i4)                    # 4 th Token
        elif i4 == "~~~":
          i4=i4.replace("~~~","'s")
          tok3.append(i4)
        elif i4 == "~~~~":
          i4=i4.replace("~~~~","'d")
          tok3.append(i4)
        elif i4 == "~~~~~":
          i4=i4.replace("~~~~~","'m")
          tok3.append(i4)
        elif i4 == "~~~~~~":
          i4 = i4.replace("~~~~~~","'S")
          tok3.append(i4)  # do
        elif i4 == "~~~~~~~":
          i4 = i4.replace("~~~~~~~","'D")
          tok3.append(i4)
        elif i4 == "~~~~~~~~":
          i4 = i4.replace("~~~~~~~~","M")
          tok3.append(i4)
        else:
          tok3.append(i4)                    # do   main return
      #print(tok3)

      return tok3     # Sub function

    if smart_recognition == False:

      if include_slash == False:
          for s in slash:
              pun.remove(s)
      elif include_slash not in(True, False):
          raise ValueError("include_slash value must be ether True or False")

      if punc_tokenize == True:
          for char in pun:
              text=text.replace(char, ' ' + char + ' ')
      elif punc_tokenize not in(True,False):
          raise ValueError("'Punc_tokenize' value must be a boolean object.")

      token=[]
      token1=[]
      token2=[]
      text1=text
      new_tok=[]
      new_tok1=[]
      new_tok2=[]
      for i in text.split():
          token.append(i)

      if del_words != None:
          for i2 in token:
              if i2 not in del_words:
                  new_tok.append(i2)
          if output_case == 'same':
              return new_tok
          elif output_case == 'lower':
              for i3 in new_tok:
                  new_tok1.append(i3.lower())
              return new_tok1
          elif output_case == 'upper':
              for i4 in new_tok:
                  new_tok2.append(i4.upper())
              return new_tok2
          elif output_case not in('same','upper','lower'):
              raise ValueError("output value can be ether 'same','lower' or 'upper'")

      elif del_words == None:
          if output_case == 'same':
              return token
          elif output_case == 'lower':
              for p in token:
                  token1.append(p.lower())
              return token1
          elif output_case == 'upper':
              for p1 in token:
                  token2.append(p1.upper())
              return token2
          elif output_case not in('same','upper','lower'):
              raise ValueError("output value can be ether 'same','lower' or 'upper'")

      elif del_words != None or type(del_words) != list:
          raise TypeError("del_word value must be a list object")

    elif smart_recognition == True:
      token_002=token_02(text)
      smart_token=[]
      if output_case == 'same':
        for s in token_002:
          smart_token.append(s)
      elif output_case == 'lower':
        for l in token_002:
          smart_token.append(l.lower())
      elif output_case == 'upper':
        for u in token_002:
          smart_token.append(u.upper())
      elif output_case not in('same','upper','lower'):
          raise ValueError("output value can be ether 'same','lower' or 'upper'")

      #if del_words != None:  # del_words
        #for w in smart_token:
          #if w not in del_words:
            #smart_token.remove(w)
      #elif del_words != None and type(del_words) not in(list,tuple,set):
          #raise TypeError("del_word value must be a list,tuple or set object")
      #print(smart_token)

      smart_token1=[]
      sp_ch=[]
      output=0
      if sp_character_tokens == True:
        Text69= ' '.join([w1 for w1 in smart_token])
        pun11=["!","'",'"',"#","$","%","&","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","|","~","\\"]
        alpha11=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        for T69 in Text69:
          if T69 not in pun11 and T69 not in alpha11:
            sp_ch.append(T69)
        if len(sp_ch) > 0:
          for sp in sp_ch:
            Text69=Text69.replace(sp, ' ' + sp + ' ')
          for w in Text69.split():
            smart_token1.append(w)
          if del_words == None:      # del words
            return smart_token1
          elif del_words != None and type(del_words) in(list,tuple,set):
            Smart_token2=[]
            for w2 in smart_token1:
              if w2 not in del_words:
                Smart_token2.append(w2)
            return Smart_token2
          elif del_words != None and type(del_words) not in(list,tuple,set):
            raise TypeError("del_word value must be a list,tuple or set object")

          #return smart_token1
        else:
          if del_words == None:
            return smart_token
          elif del_words != None and type(del_words) in(list,tuple,set):
            Smart_token1=[]
            for w3 in smart_token:
              if w3 not in del_words:
                Smart_token1.append(w3)
            return Smart_token1
            #return smart_token
          elif del_words != None and type(del_words) not in(list,tuple,set):
            raise TypeError("del_word value must be a list,tuple or set object")
          #return smart_token
          #return smart_token

      elif sp_character_tokens == False:
        Smart_token=[]
        if del_words != None and type(del_words) in(list,tuple,set):
          for w4 in smart_token:
            if w4 not in del_words:
              Smart_token.append(w4)
          return Smart_token
        elif del_words == None:
          return smart_token
        elif del_words != None and type(del_words) not in(list,tuple,set):
          raise TypeError("del_word value must be a list,tuple or set object")
        #return smart_token

      elif sp_character_tokens not in(True,False):
          raise ValueError("'emoji_tokens' value must be a boolean object.")

    elif type(smart_recognition) != bool:
        raise TypeError("smart_recognition value must be a boolean object.")
    

Punctuations =["!","'",'"',"#","$","%","&","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","|","~","\\"]

EnglishPronouns = ['he','she','i','me','we','us','him','her','it','they','them','you','He','She','I','Me','We','Us','Him','Her','It','They','Them','You']

def read_txt(path,first_line_only=False,case='same'):
    """
    Reads a text file and processes its content based on specified parameters.

    Parameters:
    * path (str): The path to the text file.
    * first_line_only (bool, optional): If True, reads only the first line of the file. Defaults to False.
    * case (str, optional): Specifies the case of the output text. 
        - 'same' (default): Returns text as it is.
        - 'lower': Returns text in lowercase.
        - 'upper': Returns text in uppercase. Default is 'same'

    Returns:
    - list or str: Processed text content based on the specified case parameter.
    
    
    Example:
    ```
    # Read entire file content in lowercase
    content = read_txt('path/to/file.txt', case='lower')

    # Read only the first line in uppercase
    first_line = read_txt('path/to/file.txt', first_line_only=True, case='upper')
    ```
    """
    
    p_file=0
    lines=0
    fresh_lines=[]
    c1=[]
    
    if path[-3::] == 'txt':
        p_file=open(path,'r')
        if first_line_only == False:
            lines=p_file.readlines()
        elif first_line_only == True:
            lines=p_file.readline()
            lines=lines.replace('\n','')
            
        elif first_line_only not in(True,False):
            raise ValueError("The value of the 'first_line_only' parameter must be either True or False.")
        if type(lines) == list:    
            for sent in lines:
                fresh_lines.append(sent.replace('\n',''))
                
        elif type(lines) == str:
            fresh_lines.append(lines.replace('\n',''))
            
        if case == 'same':
            return fresh_lines
        elif case == 'lower':
            for f in fresh_lines:
                c1.append(f.lower())
            return c1
        elif case == 'upper':
            for f1 in fresh_lines:
                c1.append(f1.upper())
            return c1
        elif case not in('same','upper','lower'):
            raise ValueError("The value of the 'case' must be among ['same','upper','lower'] ")
            
    else:
        raise ValueError("The file must be a text file having '.txt' extesion")


def text_to_tokens(data,fit_on_new_data=False,word_index_dict=None,apply_on='words',add_vocabulary=None,oob_token=None,smart_recognition=True,sp_character_tokens=False,output_token_case='same',token_type='advance',del_words_or_ch=None):

    """
    Convert text data into numerical tokens based on specified tokenization criteria.

    This function processes textual data and converts it into numerical tokens using flexible tokenization options. It supports word-based or character-based tokenization, the inclusion of additional vocabularies, and advanced tokenization features.

    Parameters
    ----------
    * data : list, tuple, set, or pandas.core.series.Series
         The input text data to be tokenized. Each element should be a string.

    * fit_on_new_data : bool, optional, default False
         Indicates whether to fit the tokenization model on new data using a custom `word_index_dict`. If set to `True`, the function will use `word_index_dict` to map words or characters to tokens. If `False`, the function will use an internally generated token dictionary based on the input data provided. This option is useful when you want to update or change the tokenization mapping based on new or additional data.

    * word_index_dict : dict, optional, default None
         A dictionary mapping words or characters to their corresponding tokens. This parameter is required if `fit_on_new_data` is `True`. The dictionary should provide a mapping where keys are words or characters and values are their corresponding integer tokens. This allows for the reuse of a predefined tokenization scheme or the integration of new data into an existing tokenization model. When provided, the function will use this dictionary to convert text data into tokens, ensuring consistency with previously defined token mappings.

    * apply_on : str, optional, default 'words'
         The criteria for tokenization. Options include:
         - 'words' or 'word': Tokenize based on words.
         - 'alpha', 'alphabet', or 'alphabets': Tokenize based on individual characters.

    * add_vocabulary : list, set, tuple, or dict, optional, default None
         An additional vocabulary to incorporate into the tokenization process. If provided, the function will ensure tokens are created based on this expanded vocabulary.

    * oob_token : str, optional, default None
         A token used for out-of-bound words not found in the existing vocabulary. If specified, this token will be assigned to such words.

    * smart_recognition : bool, optional, default True
         Enables advanced recognition features for improved tokenization accuracy. When enabled, the function:
         - Separates common punctuation from words.
         - Handles contractions effectively (e.g., "don't" -> "do" "n't").
         - Recognizes and tokenizes numbers, dates, and other numerical data.
         - Differentiates between acronyms, abbreviations, and standard words.

    * sp_character_tokens : bool, optional, default False
         If True, special characters are treated as distinct tokens. This can be useful for tasks where the presence and position of special characters are significant.

    * output_token_case : str, optional, default 'same'
         Specifies the case of the output tokens. Options include:
         - 'same': Retain the same case as the input.
         - 'lower': Convert all tokens to lowercase.
         - 'upper': Convert all tokens to uppercase.

    * token_type : str, optional, default 'advance'
         Determines the type of tokenization applied. Options include:
         - 'advance': Utilizes advanced tokenization with smart recognition features.
         - 'basic': Performs basic tokenization without advanced recognition.

    * del_words_or_ch : list, set, tuple, or None, optional, default None
        A list of words or characters to be excluded from the tokenization process. If specified, these elements will be removed before tokenization.

    Returns
    -------
    list
        A list of lists containing the tokenized representations of the input text data.

    dict
        A dictionary mapping each word/character to its corresponding token.

    Notes
    -----
    - For word-based tokenization, punctuation is managed by separating punctuation marks from words and assigning them distinct tokens.
    - Providing `add_vocabulary` extends the vocabulary with any new words encountered in the input text, ensuring comprehensive tokenization.
    - If `oob_token` is supplied, it will be used for words not found in the vocabulary, preventing potential issues with missing tokens.
    - The function ensures that each unique word or character is assigned a distinct token, preserving the integrity of the text’s meaning.
    - It is robust and adaptable to various text data formats, making it suitable for a wide range of natural language processing (NLP) tasks.
    - The function includes mechanisms for handling common issues such as unsupported data types and ensures compatibility with text processing libraries (e.g., pandas).

    About
    -----
    The `text_to_tokens` function is designed to transform textual data into a numerical format suitable for machine learning models and computational analysis. It offers extensive flexibility in tokenization, allowing users to choose between word-based and character-based approaches, incorporate additional vocabularies, and apply advanced tokenization techniques.

    The function’s advanced features, including smart recognition and special character handling, enhance the accuracy and utility of the tokenization process. By separating punctuation, handling contractions, and recognizing numerical data, it maintains the textual context and meaning, making it an effective tool for preprocessing text in various NLP applications.

    Example
    -------
    >>> data = ['This is an example sentence.', 'Another sentence for testing.']
    >>> tokens, token_dict = text_to_tokens(data)
    >>> print(tokens)
    [[1, 2, 3, 4, 5], [6, 5, 7, 8]]
    >>> print(token_dict)
    {'This': 1, 'is': 2, 'an': 3, 'example': 4, 'sentence': 5, 'Another': 6, 'for': 7, 'testing': 8}
    """
    
    import re

    d2={' ':0, 'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':10, 'K':11, 'L':12, 'M':13, 'N':14, 'O':15, 'P':16, 'Q':17, 'R':18,
       'S':19, 'T':20, 'U':21, 'V':22, 'W':23, 'X':24, 'Y':25, 'Z':26, 'a':27, 'b':28, 'c':29, 'd':30, 'e':31, 'f':32, 'g':33, 'h':34,'i':35, 'j':36,
       'k':37, 'l':38, 'm':39, 'n':40, 'o':41, 'p':42,'q':43, 'r':44, 's':45, 't':46, 'u':47, 'v':48, 'w':49, 'x':50, 'y':51, 'z':52,
       '`':53, '~':54, '!':55, '@':56, '#':57, '$':58, '%':59, '^':60, '&':61, '(':62, ')':63, '-':64, '_':65, '=':66, '+':67, '[':68, ']':69, '{':70, '}':71,
       ',':72, '.':73, '?':74, '\\':75, '/':76, ';':77, '|':78, '<':79, '>':80, "'":81, '"':82, '\n':83,'1':84, '2':85, '3':86,
          '4':87, '5':88, '6':89, '7':90, '8':91, '9':92, '0':93,'’':94, ':':95, '‘':96, '“':97, '”':98, '—':99, '–':100}

    pun2=["!","'",'"',"#","$","%","&","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","|","~","\\","’",":","‘","“","”","—","–"]

    data1=0
    if type(data) in(list,tuple,set):
        data1= data
    elif hasattr(data, 'to_list'):
        data1 = data.to_list()
    else:
        raise TypeError("The data must be of type 'list', 'tuple', 'set', or 'pandas.core.series.Series', but the given data type is {}".format(type(data)))
    #print(data1)
    ttc_list=[]
    for text3 in data1:
        for word3 in text3.split():
            ttc_list.append(word3)
    big_text=' '.join([w3 for w3 in ttc_list])
    for cc2 in pun2:
        big_text= big_text.replace(cc2,' ' + cc2 + ' ')

    unavaible_list=[]
    unavaible_list_tok=[]
    for bt in big_text.split():
        for ct in bt:
            if ct not in d2:
                unavaible_list.append(ct)
    for ult,iit in enumerate(unavaible_list,start=101):
        unavaible_list_tok.append(ult)

    new_d2={}
    for key,value in zip(unavaible_list,unavaible_list_tok):
        new_d2.update({key:value})

    d2.update(new_d2)
    pun3= pun2+unavaible_list
    #print(d2)

    def tok(text,apply=apply_on,dd=d2,pun11=pun3,token_type1=token_type,smart_recognition1=smart_recognition):
      #from optimal_data_selector.text import word_tokenizer
      from optilearn.text import word_tokenizer

      def remove_punctuations(text1):
        pun2=["!",'"',"#","$","%","&","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","|","~","\\"]
        pun3=["'"]
        for p in pun2:
          text1=text1.replace(p,' ')
        tokk=[]
        for w in text1.split():
          tokk.append(w)
        return tokk

      aw_list=[]
      if apply in('alpha','alphabet','alphabets'):
        hax=text.encode('unicode_escape').decode('utf-8')
        for a in hax:
          aw_list.append(dd[a])

        return aw_list

      elif apply in('words','word'):
        key=[]
        value=[]
        if token_type1 == 'advance':
          tok=word_tokenizer(text,smart_recognition=smart_recognition1,output_case=output_token_case,sp_character_tokens=sp_character_tokens,del_words=del_words_or_ch)
        elif token_type1 == 'basic':
          tok=remove_punctuations(text)
        elif token_type1 not in('advance','basic'):
          raise ValueError("token_type value must be ether 'advance' or 'basic'")
        return tok

      elif apply not in('words','word','alpha','alphabet','alphabets'):
        raise ValueError("apply_on value must be ether 'words','word','alpha','alphabet' or 'alphabets'")

    def convertor(list1,dict1):
      list2=[]
      for l in list1:
        list2.append(dict1[l])
      return list2


    def case_change(list1,case1):
      list2=[]
      for i in list1:
        if case1== 'same':
          list2.append(i)
        elif case1 == 'lower':
          list2.append(i.lower())
        elif case1 == 'upper':
          list2.append(i.upper())
      return list2

    if fit_on_new_data == False and word_index_dict == None:
      if apply_on in('alpha','alphabet','alphabets'):
        token1=[]
        for sent in data1:
          tt=tok(sent,apply=apply_on,dd=d2,pun11=pun3,token_type1=token_type,smart_recognition1=smart_recognition)
          token1.append(tt)
        return token1,d2

      elif apply_on in('words','word'): #and add_vocabulary == None:
        key=[]
        key2=[]
        value=0
        dd={}
        for sent in data1:
          tt=tok(sent,apply=apply_on,dd=d2,pun11=pun3,token_type1=token_type,smart_recognition1=smart_recognition)

          if add_vocabulary == None:
            for t in tt:                                          # Looking for change
              key.append(t)
            key1=set(key)
          elif add_vocabulary != None and type(add_vocabulary) in(list,tuple,set):
            for t in tt:
              key.append(t)
            key1=set(key+case_change(add_vocabulary,case1=output_token_case))           # ****************
          elif add_vocabulary != None and type(add_vocabulary) not in(list,tuple,set):
            raise TypeError("The value of 'add_vocabulary' must be a list, tuple, or set object only, but the given type is {}".format(type(add_vocabulary)))

        for k in key1:
          key2.append(k)                                        # Sorted function can be used
        if oob_token != None and type(oob_token) == str:
          key2.insert(0,oob_token)
        elif oob_token != None and type(oob_token) != str:
          raise TypeError("oob_token value must be a string object")
        #return key2,d2
        #key2=sorted(key2)

        if oob_token != None and type(oob_token) == str:
          #for i in range(len(key2)):                          # 30 July change
          value=list(range(len(key2)))
        else:
          #for i in range(1,len(key2)+1):                      # 30 July change
          value=list(range(1,len(key2)+1))

        for kk,vv in zip(key2,value):
          dd.update({kk:vv})
        #return key2,dd
        token2=[]
        token3=[]                                            # implimentation
        for sent1 in data1:
          tt1=tok(sent1,apply=apply_on,dd=dd,pun11=pun3,token_type1=token_type,smart_recognition1=smart_recognition)
          token2.append(tt1)
        for t2 in token2:
          t3=convertor(t2,dd)
          token3.append(t3)
        return token3,dd

    elif fit_on_new_data == True and word_index_dict != None and type(word_index_dict) == dict:
      token4=[]
      token5=[]
      token6=[]
      nn_dict={}
      data22=data1

      def xx(ll,s,ss):
        u=[]
        for i in ll:
          if i in s:
            u.append(i)
          elif i not in s:
            if 0 in ss:
              u.append(ss[0])
            else:
              raise KeyError(f"Word '{i}' not in word_index. Add an oob_token to prevent this error")
        return u

      for k2,v2 in word_index_dict.items():
        nn_dict.update({v2:k2})

      for sent2 in data22:
        tok11=tok(sent2,apply=apply_on,dd=d2,pun11=pun3,token_type1=token_type,smart_recognition1=smart_recognition)
        token4.append(tok11)
      #print(token4)
      for t44 in token4:
        re=xx(t44,word_index_dict,nn_dict)
        token5.append(re)
      #return token5
      for t65 in token5:
        co=convertor(t65,word_index_dict)
        token6.append(co)
      return token6

    elif fit_on_new_data == True and word_index_dict == None:
      raise ValueError("The function needs the dictionary that had been created initially to convert words into tokens.")

