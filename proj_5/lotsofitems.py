from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import User, Catalog, Item

engine = create_engine('sqlite:///items.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base = declarative_base()
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Catalog Basketball
Basketball = Catalog(name="Basketball", user_id=1)
session.add(Basketball)
session.commit()

Basketball = Item(name="Basketball",
                  description="A basketball is a spherical inflated ball used in basketball games. Basketballs typically range in size from very small promotional items only a few inches in diameter to extra large balls nearly a foot in diameter used in training exercises. For example, a basketball in high school would be about 27 inches in circumference, while an NBA ball would be about 29 inches. The actual standard size of a basketball in the NBA is 29.5 to 29.85 inches (74.9 to 75.8 cm) in circumference.",
                  catalog_id=1,
                  user_id=1,
                  image="https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png")
session.add(Basketball)
session.commit()

Backboard = Item(name="Backboard",
                 description="A backboard is a piece of basketball equipment. It is a raised vertical board with a basket attached. It is made of a flat, rigid piece of, often Plexiglas or tempered glass which also has the properties of safety glass when accidentally shattered. It is usually rectangular as used in NBA, NCAA and international basketball. In recreational environments, a backboard may be oval or a fan-shape, particularly in non-professional games.",
                 catalog_id=1,
                 user_id=1,
                 image="https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Basketball_net.jpg/320px-Basketball_net.jpg")
session.add(Backboard)
session.commit()


# Catalog Football
Football = Catalog(name="Football", user_id=1)
session.add(Football)
session.commit()

Football = Item(name="Football",
                description='A football, soccer ball, or association football ball is the ball used in the sport of association football. The name of the ball varies according to whether the sport is called "football", "soccer", or "association football". The ball\'s spherical shape, as well as its size, weight, and material composition, are specified by Law 2 of the Laws of the Game maintained by the International Football Association Board. Additional, more stringent, standards are specified by FIFA and subordinate governing bodies for the balls used in the competitions they sanction.',
                catalog_id=2,
                user_id=1,
                image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/1998_-_Tricolore_%28France%29_%284170715889%29.jpg/240px-1998_-_Tricolore_%28France%29_%284170715889%29.jpg")
session.add(Football)
session.commit()

Kit = Item(name="Soccer Kit",
                 description="In association football, kit (also referred to as strip or soccer uniform) is the standard equipment and attire worn by players. The sport's Laws of the Game specify the minimum kit which a player must use, and also prohibit the use of anything that is dangerous to either the player or another participant. Individual competitions may stipulate further restrictions, such as regulating the size of logos displayed on shirts and stating that, in the event of a match between teams with identical or similar colours, the away team must change to different coloured attire.",
                 catalog_id=2,
                 user_id=1,
                 image="https://ae01.alicdn.com/kf/HTB18amsPVXXXXbIXXXXq6xXFXXXm/new-men-plate-football-clothes-Training-Games-men-s-font-b-soccer-b-font-jerseys-adult.jpg")
session.add(Kit)
session.commit()

Card = Item(name="Penalty Card",
             description='A penalty card is used in many sports as a means of warning, reprimanding or penalising a player, coach or team official. Penalty cards are most commonly used by referees or umpires to indicate that a player has committed an offense. The referee will hold the card above his or her head while looking or pointing towards the player that has committed the offense. The colour and/or shape of the card used by the official indicates the type or seriousness of the offence and the level of punishment that is to be applied.',
             catalog_id=2,
             user_id=1,
             image="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Yellow_card.svg/200px-Yellow_card.svg.png")
session.add(Card)
session.commit()


# Catalog PingPong
PingPong = Catalog(name="PingPong", user_id=1)
session.add(PingPong)
session.commit()

Ball = Item(name="Ball",
            description="The ball is made of celluloid plastic as of 2015, colored white or orange, with a matte finish. The choice of ball color is made according to the table color and its surroundings. For example, a white ball is easier to see on a green or blue table than it is on a grey table.",
            catalog_id=3,
            user_id=1,
            image="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Assortment_of_40_mm_table_tennis_balls.jpg/320px-Assortment_of_40_mm_table_tennis_balls.jpg")
session.add(Ball)
session.commit()

Racket = Item(name="Racket",
              description='A basic table tennis racket (has notions of being called a "paddle" or "bat") is used by table tennis players. The table tennis racket is usually made from laminated wood covered with rubber on one or two sides depending on the player\'s grip. Unlike a conventional "racket", it does not include strings strung across an open frame. The USA generally uses the term "paddle" while Europeans and Asians use the term "bat" and the official ITTF term is "racket".',
              catalog_id=3,
              user_id=1,
              image="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Tabletennis.jpg/320px-Tabletennis.jpg")
session.add(Racket)
session.commit()

Table = Item(name="Table",
             description='The table is 2.74 m (9.0 ft) long, 1.525 m (5.0 ft) wide, and 76 cm (2.5 ft) high with any continuous material so long as the table yields a uniform bounce of about 23 cm (9.1 in) when a standard ball is dropped onto it from a height of 30 cm (11.8 in), or about 77%. The table or playing surface is uniformly dark coloured and matte, divided into two halves by a net at 15.25 cm (6.0 in) in height. The ITTF approves only wooden tables or their derivates. Concrete tables with a steel net or a solid concrete partition are sometimes available in outside public spaces, such as parks.',
             catalog_id=3,
             user_id=1,
             image="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Table_Tennis_Table_Blue.svg/640px-Table_Tennis_Table_Blue.svg.png")
session.add(Table)
session.commit()


# Catalog Snowboarding
Snowboarding = Catalog(name="Snowboarding", user_id=1)
session.add(Snowboarding)
session.commit()

Snowboard = Item(name="Snowboard",
                 description='Snowboards are boards that are usually the width of one\'s foot longways, with the ability to glide on snow. Snowboards are differentiated from monoskis by the stance of the user. In monoskiing, the user stands with feet inline with direction of travel (facing tip of monoski/downhill) (parallel to long axis of board), whereas in snowboarding, users stand with feet transverse (more or less) to the longitude of the board. Users of such equipment may be referred to as snowboarders.',
                 catalog_id=4,
                 user_id=1,
                 image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Snowboard_with_Strap-In_Bindings_and_Stomp_Pad.png/800px-Snowboard_with_Strap-In_Bindings_and_Stomp_Pad.png")
session.add(Snowboard)
session.commit()

Goggles = Item(name="Goggles",
               description='Goggles or safety glasses are forms of protective eyewear that usually enclose or protect the area surrounding the eye in order to prevent particulates, water or chemicals from striking the eyes. They are used in chemistry laboratories and in woodworking. They are often used in snow sports as well, and in swimming. Goggles are often worn when using power tools such as drills or chainsaws to prevent flying particles from damaging the eyes. Many types of goggles are available as prescription goggles for those with vision problems.',
               catalog_id=4,
               user_id=1,
               image="http://scene7.zumiez.com/is/image/zumiez/pdp_hero/Electric-EG2-Matte-Black-Brose-Red-Chrome-Snowboard-Goggles-_267724.jpg")
session.add(Goggles)
session.commit()


# Catalog Hockey
Hockey = Catalog(name="Hockey", user_id=1)
session.add(Hockey)
session.commit()

Stick = Item(name="Hockey Stick",
             description="A hockey stick is a piece of equipment used in field hockey, ice hockey, roller hockey or underwater hockey to move the ball or puck.",
             catalog_id=5,
             user_id=1,
             image="https://cdn.shopify.com/s/files/1/0314/1049/products/Pro_Stock_Hockey_Stick_-_bauer-supreme-totalone-mx3_2b0f4a1d-ca9a-4141-a558-010db0435420.jpg?v=1466623278")
session.add(Stick)
session.commit()

Puck = Item(name="Hockey Puck",
            description="A hockey puck is a disk made of vulcanized rubber that serves the same functions in various games as a ball does in ball games. The best-known use of pucks is in ice hockey, a major international sport.",
            catalog_id=5,
            user_id=1,
            image="https://images-na.ssl-images-amazon.com/images/I/419fcN-UGlL._SX355_.jpg")
session.add(Puck)
session.commit()

