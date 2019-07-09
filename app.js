const express = require('express');
const nunjucks = require('nunjucks');
const Posts = require('./models/posts');
const database = require('./utils/database');

const app = express()
const port = 3000

nunjucks.configure('views', {
    autoescape: false,
    express: app
});

app.use(express.static('public'));

app.get('/', (req, res) => {
    Posts.random()
        .then(item => {
            res.render('index.njk', {item: item});
        });    
});

app.get('/attachments/:itemId', (req, res) => {
    Posts.attachments(req.params.itemId)
        .then(html => {
            res.send(html);
        });    
});

app.use('/', (req, res) => {
    res.status(404).render('404.njk');
});

database.connect(() => {
    app.listen(port, () => {
        console.log(`Listening on port ${port}`);
    });
});

