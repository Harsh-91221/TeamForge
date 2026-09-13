require('dotenv').config({ path: '.env' });
const mongoose = require('mongoose');

async function testMongoDB() {
  console.log('=== MongoDB Connection Test ===\n');
  
  // Connect to MongoDB
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log('✓ Connected to MongoDB successfully');
    console.log(`  Database: teamforge`);
    console.log(`  Server: ${mongoose.connection.host}\n`);
    
    // Get all collections
    const collections = await mongoose.connection.db.listCollections().toArray();
    console.log('=== Collections ===');
    collections.forEach(col => {
      console.log(`  - ${col.name}`);
    });
    console.log(`\nTotal collections: ${collections.length}\n`);
    
    // Show document count for each collection
    console.log('=== Document Counts ===');
    for (const col of collections) {
      try {
        const count = await mongoose.connection.db.collection(col.name).countDocuments();
        console.log(`  ${col.name}: ${count} documents`);
        
        // Show first document from each collection (if any)
        if (count > 0 && count <= 5) {
          const sample = await mongoose.connection.db.collection(col.name).findOne();
          console.log(`    Sample: ${JSON.stringify(sample, null, 2).split('\n').slice(0, 8).join('\n    ')}`);
        }
      } catch (err) {
        console.log(`  ${col.name}: Error reading - ${err.message}`);
      }
    }
    
    // Example: Show members if they exist
    console.log('\n=== Recent Members (if any) ===');
    try {
      const members = await mongoose.connection.db.collection('members').find({}, { projection: { userId: 1, workspaceId: 1, role: 1, joinedAt: 1 } }).limit(10).toArray();
      if (members.length === 0) {
        console.log('  No members found');
      } else {
        members.forEach(m => console.log(`  - ${m.userId} in ${m.workspaceId} as ${m.role}`));
      }
    } catch (err) {
      console.log(`  Error: ${err.message}`);
    }
    
    // Example: Show workspaces if they exist
    console.log('\n=== Workspaces (if any) ===');
    try {
      const workspaces = await mongoose.connection.db.collection('workspaces').find({}, { projection: { _id: 1, name: 1, inviteCode: 1, owner: 1 } }).limit(5).toArray();
      if (workspaces.length === 0) {
        console.log('  No workspaces found');
      } else {
        workspaces.forEach(w => console.log(`  - ${w.name} (${w.inviteCode}) owned by ${w.owner}`));
      }
    } catch (err) {
      console.log(`  Error: ${err.message}`);
    }
    
  } catch (err) {
    console.error('✗ Failed to connect to MongoDB:', err.message);
  } finally {
    await mongoose.connection.close();
    console.log('\n✓ Connection closed');
  }
}

testMongoDB();
