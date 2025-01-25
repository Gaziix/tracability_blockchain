const mysql = require('mysql2');

const db = mysql.createConnection({
  host: '127.0.0.1',
  user: 'ddb_user',
  password: 'Azerty123*',
  database: 'pharmaceutique',
});

db.connect((err) => {
  if (err) {
    console.error('Erreur de connexion à la base de données :', err);
    process.exit(1);
  }
  console.log('Connecté à la base de données MariaDB.');
});

module.exports = db;
