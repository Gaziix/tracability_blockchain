const express = require('express');
const { isAuthenticated } = require('../middlewares/authMiddleware');
const axios = require('axios');
const companiesModel = require('../models/companiesModels'); // Import du modèle des entreprises

const router = express.Router();

// Route pour afficher la page forward-product
router.get('/', isAuthenticated, async (req, res) => {
  const user = req.session.user;
  const companyName = user.company_name;

  try {
    // Récupérer les données de la blockchain
    const response = await axios.get('http://127.0.0.1:8080/blockchain');
    const blockchainData = response.data;

    // Filtrer les transactions où l'entreprise du transporteur est impliquée comme destination
    const receivedProducts = [];
    blockchainData.chain.forEach(block => {
      block.transactions.forEach(transaction => {
        if (transaction.destination_id === companyName) {
          receivedProducts.push({
            productId: transaction.product.id,
            serialNumber: transaction.product.serial_number,
            productName: `Produit ${transaction.product.id}` // Adaptez selon votre modèle de produit
          });
        }
      });
    });

    // Récupérer la liste des entreprises
    companiesModel.getCompaniesIdAndName((err, companies) => {
      if (err) {
        return res.status(500).send("Erreur lors de la récupération des entreprises");
      }

      // Rendre la vue avec les produits reçus et les entreprises
      res.render('forward_product', { 
        user, 
        pageTitle: "Transfert de produits", 
        products: receivedProducts,
        companies: companies // Passer les entreprises à la vue
      });
    });

  } catch (error) {
    console.error("Erreur lors de la récupération des produits depuis la blockchain:", error);
    return res.status(500).send("Erreur lors de la récupération des produits");
  }
});

// Route POST pour traiter le transfert de produit
router.post('/', isAuthenticated, (req, res) => {
  const { productId, serialNumber, destinationId } = req.body;

  // Définir l'URL du serveur Python pour envoyer les données
  const serverUrl = 'http://127.0.0.1:8080/input';

  // Préparer les paramètres de la requête
  const params = new URLSearchParams();
  params.append('dest_id', destinationId);  // ID du destinataire (Entreprise)
  params.append('product_id', productId);  // ID du produit
  params.append('product_sn', serialNumber);  // Numéro de série du produit

  // Envoi des données à l'API Python
  axios.get(serverUrl, { params })
    .then(response => {
      console.log("Réponse du serveur Python:", response.data);
      res.send('Transfert de produit effectué avec succès');
    })
    .catch(error => {
      console.error("Erreur lors de l'envoi du transfert de produit:", error);
      res.status(500).send('Erreur lors du transfert de produit');
    });
});

module.exports = router;
