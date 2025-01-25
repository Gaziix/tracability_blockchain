const express = require('express');
const authController = require('../controllers/authController');

const router = express.Router();

// Route pour afficher la page de connexion
router.get('/login', (req, res) => {
  res.render('auth/login', { 
    pageTitle: "Connexion" // Titre personnalisé pour cette page
  });
});

// Route pour traiter le formulaire de connexion
router.post('/login', authController.login);

// Route pour la déconnexion
router.get('/logout', authController.logout);

module.exports = router;
