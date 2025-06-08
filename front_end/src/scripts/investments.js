import axios from 'axios';

const API_URL = 'http://0.0.0.0:8002/api/v1';

export const investments = {
    async getTradingByName(name) {
      try {
        const response = await axios.get(`${API_URL}/top_cryptos`);
        const data = response.data;
        console.log("Trading data", data)

        if (data[name]) {
          return data[name];
        } else {
          console.warn('Crypto not found:', name);
          return null;
        }
      } catch (error) {
        console.error('Error getting crypto prices:', error.response?.data || error);
        throw error;
      }
    },

    async getPriceByName(name){
      try {
        const response = await axios.get(`${API_URL}/monthly_prices`)
        const data = response.data
        console.log("Fetched monthly prices:", data)
        if (data.hasOwnProperty(name)) {
          return data[name]
        } else {
          console.warn(`No data found for crypto: ${name}`)
          return null
        }
      } catch (error) {
        console.error('Error fetching crypto prices:', error.response?.data || error)
        throw error
      }
    }
}