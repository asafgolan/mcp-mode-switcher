#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Config
const dbPath = path.join(os.homedir(), 'Library/Application Support/Windsurf/User/globalStorage/state.vscdb');
const rooKey = 'RooVeterinaryInc.roo-cline';
let lastMode = null;

// Get current mode from DB
function getCurrentMode() {
    try {
        const query = `SELECT value FROM ItemTable WHERE key = '${rooKey}';`;
        const result = execSync(`sqlite3 "${dbPath}" "${query}"`, { encoding: 'utf8' }).trim();
        if (!result) return null;
        const data = JSON.parse(result);
        return data.mode || 'default';
    } catch (e) {
        return null;
    }
}

// Check for changes
function checkMode() {
    const currentMode = getCurrentMode();
    if (currentMode && lastMode && currentMode !== lastMode) {
        console.log(`🎉 MODE CHANGED: ${lastMode} → ${currentMode}`);
        console.log('👋 Hello World! Mode has changed!');
        
        // Execute MCP mode switcher Python script
        try {
            const scriptPath = path.join(__dirname, 'mode-managers', 'mcp', 'mcp.py');
            console.log(`🔧 Executing MCP switcher: python3 ${scriptPath} ${currentMode}`);
            
            const result = execSync(`python3 "${scriptPath}" "${currentMode}"`, { 
                encoding: 'utf8',
                timeout: 30000 // 30 second timeout
            });
            
            console.log('✅ MCP switch completed:', result.trim());
        } catch (error) {
            console.log('❌ MCP switch failed:', error.message);
            // Continue execution even if MCP switch fails
        }
    }
    lastMode = currentMode;
}

// Watch database file for changes
if (fs.existsSync(dbPath)) {
    console.log('👀 Watching for mode changes...');
    fs.watchFile(dbPath, { interval: 1000 }, checkMode);
    checkMode(); // Initial check
    
    // Keep process alive
    process.on('SIGINT', () => {
        console.log('\n👋 Stopping watcher...');
        fs.unwatchFile(dbPath);
        process.exit(0);
    });
    
    console.log('✅ Watcher started. Press Ctrl+C to stop.');
} else {
    console.log('❌ Database not found:', dbPath);
}
