/**
 * N8N Config Error Fix - Client-side JavaScript
 * Run this in browser console to fix config-related errors
 */

(function() {
    console.log('🔧 N8N Config Error Fix Starting...');
    
    // 1. Clear localStorage
    try {
        const keysToRemove = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && (key.includes('n8n') || key.includes('workflow') || key.includes('config'))) {
                keysToRemove.push(key);
            }
        }
        
        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
            console.log(`✅ Removed localStorage key: ${key}`);
        });
    } catch (e) {
        console.error('❌ Error clearing localStorage:', e);
    }
    
    // 2. Clear sessionStorage
    try {
        const sessionKeysToRemove = [];
        for (let i = 0; i < sessionStorage.length; i++) {
            const key = sessionStorage.key(i);
            if (key && (key.includes('n8n') || key.includes('workflow') || key.includes('config'))) {
                sessionKeysToRemove.push(key);
            }
        }
        
        sessionKeysToRemove.forEach(key => {
            sessionStorage.removeItem(key);
            console.log(`✅ Removed sessionStorage key: ${key}`);
        });
    } catch (e) {
        console.error('❌ Error clearing sessionStorage:', e);
    }
    
    // 3. Clear IndexedDB
    try {
        if ('indexedDB' in window) {
            indexedDB.databases().then(databases => {
                databases.forEach(db => {
                    if (db.name && (db.name.includes('n8n') || db.name.includes('workflow'))) {
                        const deleteReq = indexedDB.deleteDatabase(db.name);
                        deleteReq.onsuccess = () => console.log(`✅ Deleted IndexedDB: ${db.name}`);
                        deleteReq.onerror = () => console.error(`❌ Error deleting IndexedDB: ${db.name}`);
                    }
                });
            });
        }
    } catch (e) {
        console.error('❌ Error clearing IndexedDB:', e);
    }
    
    // 4. Reset global config objects
    try {
        if (typeof window !== 'undefined') {
            // Common N8N global variables that might be corrupted
            const globalVarsToReset = ['n8nConfig', 'workflowConfig', 'nodeConfig', 'appConfig'];
            
            globalVarsToReset.forEach(varName => {
                if (window[varName]) {
                    delete window[varName];
                    console.log(`✅ Reset global variable: ${varName}`);
                }
            });
        }
    } catch (e) {
        console.error('❌ Error resetting global variables:', e);
    }
    
    // 5. Force reload with cache bypass
    console.log('🔄 Reloading page with cache bypass...');
    setTimeout(() => {
        window.location.reload(true);
    }, 1000);
    
    console.log('✅ N8N Config Error Fix Completed!');
    console.log('📋 If error persists:');
    console.log('   1. Clear all browser data for this domain');
    console.log('   2. Try incognito/private mode');
    console.log('   3. Update N8N to latest version');
    console.log('   4. Check browser console for specific errors');
})();