const mongodb = require("mongodb");

let db;

exports.connect = callback => {
    const mongoClient = new mongodb.MongoClient(new mongodb.Server('localhost', 27017));
    mongoClient.connect((err, client) => {
        if (err) {
            console.log(err);
        }
        else {
            db = client.db('vk-mousemath');
            callback();
        }
    });
};

exports.db = () => db;

