import dns from 'node:dns';
import mongoose from 'mongoose'; // Import mongoose library
import { config } from './app.config'; // Import configuration from app.config

const connectDatabase = async () => {
  // Define an asynchronous function to connect to the database
  try {
    if (config.MONGO_DNS_SERVERS) {
      dns.setServers(config.MONGO_DNS_SERVERS.split(',').map((server) => server.trim()));
    }
    await mongoose.connect(config.MONGO_URI); // Attempt to connect to the MongoDB database using the URI from the config
    console.log('Connected to Mongo Database'); // Log success message if connection is successful
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error('Error connecting to Mongo database:', message);
    throw error;
  }
};

export default connectDatabase; // Export the connectDatabase function as the default export

