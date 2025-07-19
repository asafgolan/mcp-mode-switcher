#!/usr/bin/env node

/**
 * Standalone Roo-Code Mode Reader
 * Simple script to read current mode from VS Code/Windsurf global state database
 * No VS Code dependencies - uses direct SQLite access
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration
const CONFIG = {
    windsurfDbPath: path.join(os.homedir(), 'Library/Application Support/Windsurf/User/globalStorage/state.vscdb'),
    vscodeDbPath: path.join(os.homedir(), 'Library/Application Support/Code/User/globalStorage/state.vscdb'),
    rooExtensionKey: 'RooVeterinaryInc.roo-cline'
};

console.log('🎯 Standalone Roo-Code Mode Reader');
console.log('==================================');

/**
 * Check if sqlite3 is available
 */
function checkSqlite() {
    try {
        execSync('which sqlite3', { stdio: 'ignore' });
        return true;
    } catch (e) {
        console.log('❌ sqlite3 not found. Install with: brew install sqlite');
        return false;
    }
}

/**
 * Read current mode from VS Code/Windsurf global state database
 */
function getCurrentMode(dbPath, dbName) {
    if (!fs.existsSync(dbPath)) {
        console.log(`❌ ${dbName} database not found: ${dbPath}`);
        return null;
    }

    console.log(`🔍 Reading from ${dbName} database...`);
    
    try {
        // Query for Roo-Code extension data
        const query = `SELECT value FROM ItemTable WHERE key = '${CONFIG.rooExtensionKey}';`;
        const result = execSync(`sqlite3 "${dbPath}" "${query}"`, { encoding: 'utf8' }).trim();
        
        if (!result) {
            console.log(`❌ No Roo-Code data found in ${dbName} database`);
            return null;
        }

        // Parse JSON and extract mode
        try {
            const data = JSON.parse(result);
            const mode = data.mode || 'default';
            
            console.log(`✅ Found Roo-Code data in ${dbName}:`);
            console.log(`   🎯 Current Mode: ${mode}`);
            
            // Show additional useful info
            if (data.apiProvider) {
                console.log(`   🤖 API Provider: ${data.apiProvider}`);
            }
            if (data.customModes && data.customModes.length > 0) {
                console.log(`   📋 Custom Modes: ${data.customModes.length} available`);
            }
            
            return mode;
            
        } catch (e) {
            console.log(`❌ Error parsing Roo-Code data: ${e.message}`);
            console.log(`📄 Raw data: ${result.substring(0, 200)}...`);
            return null;
        }
        
    } catch (e) {
        console.log(`❌ Error querying ${dbName} database: ${e.message}`);
        return null;
    }
}

/**
 * Main function
 */
function main() {
    // Check prerequisites
    if (!checkSqlite()) {
        process.exit(1);
    }

    console.log('🔍 Searching for Roo-Code mode...\n');

    // Try Windsurf first (most likely to have current data)
    let mode = getCurrentMode(CONFIG.windsurfDbPath, 'Windsurf');
    
    // Fallback to VS Code if Windsurf doesn't have data
    if (!mode) {
        console.log('\n🔄 Trying VS Code database...\n');
        mode = getCurrentMode(CONFIG.vscodeDbPath, 'VS Code');
    }

    // Summary
    console.log('\n' + '='.repeat(50));
    if (mode) {
        console.log(`🎯 CURRENT ROO-CODE MODE: ${mode.toUpperCase()}`);
        console.log(`📅 Retrieved at: ${new Date().toLocaleString()}`);
        
        // Exit with mode as return code (useful for scripting)
        console.log(`\n💡 Use in scripts: MODE=$(node roo-mode-reader.js 2>/dev/null | grep "CURRENT ROO-CODE MODE" | cut -d: -f2 | xargs)`);
        
    } else {
        console.log('❌ Could not determine current Roo-Code mode');
        console.log('💡 Make sure Roo-Code extension is installed and has been used at least once');
        process.exit(1);
    }
}

// Handle command line arguments
if (process.argv.includes('--help') || process.argv.includes('-h')) {
    console.log(`
Usage: node roo-mode-reader.js [options]

Options:
  --help, -h     Show this help message
  --json         Output mode as JSON
  --quiet        Only output the mode name

Examples:
  node roo-mode-reader.js                    # Full output
  node roo-mode-reader.js --json             # JSON output
  node roo-mode-reader.js --quiet            # Just the mode name
  MODE=$(node roo-mode-reader.js --quiet)    # Use in scripts
`);
    process.exit(0);
}

// Handle JSON output
if (process.argv.includes('--json')) {
    if (!checkSqlite()) process.exit(1);
    
    let mode = getCurrentMode(CONFIG.windsurfDbPath, 'Windsurf');
    if (!mode) mode = getCurrentMode(CONFIG.vscodeDbPath, 'VS Code');
    
    console.log(JSON.stringify({
        mode: mode || null,
        timestamp: new Date().toISOString(),
        source: mode ? 'global-state' : 'not-found'
    }));
    process.exit(mode ? 0 : 1);
}

// Handle quiet output
if (process.argv.includes('--quiet')) {
    if (!checkSqlite()) process.exit(1);
    
    let mode = getCurrentMode(CONFIG.windsurfDbPath, 'Windsurf');
    if (!mode) mode = getCurrentMode(CONFIG.vscodeDbPath, 'VS Code');
    
    if (mode) {
        console.log(mode);
        process.exit(0);
    } else {
        process.exit(1);
    }
}

// Run main function
main();
