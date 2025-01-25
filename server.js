const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const path = require('path');
const authRoutes = require('./routes/authRoutes');
const menuRoutes = require('./routes/menuRoutes');
const displayTransactionsRoutes = require('./routes/displayTransactionsRoutes');
const newTransactionRoutes = require('./routes/newTransactionRoutes');
const displayActorsRoutes = require('./routes/displayActorsRoutes');
const forwardProductRoutes = require('./routes/forwardProductRoutes');

const app = express();
const PORT = 3000;

// Configurer EJS comme moteur de templates
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware global
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Configuration de la session
app.use(
  session({
    secret: 'votre_clé_secrète', // Remplacez par une clé unique et sécurisée
    resave: false, // Ne sauvegarde pas la session si elle n'a pas été modifiée
    saveUninitialized: true, // Sauvegarde une session non initialisée
    cookie: { secure: false }, // Passez à true si vous utilisez HTTPS
  })
);

// Servir les fichiers statiques
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.use('/auth', authRoutes);
app.use('/menu', menuRoutes);
app.use('/display-transactions', displayTransactionsRoutes);
app.use('/new-transaction', newTransactionRoutes);
app.use('/display-actors', displayActorsRoutes);
app.use('/forward-product', forwardProductRoutes);


// Rediriger la racine (/) vers /auth/login
app.get('/', (req, res) => {
    res.redirect('/auth/login');
});

// Serveur
app.listen(PORT, () => {
  console.log(`Serveur démarré sur http://localhost:${PORT}`);
});
