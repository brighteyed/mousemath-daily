const db = require('../utils/database').db;
const ObjectId = require('../utils/database').ObjectId;

function unixTimestampToString(t) {
    const dt = new Date(t * 1000);
    return dt.toLocaleString();
}

class Post {
    constructor(text, date, url, id) {
        this.id = id;
        this.text = text;
        this.date = date;
        this.url = url;
    }

    static random() {
        return db().collection('posts').aggregate([{ $sample: { size: 1}}]).toArray()
            .then(items => {
                return new Post(items[0].text, items[0].date, items[0].url, items[0]._id);
            })
            .catch(err => {
                console.log(err);
            });
    }

    static attachments(itemId) {
        return db().collection('posts').findOne({_id: new ObjectId(itemId)})
            .then(item => {
                if (item.photos) {
                    let photos = "";
                    item.photos.forEach(photo => {
                        if (photo.y) {
                            photos += `<img src="${photo.y.url}"/>`;
                        } else if (photo.x) {
                            photos += `<img src="${photo.x.url}"/>`;
                        } else if (photo.m) {
                            photos += `<img src="${photo.m.url}"/>`;
                        }                    
                    });

                    return `<div class="photos">${photos}</div>`;
                }

                return "";
            })
            .catch(err => {
                console.log(err);
            });
    }
}    

module.exports = Post;