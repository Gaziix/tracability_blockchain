const db = require('../config/database');

const getProductsIdAndName = (callback) => {
  const query = `SELECT id, product_name FROM products`;
  db.query(query, callback);
};

// Fonction pour récupérer le nom du produit basé sur l'ID
async function getProductNameById(productId) {
  const query = 'SELECT product_name FROM products WHERE id = ?';
  return new Promise((resolve, reject) => {
    db.query(query, [productId], (error, results) => {
      if (error) {
        console.error("Erreur lors de l'exécution de la requête SQL:", error);
        reject('Inconnu');
      }

      // Vérifier si la réponse est un tableau avec des résultats
      if (Array.isArray(results) && results.length > 0) {
        console.log("Nom du produit:", results[0].product_name);
        resolve(results[0].product_name || 'Inconnu');
      } else {
        console.error("Aucun produit trouvé pour l'ID:", productId);
        resolve('Inconnu');
      }
    });
  });
}

module.exports = {
    getProductsIdAndName,getProductNameById
};
