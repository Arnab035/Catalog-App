from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

User1 = User(name="Bryan", email="bryan.texas@gmail.com",
	         picture="http://weknowyourdreams.com/images/dog/dog-07.jpg")
session.add(User1)
session.commit()

category1 = Category(user_id= 1, name="Soccer")
session.add(category1)
session.commit()

category2 = Category(user_id=1, name="Basketball")
session.add(category2)
session.commit()

category3 = Category(user_id=1, name ="Baseball")
session.add(category3)
session.commit()

category4 = Category(user_id=1, name="Frisbee")
session.add(category4)
session.commit()

category5 = Category(user_id=1, name="Snowboarding")
session.add(category5)
session.commit()

category6 = Category(user_id=1, name="Rock Climbing")
session.add(category6)
session.commit()

category7 = Category(user_id=1, name="Foosball")
session.add(category7)
session.commit()

category8 = Category(user_id=1, name="Skating")
session.add(category8)
session.commit()

category9 = Category(user_id=1, name="Hockey")
session.add(category9)
session.commit()

item1 = Item(user_id=1, category_id=9, name="Stick", 
	         picture="http://www.sukhdevandco.com/products/"+
	         "hockey/field_hockey_sticks.jpg",
	         description = "A hockey stick is a piece of equipment"+
	         " used in field hockey, ice hockey , roller hockey or"+
	         " underwater hockey to move the ball or puck."+
	         " Traditionally hockey sticks have been made from wood,"+
	         " more specifically Mulberry.")

session.add(item1)
session.commit()

item2 = Item(user_id=1, category_id=5, name="Goggles", 
	         picture="https://coresites-cdn.factorymedia.com/"
	         +"whitelines_new/wp-content/uploads/2014/10/"
	         +"dragon-d1-best-snowboard-goggles-2014-2015-.jpg",
	         description= " These protect the eyes from glare"+
	         " and from icy particles flying up from"+
	         " the ground when snowboarding.")

session.add(item2)
session.commit()

item3 = Item(user_id=1, category_id=5, name="Snowboard", 
			 picture="http://www.carbonfibergear.com/"+
			 "wp-content/uploads/2009/02/"+
			 "the-whip-fr-117-snowboard.jpg", 
	         description="Snowboards are boards that are usually"+
	         " the width of one's foot longways"+
	         ", with the ability to glide on snow."+
	         "Size and shape variances in the boards accommodate"
	         +" for different snow conditions and riding styles.")

session.add(item3)
session.commit()

item4 = Item(user_id=1, category_id=2, name="Basketball(ball)", 
			 picture="https://upload.wikimedia.org/wikipedia/commons"+
			 "/7/7a/Basketball.png",
			 description="A basketball is a spherical inflated ball"+
			 " used in a game of basketball. "+
			 "Basketballs typically range in size from very"+
			 " small promotional items"+
			 " only a few inches in diameter to extra large balls"+
			 " nearly a foot in diameter used in training exercises"+
			 " to increase the skill of players.")

session.add(item4)
session.commit()

item5 = Item(user_id=1, category_id=1, name="Shinguards", 
	         picture="http://assets.academy.com/mgen/00/10269800.jpg",
			 description="A shin guard or shin pad is a piece of "+
			 "equipment worn on the front of a players shin to protect"+
			 " them from injury. Modern day shin guards are"+
			 " made of many differing synthetic materials." )

session.add(item5)
session.commit()

item6 = Item(user_id=1, category_id=4, name="Frisbee", 
			 picture="https://upload.wikimedia.org/wikipedia/commons"+
			 "/f/fa/Frisbee_090719.jpg",
			 description="The term Frisbee, is often used to generically"+
			 " describe all flying discs. A flying disc is a disc-shaped"+
			 " gliding toy or sporting item that is generally plastic"+
			 " and roughly 20 to 25 centimetres (8 to 10 in) in"+
			 " diameter with a lip,[1] used recreationally and"+
			 " competitively for throwing and catching.")

session.add(item6)
session.commit()

item7 = Item(user_id=1, category_id=3, name="Baseball bat", 
		     picture="http://wiki.urbandead.com/images/2/20/Baseball_bat.png",
			 description="A baseball bat is a smooth wooden or metal club"+
			 " used in the sport of baseball to hit the ball after it is"+
			 " thrown by the pitcher. By regulation it may be no more"+
			 " than 2.75 inches in diameter at the thickest part and"+
			 " no more than 42 inches (1,100 mm) long.")

session.add(item7)
session.commit()

item8 = Item(user_id=1, category_id=1, name="Jersey", 
		     picture="https://pbs.twimg.com/media/BkI2S7PCUAAtOcG.jpg",
			 description="A jersey as used in sport is a shirt worn by"+
			 " a member of a team, typically depicting the athlete's"+
			 " name and team number as well as the logotype of the team"+
			 " or corporate sponsor.")

session.add(item8)
session.commit()

item9 = Item(user_id=1, category_id=1, name="Soccer Cleats",
			 picture="http://houseofsoccercleats.com/wp-content/uploads/"+
			 "2013/03/Nike-Mercurial-Vapor-Superfly-III-FG-Boots-"+
			 "Barcelona-Soccer-Cleats-Zebra.jpg",
			 description="Cleats or studs are protrusions on the sole of a"+
			 " shoe,"+
			 " or on an external attachment to a shoe, that provide additional"+
			 " traction on a soft or slippery surface. In American English"+
			 " the term cleats is used synecdochically to refer to shoes"+
			 " featuring such protrusions.")

session.add(item9)
session.commit()

print("Added catalogs and their items!!!")

