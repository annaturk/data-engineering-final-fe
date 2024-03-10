const Pool = require('pg').Pool

const express = require('express');
const app = express();

const pool = new Pool({
    user: 'postgres',
    host: '34.171.12.201',
    database: 'chicago_business_intelligence',
    password: 'root'
});

const bodyParser = require('body-parser');

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }));

pool.connect((err, client, release) => {
    if (err) {
        return console.error(
            'Error acquiring client', err.stack)
    }
    client.query('SELECT NOW()', (err, result) => {
        release()
        if (err) {
            return console.error(
                'Error executing query', err.stack)
        }
        console.log("Connected to Database !")
    })
})



app.get('/cbidata', (req, res, next) => {
    console.log("CCVI DATA :");
    pool.query('Select * from ccvi_data')
        .then(ccviData => {
            console.log(ccviData);
            res.send(ccviData.rows);
        })
})

// Use port 8080 by default, unless configured differently in Google Cloud
const port = process.env.PORT || 8080;
app.listen(port, () => {
   console.log(`App is running at: http://localhost:${port}`);
});