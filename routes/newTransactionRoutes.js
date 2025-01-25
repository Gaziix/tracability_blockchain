const express = require('express');
const { isAuthenticated } = require('../middlewares/authMiddleware');
const path = require('path');
const axios = require('axios');

const router = express.Router();
const productsModel = require('../models/productsModels'); // Import du modèle de produits
const companiesModel = require('../models/companiesModels'); // Import du modèle des entreprises

// Route pour la page de transaction
router.get('/', isAuthenticated, (req, res) => {
  const user = req.session.user;

  // Récupérer les produits depuis la base de données
  productsModel.getProductsIdAndName((err, products) => {
    if (err) {
      return res.status(500).send("Erreur lors de la récupération des produits");
    }

    // Récupérer les entreprises depuis la base de données
    companiesModel.getCompaniesIdAndName((err, companies) => {
      if (err) {
        return res.status(500).send("Erreur lors de la récupération des entreprises");
      }

      // Rendre la vue en passant les produits et les entreprises
      res.render('new_transaction', { 
        user, 
        pageTitle: "Gestion des transactions",
        products, // Liste des produits
        companies // Liste des entreprises
      });
    });
  });
});

// Route POST pour traiter la soumission du formulaire
router.post('/', isAuthenticated, (req, res) => {
  const { productId, serialNumber, buyerId } = req.body;


  // Définir l'URL du serveur Python pour envoyer les données
  const serverUrl = 'http://127.0.0.1:8080/input';

  // Préparer les paramètres de la requête
  const params = new URLSearchParams();
  params.append('dest_id', buyerId);  // ID de l'acheteur (Entreprise)
  params.append('product_id', productId);  // ID du produit
  params.append('product_sn', serialNumber);  // Numéro de série du produit
  console.log(params)
  // Envoi des données à l'API Python
  axios.get(serverUrl, { params })
    .then(response => {
      console.log("Réponse du serveur Python:", response.data);
      res.send('Transaction envoyée avec succès');
    })
    .catch(error => {
      console.error("Erreur lors de l'envoi de la transaction:", error);
      res.status(500).send('Erreur lors de l\'envoi de la transaction');
    });
});

module.exports = router;
