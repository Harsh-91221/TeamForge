require('dotenv').config({ path: './backend/.env' });
const mongoose = require('mongoose');

async function demoMongoDB() {
  console.log('=== MongoDB Demo for TeamForge ===\n');
  
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log('✓ Connected to MongoDB Atlas\n');
    
    const db = mongoose.connection.db;
    
    // List all collections
    const collections = await db.listCollections().toArray();
    console.log('📊 Collections in database:');
    collections.forEach(col => console.log(`   - ${col.name}`));
    
    // Show counts and samples for each collection
    console.log('\n📋 Document Details:\n');
    for (const col of collections) {
      const count = await db.collection(col.name).countDocuments();
      console.log(`─── ${col.name} (${count} documents) ───`);
      
      if (count > 0) {
        const sample = await db.collection(col.name).find({}, { projection: { _id: 1, ...getSampleProjection(col.name) } }).limit(2).toArray();
        sample.forEach(doc => {
          console.log(`   ID: ${doc._id.toString().substring(0, 24)}...`);
          console.log(`   Data: ${JSON.stringify(doc).substring(0, 200)}...`);
        });
      }
      console.log('');
    }
    
    console.log('\n🔧 To DELETE all documents securely, run this in mongosh:\n');
    console.log(`use teamforge;`);
    console.log(`db.getCollectionNames().forEach(c => db[c].deleteMany({}));`);
    console.log('\nOr use the Node.js script below:');
    
  } catch (err) {
    console.error('✗ Error:', err.message);
  } finally {
    await mongoose.connection.close();
  }
}

function getSampleProjection(collectionName) {
  const projections = {
    users: { name: 1, email: 1 },
    workspaces: { name: 1, inviteCode: 1, owner: 1 },
    members: { userId: 1, workspaceId: 1, role: 1 },
    projects: { name: 1, description: 1 },
    tasks: { title: 1, status: 1 },
    accounts: { provider: 1, providerId: 1 }
  };
  return projections[collectionName] || {};
}

demoMongoDB();
