/**
 * SafeSense Kids Guardian - Background Service Worker
 * Handles extension lifecycle and background tasks
 */

console.log('SafeSense Kids Guardian background service started');

// Listen for extension installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Extension installed');
    
    // Set default settings
    chrome.storage.local.set({
      'safesense_enabled': true,
      'safesense_auto_analyze': true,
      'safesense_show_warnings': true,
      'safesense_installed_at': Date.now()
    });

    // Open welcome page (optional - comment out if annoying)
    try {
      chrome.tabs.create({
        url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' // Demo video
      });
    } catch (error) {
      console.warn('Could not open welcome page:', error);
    }
  } else if (details.reason === 'update') {
    console.log('Extension updated');
  }
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Message received:', request);

  if (request.action === 'analyzeVideo') {
    // Handle video analysis request
    sendResponse({ status: 'analyzing' });
  } else if (request.action === 'getSettings') {
    // Return extension settings
    chrome.storage.local.get(null, (settings) => {
      sendResponse(settings);
    });
    return true; // Keep channel open for async response
  } else if (request.action === 'updateSettings') {
    // Update settings
    chrome.storage.local.set(request.settings, () => {
      sendResponse({ status: 'updated' });
    });
    return true;
  }
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  console.log('Extension icon clicked on tab:', tab.id);
});

// Clean up old cache periodically (every 24 hours)
try {
  chrome.alarms.create('cleanCache', { periodInMinutes: 60 * 24 });
  console.log('Cache cleanup alarm created');
} catch (error) {
  console.warn('Could not create alarm:', error);
}

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'cleanCache') {
    console.log('Cleaning old cache...');
    
    chrome.storage.local.get(null, (items) => {
      const now = Date.now();
      const keysToRemove = [];
      
      for (const [key, value] of Object.entries(items)) {
        if (key.startsWith('safesense_') && value.timestamp) {
          const age = now - value.timestamp;
          if (age > 7 * 24 * 60 * 60 * 1000) { // Older than 7 days
            keysToRemove.push(key);
          }
        }
      }
      
      if (keysToRemove.length > 0) {
        chrome.storage.local.remove(keysToRemove);
        console.log(`Removed ${keysToRemove.length} old cache entries`);
      }
    });
  }
});
