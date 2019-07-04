const express = require('express');
const nunjucks = require('nunjucks');
const database = require('./utils/database');

const app = express()
const port = 3000

nunjucks.configure('views', {
    autoescape: true,
    express: app
});

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.render('index.njk');
});

app.use('/', (req, res) => {
    res.status(404).render('404.njk');
});

database.connect(() => {
    app.listen(port, () => {
        console.log(`Listening on port ${port}`);
    });
});

