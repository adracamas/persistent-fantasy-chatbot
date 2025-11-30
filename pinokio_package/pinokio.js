// Pinokio Launcher UI for Fantasy Chatbot
const menu = [
  {
    title: "🚀 Quick Start",
    run: "install.js",
    params: { setup: true }
  },
  {
    title: "💻 Start CLI Chatbot", 
    run: "start_cli.js",
    description: "Launch command-line interface with memory commands"
  },
  {
    title: "🌐 Start Web Interface",
    run: "start_web.js", 
    description: "Launch beautiful browser-based interface"
  },
  {
    title: "🧠 Memory Management",
    run: "manage_memory.js",
    description: "Browse and manage stored memories"
  },
  {
    title: "📊 System Statistics",
    run: "view_stats.js",
    description: "Check AI model and memory system status"
  },
  {
    title: "🔧 Configuration",
    run: "configure.js",
    description: "Adjust AI parameters and settings"
  }
];

// Dynamic status check
const running = await kernel.local("start_cli.js");
const webRunning = await kernel.local("start_web.js");

const statusItems = [];

if (!running) {
  statusItems.push({
    type: "status",
    message: "🤖 Ready to start your fantasy adventure!",
    color: "green"
  });
} else {
  statusItems.push({
    type: "status", 
    message: "✅ CLI chatbot is running",
    color: "green"
  });
}

if (webRunning) {
  statusItems.push({
    type: "status",
    message: "🌐 Web interface is running", 
    color: "blue"
  });
}

// Hardware detection info
const hasGPU = await kernel.exec("nvidia-smi");
if (hasGPU) {
  statusItems.push({
    type: "info",
    message: "🖥️ GPU detected - Optimal performance available",
    color: "green"
  });
} else {
  statusItems.push({
    type: "warning", 
    message: "⚠️ CPU-only mode - Performance may be slower",
    color: "yellow"
  });
}

// Add status to menu
menu.unshift({
  title: "📊 System Status",
  items: statusItems
});

// Additional menu items
menu.push({
  title: "📖 Documentation",
  items: [
    {
      type: "link",
      title: "How to Use",
      url: "https://github.com/your-username/fantasy-chatbot/blob/main/README.md"
    },
    {
      type: "link", 
      title: "God-Like Control Guide",
      url: "https://github.com/your-username/fantasy-chatbot/blob/main/GOD_MODE_GUIDE.md"
    },
    {
      type: "link",
      title: "Troubleshooting",
      url: "https://github.com/your-username/fantasy-chatbot/blob/main/TROUBLESHOOTING.md"
    }
  ]
});

return menu;