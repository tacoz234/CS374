// Ben Berry

// Wine Database

// db.getCollectionNames();

// [
//   'suppliers',
//   'products',
//   'order_lines',
//   'purchase_orders',
//   'supplies'
// ]

// db.suppliers.find();

// {
//     _id: 21,
//     name: 'Deliwines',
//     address: '240, Avenue of the Americas',
//     city: 'New York',
//     status: 20
//   },

// db.products.find();

// {
//     _id: 119,
//     name: 'Chateau Miraval, Cotes de Provence Rose, 2015',
//     type: 'rose',
//     available_quantity: 126
//   },

// db.order_lines.find();

// {
//     _id: ObjectId('691cbba9744d7708f589b03d'),
//     product_order: 1511,
//     product: 212,
//     quantity: 2
//   },

// db.purchase_orders.find();

// { _id: 1511, date: '2015-03-24', supplier: 37 },

// db.supplies.find();

// {
//     _id: ObjectId('691cbba859e980dbc489b03d'),
//     supplier: 21,
//     product: 119,
//     purchase_price: 15.99,
//     delivery_period: 1
//   },

// db.order_lines.find({ product: 212 })

// [
//   {
//     _id: ObjectId('691cbba9744d7708f589b03d'),
//     product_order: 1511,
//     product: 212,
//     quantity: 2
//   },
//   {
//     _id: ObjectId('691cbba9744d7708f589b055'),
//     product_order: 1538,
//     product: 212,
//     quantity: 15
//   },
//   {
//     _id: ObjectId('691cbba9744d7708f589b059'),
//     product_order: 1577,
//     product: 212,
//     quantity: 6
//   }
// ]

// db.products.find({ available_quantity: { $lt: 20 } })

// [
//   {
//     _id: 185,
//     name: 'Chateau Petrus, 1975',
//     type: 'red',
//     available_quantity: 5
//   },
//   {
//     _id: 219,
//     name: 'Marques de Caceres, Rioja Crianza, 2010 ',
//     type: 'red',
//     available_quantity: 0
//   },
//   {
//     _id: 265,
//     name: 'Chateau Sociando-Mallet, Haut-Medoc, 1998',
//     type: 'red',
//     available_quantity: 17
//   },
//   {
//     _id: 331,
//     name: 'Chateau La Commanderie, Lalande-de-Pomerol, 1998',
//     type: 'red',
//     available_quantity: 3
//   },
//   {
//     _id: 494,
//     name: 'Veuve-Cliquot, Brut, 2012',
//     type: 'sparkling',
//     available_quantity: 1
//   },
//   {
//     _id: 523,
//     name: 'Chateau Andron Blanquet, Saint Estephe, 1979',
//     type: 'red',
//     available_quantity: 13
//   },
//   {
//     _id: 783,
//     name: "Clos D'Opleeuw, Chardonnay, 2012",
//     type: 'white',
//     available_quantity: 8
//   }
// ]

// db.suppliers.find({city: "New York"})

// [
//   {
//     _id: 21,
//     name: 'Deliwines',
//     address: '240, Avenue of the Americas',
//     city: 'New York',
//     status: 20
//   }
// ]

// db.products.find({type: { "$in": ["rose", "white"] }, available_quantity: {"$gt": 50}});

// [
//   {
//     _id: 119,
//     name: 'Chateau Miraval, Cotes de Provence Rose, 2015',
//     type: 'rose',
//     available_quantity: 126
//   },
//   {
//     _id: 289,
//     name: 'Chateau Saint Estève de Neri, 2015',
//     type: 'rose',
//     available_quantity: 126
//   },
//   {
//     _id: 300,
//     name: 'Chateau des Rontets, Chardonnay, Birbettes',
//     type: 'white',
//     available_quantity: 64
//   },
//   {
//     _id: 632,
//     name: 'Meneghetti, Chardonnay, 2010',
//     type: 'white',
//     available_quantity: 83
//   },
//   {
//     _id: 668,
//     name: 'Gallo Family Vineyards, Grenache, 2014',
//     type: 'rose',
//     available_quantity: 95
//   },
//   {
//     _id: 899,
//     name: 'Trimbach, Riesling, 1989',
//     type: 'white',
//     available_quantity: 142
//   }
// ]

// Restaurant Database

// db.getCollectionNames();

// [ 'restaurants', 'people' ]

// db.restaurants.find();

// {
//     _id: 1,
//     address: '30 Greyhound Road Hammersmith',
//     location: 'London',
//     name: '@ Thai Restaurant',
//     outcode: 'W6',
//     postcode: '8NX',
//     rating: 4.5,
//     type_of_food: 'Thai'
//   },

// db.people.find();

// {
//     _id: ObjectId('691e40a4599bdbe3e389b03d'),
//     name: 'Seppe',
//     restaurant_id: 23,
//     rating: 5
//   },

// db.restaurants.find({ location: "London" }, { name: 1, rating: 1 }).sort({ rating: -1 });

// [
//   { _id: 55, name: 'Alasia', rating: 'Not yet rated' },
//   {
//     _id: 101,
//     name: 'Anokha Indian Bar & Restaurant',
//     rating: 'Not yet rated'
//   },
//   { _id: 15, name: 'Aarthi', rating: 6 },
//   { _id: 165, name: 'Bamboo Box', rating: 5.5 },
//   { _id: 174, name: 'Barbican Tandoori', rating: 5.5 },
//   { _id: 23, name: 'Absolute Caribbean', rating: 5 },
//   { _id: 24, name: 'Absolute Caribbean', rating: 5 },
//   { _id: 31, name: 'Admiral Pizza', rating: 5 },
//   { _id: 40, name: 'AK Chicken Food', rating: 5 },
//   { _id: 59, name: 'Alfa Pizza & Chicken', rating: 5 },
//   { _id: 67, name: 'All Nations Dalston', rating: 5 },
//   { _id: 137, name: 'Azeri Cuisine', rating: 5 },
//   { _id: 138, name: 'Azka Turkish Meze', rating: 5 },
//   { _id: 166, name: 'Bamboo Garden', rating: 5 },
//   { _id: 186, name: 'Bedouin Lounge Grill & Mezza Bar', rating: 5 },
//   { _id: 199, name: 'Bengal Berties', rating: 5 },
//   { _id: 200, name: 'Bengal Brasserie', rating: 5 },
//   { _id: 202, name: 'Bengal Lancer', rating: 5 },
//   { _id: 1, name: '@ Thai Restaurant', rating: 4.5 },
//   { _id: 35, name: 'Ai Sushi', rating: 4.5 }
// ]

// db.people.find({ rating: 5 }, { _id: 0, name: 1, restaurant_id: 1 }).sort({ name: 1 });

// [
//   { name: 'Bart', restaurant_id: 136 },
//   { name: 'Bart', restaurant_id: 143 },
//   { name: 'Bart', restaurant_id: 21 },
//   { name: 'Bart', restaurant_id: 91 },
//   { name: 'Bart', restaurant_id: 131 },
//   { name: 'Bart', restaurant_id: 40 },
//   { name: 'Bart', restaurant_id: 141 },
//   { name: 'Bart', restaurant_id: 53 },
//   { name: 'Bart', restaurant_id: 9 },
//   { name: 'Bart', restaurant_id: 55 },
//   { name: 'Bart', restaurant_id: 92 },
//   { name: 'Estefania', restaurant_id: 176 },
//   { name: 'Jan', restaurant_id: 57 },
//   { name: 'Jan', restaurant_id: 131 },
//   { name: 'Jan', restaurant_id: 134 },
//   { name: 'Jan', restaurant_id: 125 },
//   { name: 'Jan', restaurant_id: 115 },
//   { name: 'Jan', restaurant_id: 49 },
//   { name: 'Jan', restaurant_id: 67 },
//   { name: 'Jan', restaurant_id: 27 }
// ]

// db.restaurants.find({ type_of_food: { $regex: "Thai", $options: "i" } }, { _id: 0, name: 1, address: 1 });

// [
//   {
//     address: '30 Greyhound Road Hammersmith',
//     name: '@ Thai Restaurant'
//   },
//   { address: '235-241 High Street', name: "Anna's Thai Restaurant" },
//   { address: '235-241 High Street', name: "Anna's Thai Restaurant" },
//   { address: '21 Market Road', name: 'Asian Box' },
//   { address: '18 Fortess Road', name: 'Baan Thai' },
//   { address: 'Unit 23 55-59 Weir Road', name: 'Bamboo Baboom' },
//   { address: 'Unit 23 55-59 Weir Road', name: 'Bamboo Baboom' },
//   { address: '194 Shoreditch High Street', name: 'Bamboo Box' },
//   { address: '1 Ecclesall Road', name: 'Ban Thai' },
//   { address: '55 Southgate Elland', name: 'Bang Thai Dee' },
//   { address: '21 Rose Street', name: 'Bhan Thai' }
// ]