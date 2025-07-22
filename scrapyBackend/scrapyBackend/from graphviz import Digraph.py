from graphviz import Digraph

# Define ERD using Graphviz
erd = Digraph(format='png')
erd.attr(rankdir='LR', size='8,5')

# Entities with attributes
entities = {
    'User': ['user_id (PK)', 'username', 'email', 'password', 'profile_pic'],
    'ScrapPost': ['scrap_id (PK)', 'user_id (FK)', 'title', 'description', 'image', 'price', 'is_auction', 'category', 'timestamp'],
    'CraftyPost': ['crafty_id (PK)', 'user_id (FK)', 'title', 'description', 'image', 'price', 'timestamp'],
    'Auction': ['auction_id (PK)', 'scrap_id (FK)', 'start_time', 'end_time', 'starting_bid', 'highest_bid'],
    'Bid': ['bid_id (PK)', 'auction_id (FK)', 'user_id (FK)', 'bid_amount', 'timestamp'],
    'Chat': ['chat_id (PK)', 'sender_id (FK)', 'receiver_id (FK)', 'message', 'timestamp'],
    'SavedPost': ['save_id (PK)', 'user_id (FK)', 'post_type', 'post_id', 'timestamp'],
    'Report': ['report_id (PK)', 'user_id (FK)', 'post_type', 'post_id', 'reason', 'timestamp'],
    'Notification': ['notification_id (PK)', 'user_id (FK)', 'message', 'timestamp', 'is_read']
}

# Add nodes
for entity, attributes in entities.items():
    label = f"{entity}|" + "|".join(attributes)
    erd.node(entity, shape='record', label="{" + label + "}")

# Relationships
relationships = [
    ('User', 'ScrapPost'),
    ('User', 'CraftyPost'),
    ('ScrapPost', 'Auction'),
    ('Auction', 'Bid'),
    ('User', 'Bid'),
    ('User', 'Chat'),
    ('Chat', 'User'),
    ('User', 'SavedPost'),
    ('User', 'Report'),
    ('User', 'Notification')
]

# Add edges
for source, target in relationships:
    erd.edge(source, target)

erd.render('/mnt/data/scrap_platform_erd', view=False)
'/mnt/data/scrap_platform_erd.png'
