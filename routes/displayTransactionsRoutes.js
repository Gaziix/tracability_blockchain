const express = require('express');
const { isAuthenticated } = require('../middlewares/authMiddleware');
const { getProductNameById } = require('../models/productsModels');  // Assure-toi d'importer correctement

const axios = require('axios'); // Assure-toi d'installer axios via npm
const router = express.Router();

router.get('/', isAuthenticated, async (req, res) => {
  try {
    // Récupérer les données depuis l'API blockchain (ou autre source)
    const response = await axios.get('http://127.0.0.1:8080/blockchain');
    const blockchainData = response.data;

    // Extraire les transactions depuis les blocs
    const transactions = blockchainData.chain.flatMap(block => block.transactions);

    // Filtrer les transactions où le destinataire ou la source est le nom de l'entreprise de l'utilisateur
    const filteredTransactions = transactions.filter(transaction => 
      transaction.destination_id === req.session.user.company_name || 
      transaction.source_id === req.session.user.company_name
    );

    // Ajouter le nom du produit à chaque transaction
    const transactionsWithProductNames = await Promise.all(filteredTransactions.map(async (transaction) => {
      const productName = await getProductNameById(transaction.product.id);  // Récupérer le nom du produit
      return {
        ...transaction,
        productName: productName  // Ajouter le nom du produit
      };
    }));

    // Passer les transactions filtrées et les informations supplémentaires à la vue
    const user = req.session.user;
    res.render('display_transactions', { 
      user, 
      pageTitle: "Affichage des transactions",
      transactions: transactionsWithProductNames // Passer les transactions avec le nom du produit à la vue
    });
  } catch (error) {
    console.error("Erreur lors de la récupération des données blockchain:", error);
    res.status(500).send("Erreur interne du serveur.");
  }
});

module.exports = router;
