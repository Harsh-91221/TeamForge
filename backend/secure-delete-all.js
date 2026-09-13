/**
 * Securely delete all documents from all collections in a MongoDB database
 * Usage: node secure-delete-all.js "mongodb://connection-string"
 * 
 * This script:
 * 1. Connects to MongoDB
 * 2. Lists all collections
 * 3. Shows document counts before deletion
 * 4. Deletes all documents from each collection
 * 5. Verifies deletion
 */

require('dotenv').config({ path: './backend/.env' });
const { MongoClient, ObjectId } = require('mongodb');

const MONGO_URI = process.env.MONGO_URI;
const DB_NAME = 'teamforge'; // or use process.argv[2] for custom DB

async function secureDeleteAllDocuments() {
  const client = new MongoClient(MONGO_URI);
  
  try {
    await client.connect();
    console.log('✓ Connected to MongoDB\n');
    
    const db = client.db(DB_NAME);
    const collections = await db.listCollections().toArray();
    
    console.log(`📊 Found ${collections.length} collections in ${DB_NAME} database:\n`);
    
    let totalDocsDeleted = 0;
    
    for (const coll of collections) {
      const collectionName = coll.name;
      const collection = db.collection(collectionName);
      
      // Get count before deletion
      const docCount = await collection.countDocuments();
      console.log(`─── ${collectionName}: ${docCount} documents ───`);
      
      if (docCount > 0) {
        // Delete all documents
        const result = await collection.deleteMany({});
        console.log(`   ✓ Deleted ${result.deletedCount} documents\n`);
        totalDocsDeleted += result.deletedCount;
      } else {
        console.log('   (empty)\n');
      }
    }
    
    console.log(`═══════════════════════════════════════`);
    console.log(`✓ COMPLETED: Deleted ${totalDocsDeleted} total documents from ${collections.length} collections\n`);
    
    // Verify deletion
    console.log('🔍 Verification - checking remaining documents:\n');
    for (const coll of collections) {
      const count = await db.collection(coll.name).countDocuments();
      console.log(`  ${coll.name}: ${count} documents remaining`);
    }
    
  } catch (error) {
    console.error('✗ Error:', error.message);
  } finally {
    await client.close();
    console.log('\n✓ Connection closed');
  }
}

// Run the function
secureDeleteAllDocuments();
