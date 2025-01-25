const express = require('express');
const { isAuthenticated } = require('../middlewares/authMiddleware');
const axios = require('axios'); // Assure-toi d'installer axios via npm
const router = express.Router();

router.get('/', isAuthenticated, async (req, res) => {
  try {
    // Récupérer les données depuis l'API blockchain
    const response = await axios.get('http://127.0.0.1:8080/blockchain');
    const blockchainData = response.data;

    // Extraire les acteurs depuis les données de la blockchain
    const actors = blockchainData.actors;

    // Passer les acteurs et les informations supplémentaires à la vue
    const user = req.session.user;
    res.render('display_actors', { 
      user, 
      pageTitle: "Affichage des acteurs",
      actors: actors // Passer les acteurs à la vue
    });
  } catch (error) {
    console.error("Erreur lors de la récupération des données blockchain:", error);
    res.status(500).send("Erreur interne du serveur.");
  }
});

module.exports = router;
