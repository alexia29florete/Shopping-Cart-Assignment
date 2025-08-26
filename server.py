from flask import Flask, request, render_template, redirect, session, url_for
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "super_secret_key" 

ALLOWED_USERS = {
    "test": "test123",
    "admin": "n0h4x0rz-plz",
}

DATABASE_FILE = "database.txt"

def get_cart_size():
    cart = session.get("cart")
    if not isinstance(cart, dict):
        cart = {}
        session["cart"] = cart
    return sum(cart.values())



@app.route('/')
def home():
    products = [
        {"name": "Tenerife Trip", "info": "Exciting Tenerife holiday! Enjoy sun and beaches.", "offers": ["Round-trip flights and airport transfers", 
                                                                                                          "Accomodation for 7 nights at 4★ seaside hotel with breakfast included",
                                                                                                          "Excursion to the picturesque village of Masca and a traditional meal included",
                                                                                                          "Guided tour of Teide National Park",
                                                                                                          "Shopping experience in Santa Cruz - discover local markets, boutiques, and souvenirs",
                                                                                                          "Boat excursion to see dolphins & whales - enjoy the Atlantic breeze while spotting marine life (OPTIONAL: Scuba Diving)",
                                                                                                          "Full-day adventure at Loro Parque"], "price": 750, "image": "tenerife.jpg", "id": "1"},  
        {"name": "Ohrid's Beauty", "info": "Explore the beautiful Ohrid lake!\nBoating and scenery await.", "offers": ["Scenic boat tour on Lake Ohrid",
                                                                                                                       "Accomodation for 4 nights with lake view",
                                                                                                                       "Visit to the Church of St. John at Kaneo - one of the Balkans' most iconic landmarks",
                                                                                                                       "Guided walk through Ohrid Old Town",
                                                                                                                       "Day trip to Skopje - explore Macedonia's vibrant capital, with its mix of history, culture, and modern city life",
                                                                                                                       "Local cuisine experience by the lake"], "price": 350, "image": "Ohrid.jpg", "id": "2"},  
        {"name": "Malta", "info": "Discover Malta's architecture! History and culture combined.", "offers": ["Round-trip flights and airport transfers",
                                                                                                             "Accomodation for 6 nights included",
                                                                                                             "Enjoy the charming movie set and scenic surroundings at Popeye Village",
                                                                                                             "Mdina exploration - walk through the “Silent City” with its medieval architecture and narrow streets",
                                                                                                             "Boat tour in Valletta and enjoy the history of Malta that was brought to life through the cannon firing",
                                                                                                             "Excursion to Gozo Island - explore Tal Mixta Cave and enjoy scenic coastal walks",
                                                                                                             "Enjoy vibrant evening entertainment and local cuisine in St. Julian",
                                                                                                             "Leisure boat trip - relax on the water while taking in Malta's picturesque coastline"], "price": 400, "image": "Malta.jpg", "id": "3"}, 
        {"name": "Maroc's Secret", "info": "Embrace the Moroccan culture with its markets, spices, and colors.", "offers": ["Flight tickets included",
                                                                                                                            "Hotels in thehistorical center, Medina, offered in each city mentioned",
                                                                                                                            "Marrakesh exploration - stroll through vibrant souks, experience local markets, and discover the YSL Garden",
                                                                                                                            "Casablanca visit - admire modern architecture",
                                                                                                                            "Chefchaouen sightseeing tour - explore the famous blue city and its charming street",
                                                                                                                            "Rabat tour - visit historical sites and enjoy Moroccan culture",
                                                                                                                            "Guided city tours & cultural experiences - learn about history, architecture, and local traditions"], "price": 600, "image": "Maroc.jpg", "id": "4"},  
        {"name": "Sahara Desert", "info": "Hop on a camel in Sahara and enjoy sunset dunes adventure.", "offers": ["Atlas Mountains excursion",
                                                                                                                   "Roses Valley villages - visit traditional Berber villages and learn about local life and customs",
                                                                                                                   "Overnight desert camp - spend a night under the stars in a traditional tent in the Sahara desert",
                                                                                                                   "Camel ride - experience a classic camel trek across the dunes",
                                                                                                                   "Sandboarding adventure",
                                                                                                                   "ATV experience - explore the desert terrain on an exciting all-terrain vehicle ride",
                                                                                                                   "Local traditions & culture - enjoy authentic Moroccan music, food, and storytelling around the campfir"], "price": 750, "image": "Sahara.jpg", "id": "5"},  
        {"name": "Málaga Trip", "info": "Explore the sunny beaches and historic streets of Málaga!", "offers": ["Round-trip flights and airport transfers",
                                                                                                                "Accomodation for 5 nights at a seaside hotel with breakfast included",
                                                                                                                "City tour of Málaga - admire architecture, and discover hidden gems",
                                                                                                                "Beach time & relaxation - enjoy the sunny Costa del Sol beaches",
                                                                                                                "Picasso Museum visit - explore the works of Málaga's famous artist, Pablo Picasso",
                                                                                                                "Alcazaba fortress - tour the Moorish citadel with panoramic views of the city",
                                                                                                                "Shopping in city markets - browse local markets and boutique shops for souvenirs",
                                                                                                                "Experience the lively atmosphere of Málaga's bars and cafes savoring traditional Andalusian tapas and seafood dishe"], "price": 450, "image": "Malaga.jpg", "id": "6"},  
        {"name": "Madrid", "info": "Discover Madrid's culture, tapas, and lively plazas!", "offers": ["City tour of Madrid - explore grand plazas, historic streets, and iconic landmarks",
                                                                                                      "Royal Palace visit - discover the opulent rooms and gardens of Spain's royal residence",
                                                                                                      "Prado Museum experience - admire world-famous art collections by Goya, Velázquez, and more",
                                                                                                      "Tapas tasting tour - enjoy traditional Spanish tapas in local bars and eateries in Plaza Mayor",
                                                                                                      "Visit Real Madrid's Stadium in Madrid",
                                                                                                      "Retiro Park stroll - relax in the lush gardens and enjoy boating on the park's lake",
                                                                                                      "Shopping in Gran Vía - browse boutiques and department stores along Madrid's main avenue",
                                                                                                      "Enjoy a panoramic view of the city at 360 Rooftop"], "price": 500, "image": "Madrid.jpg", "id": "7"},  
        {"name": "Istanbul", "info": "Get lost in Istanbul's bazaars and enjoy the black tea!", "offers": ["Round-trip flights and airport transfers",
                                                                                                           "Accomodation for 5 nights included",
                                                                                                           "Discover the historical sites: Hagia Sophia, Blue Mosque, and Topkapi Palace",
                                                                                                           "Grand Bazaar shopping - experience the bustling markets and haggle for souvenirs",
                                                                                                           "Bosphorus boat cruise - enjoy panoramic views of the city from the water",
                                                                                                           "Spend one day getting lost in the asian part of the city",
                                                                                                           "Enjoy the ride with Taksim Tunel and enjoy a San Sebastian cake near Galata Tower",
                                                                                                           "Local tea & coffee culture - relax in traditional tea houses and sample Turkish coffee"], "price": 550, "image": "Istanbul.jpg", "id": "8"},  
        {"name": "Paris", "info": "Discover the charm of Paris! Eiffel Tower, cafés, and art await.", "offers": ["Accomodation for 6 nights and flight tickets included",
                                                                                                                 "Visit the Eiffel Tower - enjoy panoramic views of the City of Light from the iconic landmark",
                                                                                                                 "Explore the Louvre Museum - admire world-famous art, including the Mona Lisa and Venus de Milo.",
                                                                                                                 "Stroll along the Champs-Élysées - experience shopping, cafés, and historic monuments.",
                                                                                                                 "Seine River Cruise - enjoy a scenic boat ride along Paris' beautiful riverbanks.",
                                                                                                                 "Montmartre & Sacré-Cœur - wander through the artistic district and visit the stunning basilica.",
                                                                                                                 "Local culinary experience - taste French pastries, cheese, and wine at authentic cafés.",
                                                                                                                 "Evening lights tour - admire Paris' illuminated landmarks, including Notre-Dame, Mouline Rouge and the Arc de Triomphe."], "price": 700, "image": "Paris.jpg", "id": "9"},  
        {"name": "Disneyland", "info": "Experience the magic of Disneyland! Rides, shows, and fun for all ages.", "offers": ["Accomodation in one of Disneyland's resorts for 3 days",
                                                                                                                             "Access to the both Disneyland Parks",
                                                                                                                             "Fast lane ticket - for enjoying the experience without waiting at long queues"], "price": 650, "image": "Disneyland.jpg", "id": "10"}, 
        {"name": "Auschwitz-Birkenau", "info": "Visit the historical memorial and take a journey in history.", "offers": ["Accomodation for 3 nights in Krakow and flight tickets included",
                                                                                                                          "One day trip in the concentration camp Auschwitz-Birkenau",
                                                                                                                          "Guided tour in the heart of Krakow, discovering its history",
                                                                                                                          "Tickets to Oskar Schindler's Museum"], "price": 300, "image": "Auschwitz.jpg", "id": "11"},  
        {"name": "F1 Race", "info": "Feel the adrenaline of racing! Speed, excitement and legendary tracks.", "offers": ["Grandstand tickets to any European Circuit from the calendar, except Monaco",
                                                                                                                         "Accomodation for the entire weekend included in the nearest city to the location of the track",
                                                                                                                         "Pit Lane Walk - a possibility of meeting your favourite team and driver"], "price": 500, "image": "Hungaroring.jpg", "id": "12"},  
        {"name": "Positano", "info": "Relax in the beautiful Positano! Admire stunning coastlines and sights.", "offers": ["Accomodation for 2 nights in Naples and 2 nights in Positano",
                                                                                                                           "Tour in the heart of Naples", 
                                                                                                                           "Scenic coastal walk - explore the breathtaking Sentiero degli Dei with panoramic views",
                                                                                                                           "Boat tour to Capri - sail across crystal-clear waters to the famous island",
                                                                                                                           "Blue Lagoon experience - swim in hidden turquoise coves accessible by boat",
                                                                                                                           "Historic center stroll - wander Positano's colorful alleys and boutiques",
                                                                                                                           "Sunset viewpoint - admire the sea at golden hour from a cliffside terrace"], "price": 700, "image": "Positano.jpg", "id": "13"},  
        {"name": "Greek Paradise", "info": "Explore Greece's stunning islands and discover beaches, and ancient ruins", "offers": ["Flight and accommodation included ",
                                                                                                                                   "Excursion to Athens - discover the Parthenon, Acropolis Museum, and Plaka district",
                                                                                                                                   "Island hopping - explore Mykonos, Crete, and hidden gems of the Aegean Sea",
                                                                                                                                   "Zakynthos adventure - visit the Blue Caves and Navagio Beach, and spot sea turtles in their natural habitat",
                                                                                                                                   "Santorini sunset - witness the world-famous sunset over Oia's white houses",
                                                                                                                                   "Boat excursion - sail through volcanic islands and crystal caves",
                                                                                                                                   "Traditional cuisine - enjoy moussaka, souvlaki, and fresh seafood by the sea"], "price": 600, "image": "Grecia.jpg", "id": "14"},  
        {"name": "Cairo Adventure", "info": "Discover the wonders of Cairo! Pyramids and markets await.", "offers": ["Flight tickets and accomodation for 4 nights included",
                                                                                                                     "Pyramids of Giza - discover one of the Seven Wonders of the Ancient World",
                                                                                                                     "Sphinx visit - discover the iconic limestone guardian of the pyramids and the history of it",
                                                                                                                     "Egyptian Museum - see treasures of Tutankhamun and ancient artifacts",
                                                                                                                     "Nile river cruise - experience Cairo from the water with dinner on board",
                                                                                                                     "Khan el-Khalili bazaar - shop for spices, jewelry, and local crafts",
                                                                                                                     "Local cuisine - taste koshari, falafel, and traditional Egyptian tea",
                                                                                                                     "Red Sea excursion - enjoy snorkeling among colorful corals, exotic fish, optional scuba diving, and even dolphin spotting"], "price": 500, "image": "Egipt.jpg", "id": "15"},  
        {"name": "Lisbon", "info": "Enjoy Lisbon's charm! Photograph colorful streets and ocean views.", "offers": ["Flight and accommodation included - enjoy a comfortable journey and a charming stay in Lisbon",
                                                                                                                    "Tram 28 ride - discover Lisbon's historic neighborhoods on its iconic tram",
                                                                                                                    "Belém Tower - visit the city's riverside fortress and UNESCO site",
                                                                                                                    "Alfama district - wander through narrow streets filled with fado music",
                                                                                                                    "Sintra day trip - explore palaces, castles, and fairy-tale landscapes nearby",
                                                                                                                    "Ocean views - relax at Miradouros for panoramic city and sea views",
                                                                                                                    "Cabo da Roca - stand at the westernmost point of continental Europe and admire dramatic cliffs over the Atlantic"], "price": 450, "image": "Portugalia.jpg", "id": "16"},  
    ]

    cart_size = get_cart_size()
    return render_template("products.html", products=products, active_page="home", cart_size=cart_size)

@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = request.args.get("error_msg", "")  # ia mesajul din query param
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username in ALLOWED_USERS and ALLOWED_USERS[username] == password:
            session["authenticated"] = True
            session["username"] = username
            return redirect(url_for("home"))
        else:
            error_msg = "Invalid username or password!"

    cart_size = get_cart_size()
    return render_template('login.html', active_page='login', error_msg=error_msg, cart_size=cart_size)

# helper ca să găsim produsul după id
def get_product(product_id):
    products = [
        {"name": "Tenerife Trip", "info": "Exciting Tenerife holiday! Enjoy sun and beaches.", "offers": ["Round-trip flights and airport transfers", 
                                                                                                          "Accomodation for 7 nights at 4★ seaside hotel with breakfast included",
                                                                                                          "Excursion to the picturesque village of Masca and a traditional meal included",
                                                                                                          "Guided tour of Teide National Park",
                                                                                                          "Shopping experience in Santa Cruz - discover local markets, boutiques, and souvenirs",
                                                                                                          "Boat excursion to see dolphins & whales - enjoy the Atlantic breeze while spotting marine life (OPTIONAL: Scuba Diving)",
                                                                                                          "Full-day adventure at Loro Parque"], "price": 750, "image": "tenerife.jpg", "id": "1"},  
        {"name": "Ohrid's Beauty", "info": "Explore the beautiful Ohrid lake!\nBoating and scenery await.", "offers": ["Scenic boat tour on Lake Ohrid",
                                                                                                                       "Accomodation for 4 nights with lake view",
                                                                                                                       "Visit to the Church of St. John at Kaneo - one of the Balkans' most iconic landmarks",
                                                                                                                       "Guided walk through Ohrid Old Town",
                                                                                                                       "Day trip to Skopje - explore Macedonia's vibrant capital, with its mix of history, culture, and modern city life",
                                                                                                                       "Local cuisine experience by the lake"], "price": 350, "image": "Ohrid.jpg", "id": "2"},  
        {"name": "Malta", "info": "Discover Malta's architecture! History and culture combined.", "offers": ["Round-trip flights and airport transfers",
                                                                                                             "Accomodation for 6 nights included",
                                                                                                             "Enjoy the charming movie set and scenic surroundings at Popeye Village",
                                                                                                             "Mdina exploration - walk through the “Silent City” with its medieval architecture and narrow streets",
                                                                                                             "Boat tour in Valletta and enjoy the history of Malta that was brought to life through the cannon firing",
                                                                                                             "Excursion to Gozo Island - explore Tal Mixta Cave and enjoy scenic coastal walks",
                                                                                                             "Enjoy vibrant evening entertainment and local cuisine in St. Julian",
                                                                                                             "Leisure boat trip - relax on the water while taking in Malta's picturesque coastline"], "price": 400, "image": "Malta.jpg", "id": "3"}, 
        {"name": "Maroc's Secret", "info": "Embrace the Moroccan culture with its markets, spices, and colors.", "offers": ["Flight tickets included",
                                                                                                                            "Hotels in thehistorical center, Medina, offered in each city mentioned",
                                                                                                                            "Marrakesh exploration - stroll through vibrant souks, experience local markets, and discover the YSL Garden",
                                                                                                                            "Casablanca visit - admire modern architecture",
                                                                                                                            "Chefchaouen sightseeing tour - explore the famous blue city and its charming street",
                                                                                                                            "Rabat tour - visit historical sites and enjoy Moroccan culture",
                                                                                                                            "Guided city tours & cultural experiences - learn about history, architecture, and local traditions"], "price": 600, "image": "Maroc.jpg", "id": "4"},    
        {"name": "Sahara Desert", "info": "Hop on a camel in Sahara and enjoy sunset dunes adventure.", "offers": ["Atlas Mountains excursion",
                                                                                                                   "Roses Valley villages - visit traditional Berber villages and learn about local life and customs",
                                                                                                                   "Overnight desert camp - spend a night under the stars in a traditional tent in the Sahara desert",
                                                                                                                   "Camel ride - experience a classic camel trek across the dunes",
                                                                                                                   "Sandboarding adventure",
                                                                                                                   "ATV experience - explore the desert terrain on an exciting all-terrain vehicle ride",
                                                                                                                   "Local traditions & culture - enjoy authentic Moroccan music, food, and storytelling around the campfir"], "price": 750, "image": "Sahara.jpg", "id": "5"},  
        {"name": "Málaga Trip", "info": "Explore the sunny beaches and historic streets of Málaga!", "offers": ["Round-trip flights and airport transfers",
                                                                                                                "Accomodation for 5 nights at a seaside hotel with breakfast included",
                                                                                                                "City tour of Málaga - admire architecture, and discover hidden gems",
                                                                                                                "Beach time & relaxation - enjoy the sunny Costa del Sol beaches",
                                                                                                                "Picasso Museum visit - explore the works of Málaga's famous artist, Pablo Picasso",
                                                                                                                "Alcazaba fortress - tour the Moorish citadel with panoramic views of the city",
                                                                                                                "Shopping in city markets - browse local markets and boutique shops for souvenirs",
                                                                                                                "Experience the lively atmosphere of Málaga's bars and cafes savoring traditional Andalusian tapas and seafood dishe"], "price": 450, "image": "Malaga.jpg", "id": "6"},  
        {"name": "Madrid", "info": "Discover Madrid's culture, tapas, and lively plazas!", "offers": ["City tour of Madrid - explore grand plazas, historic streets, and iconic landmarks",
                                                                                                      "Royal Palace visit - discover the opulent rooms and gardens of Spain's royal residence",
                                                                                                      "Prado Museum experience - admire world-famous art collections by Goya, Velázquez, and more",
                                                                                                      "Tapas tasting tour - enjoy traditional Spanish tapas in local bars and eateries in Plaza Mayor",
                                                                                                      "Visit Real Madrid's Stadium in Madrid",
                                                                                                      "Retiro Park stroll - relax in the lush gardens and enjoy boating on the park's lake",
                                                                                                      "Shopping in Gran Vía - browse boutiques and department stores along Madrid's main avenue",
                                                                                                      "Enjoy a panoramic view of the city at 360 Rooftop"], "price": 500, "image": "Madrid.jpg", "id": "7"},  
        {"name": "Istanbul", "info": "Get lost in Istanbul's bazaars and enjoy the black tea!", "offers": ["Round-trip flights and airport transfers",
                                                                                                           "Accomodation for 5 nights included",
                                                                                                           "Discover the historical sites: Hagia Sophia, Blue Mosque, and Topkapi Palace",
                                                                                                           "Grand Bazaar shopping - experience the bustling markets and haggle for souvenirs",
                                                                                                           "Bosphorus boat cruise - enjoy panoramic views of the city from the water",
                                                                                                           "Spend one day getting lost in the asian part of the city",
                                                                                                           "Enjoy the ride with Taksim Tunel and enjoy a San Sebastian cake near Galata Tower",
                                                                                                           "Local tea & coffee culture - relax in traditional tea houses and sample Turkish coffee"], "price": 550, "image": "Istanbul.jpg", "id": "8"},    
        {"name": "Paris", "info": "Discover the charm of Paris! Eiffel Tower, cafés, and art await.", "offers": ["Accomodation for 6 nights and flight tickets included",
                                                                                                                 "Visit the Eiffel Tower - enjoy panoramic views of the City of Light from the iconic landmark",
                                                                                                                 "Explore the Louvre Museum - admire world-famous art, including the Mona Lisa and Venus de Milo.",
                                                                                                                 "Stroll along the Champs-Élysées - experience shopping, cafés, and historic monuments.",
                                                                                                                 "Seine River Cruise - enjoy a scenic boat ride along Paris' beautiful riverbanks.",
                                                                                                                 "Montmartre & Sacré-Cœur - wander through the artistic district and visit the stunning basilica.",
                                                                                                                 "Local culinary experience - taste French pastries, cheese, and wine at authentic cafés.",
                                                                                                                 "Evening lights tour - admire Paris' illuminated landmarks, including Notre-Dame, Mouline Rouge and the Arc de Triomphe."], "price": 700, "image": "Paris.jpg", "id": "9"},    
        {"name": "Disneyland", "info": "Experience the magic of Disneyland! Rides, shows, and fun for all ages.", "offers": ["Accomodation in one of Disneyland's resorts for 3 days",
                                                                                                                             "Access to the both Disneyland Parks",
                                                                                                                             "Fast lane ticket - for enjoying the experience without waiting at long queues"], "price": 650, "image": "Disneyland.jpg", "id": "10"}, 
        {"name": "Auschwitz-Birkenau", "info": "Visit the historical memorial and take a journey in history.", "offers": ["Accomodation for 3 nights in Krakow and flight tickets included",
                                                                                                                          "One day trip in the concentration camp Auschwitz-Birkenau",
                                                                                                                          "Guided tour in the heart of Krakow, discovering its history",
                                                                                                                          "Tickets to Oskar Schindler's Museum"], "price": 300, "image": "Auschwitz.jpg", "id": "11"},  
        {"name": "F1 Race", "info": "Feel the adrenaline of racing! Speed, excitement and legendary tracks.", "offers": ["Grandstand tickets to any European Circuit from the calendar, except Monaco",
                                                                                                                         "Accomodation for the entire weekend included in the nearest city to the location of the track",
                                                                                                                         "Pit Lane Walk - a possibility of meeting your favourite team and driver"], "price": 500, "image": "Hungaroring.jpg", "id": "12"},  
        {"name": "Positano", "info": "Relax in the beautiful Positano! Admire stunning coastlines and sights.", "offers": ["Accomodation for 2 nights in Naples and 2 nights in Positano",
                                                                                                                           "Tour in the heart of Naples", 
                                                                                                                           "Scenic coastal walk - explore the breathtaking Sentiero degli Dei with panoramic views",
                                                                                                                           "Boat tour to Capri - sail across crystal-clear waters to the famous island",
                                                                                                                           "Blue Lagoon experience - swim in hidden turquoise coves accessible by boat",
                                                                                                                           "Historic center stroll - wander Positano's colorful alleys and boutiques",
                                                                                                                           "Sunset viewpoint - admire the sea at golden hour from a cliffside terrace"], "price": 700, "image": "Positano.jpg", "id": "13"},  
        {"name": "Greek Paradise", "info": "Explore Greece's stunning islands and discover beaches, and ancient ruins", "offers": ["Flight and accommodation included ",
                                                                                                                                   "Excursion to Athens - discover the Parthenon, Acropolis Museum, and Plaka district",
                                                                                                                                   "Island hopping - explore Mykonos, Crete, and hidden gems of the Aegean Sea",
                                                                                                                                   "Zakynthos adventure - visit the Blue Caves and Navagio Beach, and spot sea turtles in their natural habitat",
                                                                                                                                   "Santorini sunset - witness the world-famous sunset over Oia's white houses",
                                                                                                                                   "Boat excursion - sail through volcanic islands and crystal caves",
                                                                                                                                   "Traditional cuisine - enjoy moussaka, souvlaki, and fresh seafood by the sea"], "price": 600, "image": "Grecia.jpg", "id": "14"},    
        {"name": "Cairo Adventure", "info": "Discover the wonders of Cairo! Pyramids and markets await.", "offers": ["Flight tickets and accomodation for 4 nights included",
                                                                                                                     "Pyramids of Giza - discover one of the Seven Wonders of the Ancient World",
                                                                                                                     "Sphinx visit - discover the iconic limestone guardian of the pyramids and the history of it",
                                                                                                                     "Egyptian Museum - see treasures of Tutankhamun and ancient artifacts",
                                                                                                                     "Nile river cruise - experience Cairo from the water with dinner on board",
                                                                                                                     "Khan el-Khalili bazaar - shop for spices, jewelry, and local crafts",
                                                                                                                     "Local cuisine - taste koshari, falafel, and traditional Egyptian tea",
                                                                                                                     "Red Sea excursion - enjoy snorkeling among colorful corals, exotic fish, optional scuba diving, and even dolphin spotting"], "price": 500, "image": "Egipt.jpg", "id": "15"},
        {"name": "Lisbon", "info": "Enjoy Lisbon's charm! Photograph colorful streets and ocean views.", "offers": ["Flight and accommodation included - enjoy a comfortable journey and a charming stay in Lisbon",
                                                                                                                    "Tram 28 ride - discover Lisbon's historic neighborhoods on its iconic tram",
                                                                                                                    "Belém Tower - visit the city's riverside fortress and UNESCO site",
                                                                                                                    "Alfama district - wander through narrow streets filled with fado music",
                                                                                                                    "Sintra day trip - explore palaces, castles, and fairy-tale landscapes nearby",
                                                                                                                    "Ocean views - relax at Miradouros for panoramic city and sea views",
                                                                                                                    "Cabo da Roca - stand at the westernmost point of continental Europe and admire dramatic cliffs over the Atlantic"], "price": 450, "image": "Portugalia.jpg", "id": "16"},  
    ]
    return next((p for p in products if p["id"] == product_id), None)


@app.route("/cart", methods=["GET", "POST"])
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = get_product(pid)
        if product:
            subtotal = product["price"] * qty
            total += subtotal
            items.append({
                "id": pid,
                "image": product["image"],
                "name": product["name"],
                "price": product["price"],
                "qty": qty,
                "subtotal": subtotal
            })
    
    error_msg = None

    if request.method == "POST":
    # Daca utilizatorul a trimis formularul (apasand pe buton)

        for item in items:
            # Iteram prin fiecare produs din cos

            start_date = request.form.get(f"start_date_{item['id']}")
            end_date = request.form.get(f"end_date_{item['id']}")
            # Luam datele introduse pentru fiecare produs (start_date si end_date)

            if not start_date or not end_date:
                error_msg = "Please select both start and end dates."
                break
            # Daca lipseste una dintre date, afisam mesaj de eroare si oprim verificarea

            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
                today = datetime.today().date()
                # Convertim string-urile in obiecte de tip data
                # today este data curenta

                if start_dt < today:
                    error_msg = f"Invalid start date for {item['name']}: cannot be in the past."
                    break
                # Verificam daca start_date este in trecut -> daca da, eroare

                if end_dt <= start_dt:
                    error_msg = f"Invalid dates for {item['name']}: end date must be after start date."
                    break
                # Verificam daca end_date este mai mic sau egal cu start_date -> eroare

            except ValueError:
                error_msg = f"Invalid date format for {item['name']}."
                break
            # Daca datele nu au format corect (nu sunt YYYY-MM-DD), afisam eroare

        if not error_msg:
            # Daca nu exista nicio eroare -> datele sunt valide

            for item in items:
                session[f"start_date_{item['id']}"] = request.form.get(f"start_date_{item['id']}")
                session[f"end_date_{item['id']}"] = request.form.get(f"end_date_{item['id']}")
            # Salvam in sesiune datele pentru fiecare produs

            return redirect(url_for("checkout"))
            # Dupa ce datele sunt salvate, redirectionam utilizatorul catre pagina de checkout


    cart_size = sum(cart.values())  # total produse
    return render_template("cart.html", items=items, total=total, cart_size=cart_size, error_msg=error_msg, active_page="view_cart")


@app.route("/cart/add-item/")
def add_to_cart():
    product_id = request.args.get("id")
    if not product_id:
        return "No product id provided", 400
    
    cart = session.get("cart", {}) # ma asigur ca am un cos valid, chiar daca utilizatorul nu a adaugat nimic inca
    cart[product_id] = cart.get(product_id, 0) + 1 # verifică dacă produsul există deja; dacă nu, începe de la 0. Apoi se adaugă 1 la cantitate.
    session["cart"] = cart
    
    return redirect(url_for("home"))


@app.route("/cart/update-item/")
def update_cart_item():
    product_id = request.args.get("id")
    action = request.args.get("action")  # "increase" sau "decrease"
    cart = session.get("cart", {})

    if product_id in cart:
        if action == "increase":
            cart[product_id] += 1
        elif action == "decrease":
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]

    session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.route("/cart/remove-item")
def remove_from_cart():
    product_id = request.args.get("id")
    if not product_id:
        return "No product id provided", 400
    
    cart = session.get("cart", {})
    
    if product_id in cart:
        del cart[product_id]

    session["cart"] = cart
    return redirect(url_for("view_cart"))



@app.route("/toggle_wishlist/<product_id>")
def toggle_wishlist(product_id):
    # verifică dacă userul e logat
    if not session.get("authenticated"):
        return redirect(url_for("login", error_msg="Please log in first!"))

    wishlist = session.get("wishlist", [])
    # Tip de date implicit: listă ([]). -> ma intereseaza ce produse i-au placut, nu cate
    if product_id in wishlist:
        wishlist.remove(product_id)
    else:
        wishlist.append(product_id)
    session["wishlist"] = wishlist
    return redirect(url_for("home"))



@app.route('/product/<product_id>')
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        return "Product not found", 404

    cart_size = get_cart_size()
    return render_template("product_detail.html", product=product, cart_size=cart_size)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('authenticated', None)
    return redirect(url_for('home'))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", {})
    # Tip de date implicit: dicționar ({})
    items = []
    total = 0
    error_msg = None

    for pid, qty in cart.items():
        product = get_product(pid)
        if product:
            subtotal = product["price"] * qty
            total += subtotal
            items.append({
                "id": pid,
                "name": product["name"],
                "price": product["price"],
                "qty": qty,
                "subtotal": subtotal
            })

    order_submitted = False
    order = None

    if request.method == "POST":
        # verifică datele 

        if not error_msg:
            full_name = request.form.get("full_name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            address = request.form.get("address")
            payment_method = request.form.get("payment_method")

            order = {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "address": address,
                "payment_method": payment_method,
                "products": items,
                "total": total,
            }

            # Print în consolă pentru verificare
            print(order)

            #salvare persistenta
            with open(DATABASE_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(order) + "\n")

            session["cart"] = {}
            order_submitted = True
    cart_size = get_cart_size()
    return render_template("checkout.html", active_page='cart', items=items, total=total, order_submitted=order_submitted, error_msg=error_msg, order = order, cart_size = cart_size)


@app.route('/favourites')
def favourites():
    if not session.get("authenticated"):
        return redirect(url_for("login", error_msg="Please log in first!"))

    wishlist = session.get("wishlist", [])
    items = [get_product(pid) for pid in wishlist if get_product(pid)]
    
    cart_size = get_cart_size()
    return render_template('favourites.html', active_page='favourites', cart_size=cart_size, items=items)


@app.route('/favourites/add-all-to-cart')
def add_all_to_cart():
    if not session.get("authenticated"):
        return redirect(url_for("login", error_msg="Please log in first!"))

    wishlist = session.get("wishlist", [])
    cart = session.get("cart", {})

    for pid in wishlist:
        cart[pid] = cart.get(pid, 0) + 1

    session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route('/favourites/remove/<product_id>')
def remove_from_wishlist(product_id):
    if not session.get("authenticated"):
        return redirect(url_for("login", error_msg="Please log in first!"))

    wishlist = session.get("wishlist", [])
    if product_id in wishlist:
        wishlist.remove(product_id)
        session["wishlist"] = wishlist

    return redirect(url_for("favourites"))


@app.route("/favourites/add-to-cart/<product_id>")
def add_to_cart_wishlist(product_id):
    if not session.get("authenticated"):
        return redirect(url_for("login", error_msg="Please log in first!"))

    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session["cart"] = cart

    return redirect(url_for("favourites"))



@app.route('/contact', methods=["GET", "POST"])
def contact():
    cart_size = get_cart_size()
    return render_template('contact.html', active_page='contact', cart_size=cart_size)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)