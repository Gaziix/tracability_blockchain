const db = require('../config/database');

const getCompaniesIdAndName = (callback) => {
  const query = `SELECT id, company_name FROM companies`;
  db.query(query, callback);
};

module.exports = {
    getCompaniesIdAndName,
};
