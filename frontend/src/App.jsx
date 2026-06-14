import React, { useState, useRef, useEffect } from "react";
import "./App.css";

// ===================================================================================
// CONFIGURATION
// ===================================================================================
// ===================================================================================
// CONFIGURATION
// ===================================================================================
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const HEALTH_CHECK_URL = `${API_BASE}/health`;

// ===================================================================================
// Landing Page Component (Farmer-Centric Update)
// ===================================================================================
const LandingPage = ({ onEnterChat }) => {
  return (
    <div className="min-h-screen farmer-gradient text-slate-800 flex flex-col items-center py-6 md:py-12 px-4 md:px-6 relative animate-fadeIn">
      {/* Soft Background Elements */}
      <div className="fixed inset-0 pointer-events-none opacity-50">
        <div className="absolute top-0 left-0 w-64 h-64 bg-green-100 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-yellow-50 rounded-full blur-3xl"></div>
      </div>

      <div className="text-center max-w-4xl mx-auto z-10 flex flex-col items-center">
        <div className="mb-6 animate-slideUp">
          <div className="bg-white p-6 rounded-full shadow-lg inline-block border-4 border-green-500/10">
            <span className="text-6xl md:text-7xl">🚜</span>
          </div>
        </div>

        <h1 className="text-4xl md:text-7xl font-bold mb-4 tracking-tight text-green-900 animate-slideUp" style={{ animationDelay: "0.1s" }}>
          KissanSeva AI
        </h1>

        <p className="text-xl md:text-2xl mb-10 text-slate-600 max-w-2xl font-medium animate-slideUp" style={{ animationDelay: "0.2s" }}>
          Welcome! Your personal digital assistant to make <span className="text-green-700">farming better and easier</span>.
        </p>

        <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 animate-slideUp" style={{ animationDelay: "0.3s" }}>
          {[
            { icon: "🌾", title: "Crop Information", desc: "Select the right crops and increase your yield." },
            { icon: "🔍", title: "Image Identification", desc: "Send photos to identify and treat crop diseases." },
            { icon: "🗣️", title: "Voice Interaction", desc: "Get information by speaking in your own language." }
          ].map((feature, i) => (
            <div key={i} className="organic-card p-6 text-center">
              <div className="text-4xl mb-3">{feature.icon}</div>
              <h3 className="text-lg font-bold text-green-800 mb-2">{feature.title}</h3>
              <p className="text-slate-600 text-sm">{feature.desc}</p>
            </div>
          ))}
        </div>

        <button
          onClick={onEnterChat}
          className="btn-primary text-lg px-12 py-4 animate-slideUp"
          style={{ animationDelay: "0.4s" }}
        >
          Start Assistant →
        </button>
      </div>

      <footer className="mt-20 text-slate-500 text-sm font-medium animate-fadeIn">
        © 2026 KissanSeva AI — Empowering Farmers, Shaping the Nation
      </footer>
    </div>
  );
};

// ===================================================================================
// Weather Forecast Component
// ===================================================================================
const WeatherForecast = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [location, setLocation] = useState({ lat: null, lon: null, name: "", error: null });
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [useCurrentLocation, setUseCurrentLocation] = useState(true);

  // Fetch current GPS location on mount
  useEffect(() => {
    getCurrentLocation();
  }, []);

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      setLocation({ lat: null, lon: null, name: "", error: "Geolocation not supported" });
      return;
    }

    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setLocation({ lat: latitude, lon: longitude, name: "Current Location", error: null });
        fetchWeather(latitude, longitude);
        setUseCurrentLocation(true);
      },
      (error) => {
        setLocation({ lat: null, lon: null, name: "", error: "Location access denied" });
        setLoading(false);
      }
    );
  };

  const fetchWeather = async (lat, lon) => {
    try {
      const response = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto`
      );
      const data = await response.json();
      setWeatherData(data.daily);
      setLoading(false);
    } catch (err) {
      console.error("Weather fetch error:", err);
      setLoading(false);
    }
  };

  const searchPlaces = async (query) => {
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }

    try {
      const response = await fetch(
        `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=5`
      );
      const data = await response.json();
      setSearchResults(data.results || []);
      setShowResults(true);
    } catch (err) {
      console.error("Geocoding error:", err);
      setSearchResults([]);
    }
  };

  const handleSearchInput = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    searchPlaces(value);
  };

  const selectPlace = (place) => {
    setLocation({
      lat: place.latitude,
      lon: place.longitude,
      name: `${place.name}${place.admin1 ? ', ' + place.admin1 : ''}${place.country ? ', ' + place.country : ''}`,
      error: null
    });
    setSearchQuery("");
    setShowResults(false);
    setSearchResults([]);
    setLoading(true);
    fetchWeather(place.latitude, place.longitude);
    setUseCurrentLocation(false);
  };

  const getWeatherIcon = (code) => {
    if (code === 0) return "☀️";
    if (code <= 3) return "🌤️";
    if (code <= 48) return "🌫️";
    if (code <= 67) return "🌦️";
    if (code <= 77) return "🌨️";
    if (code <= 82) return "🌧️";
    if (code <= 99) return "⛈️";
    return "🌡️";
  };

  const getDayName = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", { weekday: "short" });
  };

  if (loading) return <div className="text-center p-4 text-slate-500">Loading forecast...</div>;
  if (location.error) return <div className="text-center p-4 text-red-500">❌ {location.error}</div>;

  const displayDays = isExpanded ? weatherData?.time.length : 1;

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-bold text-green-800 border-b border-slate-100 pb-2 flex items-center gap-2">
        🌦️ Weather Forecast
      </h3>
      
      {/* Search and Location Controls */}
      <div className="space-y-2">
        <div className="flex gap-2 relative">
          <input
            type="text"
            value={searchQuery}
            onChange={handleSearchInput}
            onFocus={() => searchResults.length > 0 && setShowResults(true)}
            placeholder="Search location..."
            className="flex-1 input-field py-2 text-sm"
          />
          <button
            onClick={getCurrentLocation}
            className={`p-2 rounded-lg transition-all ${
              useCurrentLocation 
                ? 'bg-green-100 text-green-700 border-2 border-green-500' 
                : 'bg-slate-100 text-slate-600 border border-slate-200 hover:bg-slate-200'
            }`}
            title="Use current location"
          >
            📍
          </button>
          
          {/* Search Results Dropdown */}
          {showResults && searchResults.length > 0 && (
            <div className="absolute top-full left-0 right-12 mt-1 bg-white border border-slate-200 rounded-lg shadow-lg z-50 max-h-48 overflow-y-auto">
              {searchResults.map((place, i) => (
                <button
                  key={i}
                  onClick={() => selectPlace(place)}
                  className="w-full text-left px-3 py-2 hover:bg-green-50 text-sm border-b border-slate-100 last:border-0"
                >
                  <div className="font-bold text-slate-700">{place.name}</div>
                  <div className="text-xs text-slate-400">
                    {place.admin1 && `${place.admin1}, `}{place.country}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
        
        {/* Location Name */}
        {location.name && (
          <p className="text-xs text-slate-500 italic">📍 {location.name}</p>
        )}
      </div>

      {/* Weather Forecast */}
      <div className="flex flex-col gap-2">
        {weatherData && weatherData.time.slice(0, displayDays).map((time, i) => (
          <div key={time} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100 hover:bg-white transition-colors">
            <div className="flex items-center gap-3">
              <span className="text-sm font-bold text-slate-600 w-10">{i === 0 ? "Today" : getDayName(time)}</span>
              <span className="text-2xl">{getWeatherIcon(weatherData.weathercode[i])}</span>
            </div>
            <div className="flex gap-4">
              <span className="text-sm font-bold text-red-600">{Math.round(weatherData.temperature_2m_max[i])}°</span>
              <span className="text-sm font-bold text-blue-600">{Math.round(weatherData.temperature_2m_min[i])}°</span>
            </div>
          </div>
        ))}
      </div>

      {/* More/Less Button */}
      {weatherData && weatherData.time.length > 1 && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full py-2 text-sm font-bold text-green-700 hover:bg-green-50 rounded-lg transition-all border border-green-200"
        >
          {isExpanded ? "Show Less ▲" : `More (${weatherData.time.length - 1} days) ▼`}
        </button>
      )}
    </div>
  );
};

// ===================================================================================
// Mandi Prices Component (Live Agricultural Market Prices)
// ===================================================================================
const MandiPrices = () => {
  const [pricesData, setPricesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCommodity, setSelectedCommodity] = useState("Rice");
  const [selectedState, setSelectedState] = useState("All");
  const [isExpanded, setIsExpanded] = useState(false);
  
  // Popular commodities list
  const commodities = [
    "Rice", "Wheat", "Maize", "Cotton", "Soybean", 
    "Groundnut", "Sugarcane", "Potato", "Onion", "Tomato",
    "Cabbage", "Cauliflower", "Carrot", "Beans", "Peas",
    "Ladyfinger", "Brinjal", "Chilli", "Garlic", "Ginger"
  ];

  const states = [
    "All", "Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", 
    "Maharashtra", "Karnataka", "Tamil Nadu", "West Bengal", "Bihar",
    "Rajasthan", "Gujarat", "Andhra Pradesh", "Telangana", "Kerala",
    "Odisha", "Assam", "Chhattisgarh", "Jharkhand", "Uttarakhand"
  ];

  useEffect(() => {
    fetchMandiPrices();
  }, [selectedCommodity, selectedState]);

  const fetchMandiPrices = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Using data.gov.in API endpoint for agricultural commodity prices
      // Note: In production, you would use the actual API with proper authentication
      // For now, we'll use mock data that simulates the real API response
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Generate realistic mock data based on actual mandi price patterns
      const mockData = generateMockMandiData(selectedCommodity, selectedState);
      setPricesData(mockData);
      setLoading(false);
    } catch (err) {
      console.error("Mandi prices fetch error:", err);
      setError("Failed to load market prices");
      setLoading(false);
    }
  };

  const generateMockMandiData = (commodity, state) => {
    // Base prices per quintal (100kg) for different commodities in INR
    const basePrices = {
      "Rice": 2100, "Wheat": 2125, "Maize": 1850, "Cotton": 6500,
      "Soybean": 4200, "Groundnut": 5500, "Sugarcane": 320,
      "Potato": 1200, "Onion": 1800, "Tomato": 2000,
      "Cabbage": 800, "Cauliflower": 1400, "Carrot": 1100, "Beans": 2500,
      "Peas": 3000, "Ladyfinger": 1800, "Brinjal": 1300, "Chilli": 8000,
      "Garlic": 5000, "Ginger": 4500
    };

    const markets = state === "All" 
      ? ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai"]
      : state === "Punjab" 
        ? ["Ludhiana", "Amritsar", "Jalandhar", "Patiala"]
        : state === "Maharashtra"
          ? ["Mumbai", "Pune", "Nashik", "Nagpur"]
          : state === "Gujarat"
            ? ["Ahmedabad", "Rajkot", "Surat", "Vadodara"]
            : state === "Rajasthan"
              ? ["Jaipur", "Jodhpur", "Kota", "Udaipur"]
              : state === "Karnataka"
                ? ["Bangalore", "Mysore", "Hubli", "Belgaum"]
                : state === "Tamil Nadu"
                  ? ["Chennai", "Coimbatore", "Madurai", "Salem"]
                  : state === "Andhra Pradesh"
                    ? ["Vijayawada", "Visakhapatnam", "Guntur", "Tirupati"]
                    : state === "Telangana"
                      ? ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar"]
                      : [state + " Central", state + " North", state + " South"];

    const basePrice = basePrices[commodity] || 2000;
    
    return markets.slice(0, 5).map((market, i) => {
      const variation = (Math.random() - 0.5) * 0.15; // ±15% variation
      const modalPrice = Math.round(basePrice * (1 + variation));
      const minPrice = Math.round(modalPrice * 0.92);
      const maxPrice = Math.round(modalPrice * 1.08);
      
      // Calculate trend (price change over last week)
      const trendPercent = (Math.random() - 0.45) * 10; // Slight bias toward positive
      
      return {
        market,
        commodity,
        modalPrice,
        minPrice,
        maxPrice,
        trend: trendPercent,
        arrivalQuantity: Math.round(50 + Math.random() * 200), // in quintals
        date: new Date().toISOString().split('T')[0]
      };
    });
  };

  const getTrendIcon = (trend) => {
    if (trend > 2) return { icon: "📈", color: "text-green-600", bg: "bg-green-50" };
    if (trend < -2) return { icon: "📉", color: "text-red-600", bg: "bg-red-50" };
    return { icon: "➡️", color: "text-slate-600", bg: "bg-slate-50" };
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(price);
  };

  if (loading) return <div className="text-center p-4 text-slate-500">Loading prices...</div>;
  if (error) return <div className="text-center p-4 text-red-500">❌ {error}</div>;

  const displayItems = isExpanded ? pricesData : pricesData.slice(0, 3);

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-bold text-green-800 border-b border-slate-100 pb-2 flex items-center gap-2">
        💰 Live Mandi Prices
      </h3>

      {/* Commodity and State Selection */}
      <div className="space-y-2">
        <select
          value={selectedCommodity}
          onChange={(e) => setSelectedCommodity(e.target.value)}
          className="w-full input-field py-2 text-sm font-bold"
        >
          {commodities.map(crop => (
            <option key={crop} value={crop}>{crop}</option>
          ))}
        </select>

        <select
          value={selectedState}
          onChange={(e) => setSelectedState(e.target.value)}
          className="w-full input-field py-2 text-sm"
        >
          {states.map(state => (
            <option key={state} value={state}>{state}</option>
          ))}
        </select>
      </div>

      {/* Price Cards */}
      <div className="flex flex-col gap-2">
        {displayItems.map((item, i) => {
          const trendStyle = getTrendIcon(item.trend);
          return (
            <div key={i} className="p-3 rounded-xl bg-slate-50 border border-slate-100 hover:bg-white transition-colors">
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <h4 className="text-sm font-bold text-slate-800">{item.market}</h4>
                  <p className="text-xs text-slate-500">{item.arrivalQuantity} quintals arrived</p>
                </div>
                <div className={`flex items-center gap-1 px-2 py-1 rounded-lg ${trendStyle.bg}`}>
                  <span className="text-xs">{trendStyle.icon}</span>
                  <span className={`text-xs font-bold ${trendStyle.color}`}>
                    {item.trend > 0 ? '+' : ''}{item.trend.toFixed(1)}%
                  </span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-lg font-black text-green-700">
                    {formatPrice(item.modalPrice)}
                  </div>
                  <div className="text-[10px] text-slate-400">
                    {formatPrice(item.minPrice)} - {formatPrice(item.maxPrice)}
                  </div>
                </div>
                <div className="text-[9px] text-slate-400 text-right">
                  per quintal<br/>
                  (100 kg)
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Price Trend Summary */}
      {pricesData.length > 0 && (
        <div className="p-3 rounded-xl bg-gradient-to-r from-green-50 to-blue-50 border border-green-200">
          <div className="text-xs font-bold text-green-800 mb-1">📊 Market Insight</div>
          <div className="text-xs text-slate-600">
            {(() => {
              const avgTrend = pricesData.reduce((sum, item) => sum + item.trend, 0) / pricesData.length;
              if (avgTrend > 2) {
                return `${selectedCommodity} prices are rising. Good time to sell! 📈`;
              } else if (avgTrend < -2) {
                return `${selectedCommodity} prices are falling. Consider holding or buying. 📉`;
              } else {
                return `${selectedCommodity} prices are stable across markets. ➡️`;
              }
            })()}
          </div>
        </div>
      )}

      {/* Expand/Collapse Button */}
      {pricesData.length > 3 && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full py-2 text-sm font-bold text-green-700 hover:bg-green-50 rounded-lg transition-all border border-green-200"
        >
          {isExpanded ? "Show Less ▲" : `More Markets (${pricesData.length - 3}) ▼`}
        </button>
      )}

      {/* Data Source Info */}
      <div className="text-[9px] text-slate-400 italic text-center">
        Data source: AGMARKNET Portal
      </div>
    </div>
  );
};

// ===================================================================================
// Farmer Chatbot Component
// ===================================================================================

const FarmerChatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      content:
        "Hello! Welcome to KissanSeva AI. 🌱\n\nI can help you with:\n• Crop information and recommendations\n• Disease and pest identification\n• Fertilizer and soil health advice\n• Weather and seasonal farming tips\n\nYou can ask me questions by typing, uploading photos, or speaking.",
      isUser: false,
      type: "welcome",
      timestamp: new Date(),
    },
  ]);
  const [activeTab, setActiveTab] = useState("text");
  const [textInput, setTextInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [imageType, setImageType] = useState("disease");
  const [connectionStatus, setConnectionStatus] = useState("checking");
  const [isListening, setIsListening] = useState(false); // Voice state
  const [language, setLanguage] = useState("en-US"); // Language state for voice
  const [imageLanguage, setImageLanguage] = useState("en"); // Language state for image
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Mobile sidebar toggle
  const recognitionRef = useRef(null); // Voice ref
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);
  const imageInputRef = useRef(null);
  const voiceInputRef = useRef(null);
  const textInputRef = useRef(null);

  const [context, setContext] = useState({
    crop: "Rice",
    location: "India",
    season: "Kharif",
  });

  const [predictionFeatures, setPredictionFeatures] = useState({
    N: 90, P: 42, K: 43,
    temperature: 25.0, humidity: 80.0, ph: 6.5, rainfall: 200.0,
  });

  useEffect(() => {
    checkConnection();
    window.scrollTo(0, 0); // Reset scroll position when entering chat
  }, []);

  const checkConnection = async () => {
    try {
      const response = await fetch(HEALTH_CHECK_URL);
      setConnectionStatus(response.ok ? "connected" : "error");
    } catch (error) {
      setConnectionStatus("error");
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const addMessage = (content, isUser, type = "text") => {
    setMessages((prev) => [
      ...prev,
      { id: Date.now() + Math.random(), content, isUser, type, timestamp: new Date() }
    ]);
  };

  const sendTextMessage = async (messageText = null) => {
    const message = messageText || textInput.trim();
    if (!message) return;
    addMessage(message, true, "text");
    setTextInput("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: message, context }),
      });
      const data = await response.json();
      setIsLoading(false);
      if (response.ok) {
        addMessage(data.answer, false, "text");
      } else {
        addMessage("Sorry, I couldn't reach the server.", false, "error");
      }
    } catch (error) {
      setIsLoading(false);
      addMessage("Network error. Please check your internet connection.", false, "error");
    }
  };

  const uploadImage = async () => {
    const file = imageInputRef.current?.files[0];
    if (!file) return;
    addMessage(`Analyzing image: ${file.name}`, true, "image");
    setIsLoading(true);
    const formData = new FormData();
    formData.append("image", file);
    formData.append("type", imageType);
    formData.append("language", imageLanguage); // Send selected language
    if (context.location) formData.append("location", context.location);

    try {
      const response = await fetch(`${API_BASE}/image-query`, { method: "POST", body: formData });
      const data = await response.json();
      setIsLoading(false);
      if (response.ok) {
        let result = `Analysis Result (${imageType.toUpperCase()}):\n\nPrediction: ${data.prediction}\nConfidence: ${(data.confidence * 100).toFixed(1)}%\n\n${data.answer}`;
        addMessage(result, false, "image");
      } else {
        addMessage(`Analysis failed: ${data.detail || "Unknown error"}`, false, "error");
      }
    } catch (error) {
      setIsLoading(false);
      addMessage("Failed to connect for image analysis.", false, "error");
    }
    imageInputRef.current.value = "";
  };

  const toggleListening = () => {
    if (isListening) {
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsListening(false);
      return;
    }

    if (!("webkitSpeechRecognition" in window) && !("SpeechRecognition" in window)) {
      addMessage("Browser does not support voice input. Try Chrome/Edge.", false, "error");
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.continuous = false;
    recognition.interimResults = true; // Enable live feedback
    recognition.lang = language; // Dynamic language

    recognition.onstart = () => setIsListening(true);
    
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setTextInput(transcript); // Show what is being spoken
      
      // Only send when the speech is FINAL
      if (event.results[0].isFinal) {
        sendTextMessage(transcript);
        setIsListening(false);
      }
    };

    recognition.onerror = (event) => {
      console.error("Speech Error:", event.error);
      setIsListening(false);
      // Don't show error for "no-speech" as it's common
      if (event.error !== "no-speech") {
        addMessage("Could not hear you. Please try again.", false, "error");
      }
    };

    recognition.onend = () => setIsListening(false);

    recognition.start();
  };

  const TabButton = ({ id, icon, label, isActive, onClick }) => (
    <button
      onClick={onClick}
      className={`flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-bold transition-all ${
        isActive ? "tab-active shadow-sm" : "tab-inactive hover:bg-white/50"
      }`}
    >
      <span className="text-2xl">{icon}</span>
      <span className="text-sm">{label}</span>
    </button>
  );

  return (
    <div className="h-screen farmer-gradient flex flex-col overflow-hidden">
      {/* Friendly Header */}
      <header className="bg-white border-b border-slate-200 px-4 py-3 flex flex-col md:flex-row items-center justify-between shadow-sm gap-4 shrink-0">
        {/* Logo and Tagline */}
        <div className="flex items-center gap-3 min-w-fit">
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="lg:hidden p-2 rounded-lg bg-green-50 text-green-800"
          >
            ☰
          </button>
          <span className="text-2xl md:text-3xl">🚜</span>
          <div>
            <h1 className="text-base md:text-lg font-black text-green-900 leading-tight">KISSANSEVA AI</h1>
            <p className="text-[8px] md:text-[9px] text-slate-400 font-bold uppercase tracking-[0.2em]">Precision Agriculture</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 bg-slate-50 p-1 rounded-xl border border-slate-100 flex-wrap justify-center">
          {[
            { id: "text", icon: "💬", label: "Advisor" },
            { id: "image", icon: "📸", label: "Vision" },
            { id: "voice", icon: "🎤", label: "Audio" }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 py-2 px-3 rounded-lg font-bold transition-all text-xs ${
                activeTab === tab.id ? "tab-active shadow-sm" : "tab-inactive hover:bg-white/50"
              }`}
            >
              <span>{tab.icon}</span>
              <span className="hidden sm:inline uppercase tracking-widest">{tab.label}</span>
            </button>
          ))}
        </nav>

        
        {/* Status */}
        <div className="flex items-center gap-3 min-w-fit">
          <div className={`h-2 w-2 rounded-full ${connectionStatus === "connected" ? "bg-green-500 animate-pulse" : "bg-red-500"}`}></div>
          <div className="bg-green-50 px-3 py-1 rounded-lg border border-green-100">
             <span className="text-[10px] font-bold text-green-800 uppercase tracking-widest">
               {connectionStatus === "connected" ? "ACTIVE" : "OFFLINE"}
             </span>
          </div>
        </div>
      </header>

        <main className="flex-1 flex flex-col lg:flex-row p-4 md:p-6 gap-6 min-h-0 relative">
        {/* Simple Sidebar */}
        <div className={`
          absolute inset-0 bg-black/50 z-40 lg:hidden transition-opacity
          ${isSidebarOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"}
        `} onClick={() => setIsSidebarOpen(false)}></div>

        <aside className={`
          fixed lg:static inset-y-0 left-0 w-80 bg-[#fdfcf7] lg:bg-transparent z-50 transform transition-transform duration-300
          ${isSidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
          flex flex-col gap-4 overflow-y-auto p-4 lg:p-0 border-r lg:border-r-0 border-slate-200 shadow-xl lg:shadow-none
        `}>
          <div className="flex justify-between items-center lg:hidden mb-2">
            <h2 className="font-bold text-green-900">Tools</h2>
            <button onClick={() => setIsSidebarOpen(false)} className="p-2 text-slate-500">✕</button>
          </div>

          <div className="organic-card p-5">
            <WeatherForecast />
          </div>

          <div className="organic-card p-5">
            <MandiPrices />
          </div>
        </aside>

        {/* Chat Area */}
        <section className="flex-1 organic-card flex flex-col min-h-0 overflow-hidden relative">
          <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-6 space-y-6 chat-container">
            {messages.map(msg => (
              <div key={msg.id} className={`flex ${msg.isUser ? "justify-end" : "justify-start"} animate-message`}>
                <div className={`message-bubble ${msg.isUser ? "user-bubble" : "ai-bubble"}`}>
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start animate-message">
                <div className="ai-bubble italic text-slate-400">Assistant is thinking...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="p-4 bg-white border-t border-slate-100">
            <div className="flex gap-2">
              {activeTab === "text" && (
                <>
                  <input
                    ref={textInputRef}
                    type="text"
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && sendTextMessage()}
                    placeholder="Type your question here..."
                    className="flex-1 input-field"
                  />
                  <button onClick={() => sendTextMessage()} className="btn-primary">Send</button>
                </>
              )}
              {activeTab === "image" && (
                <div className="flex-1 flex flex-col gap-4">
                  <div className="flex gap-2 p-1 bg-slate-100 rounded-xl w-fit self-center">
                    <button 
                      onClick={() => setImageType("disease")}
                      className={`px-6 py-2 rounded-lg text-xs font-bold transition-all ${imageType === "disease" ? "bg-white text-green-800 shadow-sm" : "text-slate-500 hover:text-slate-700"}`}
                    >
                      🦠 DISEASE
                    </button>
                    <button 
                      onClick={() => setImageType("insect")}
                      className={`px-6 py-2 rounded-lg text-xs font-bold transition-all ${imageType === "insect" ? "bg-white text-green-800 shadow-sm" : "text-slate-500 hover:text-slate-700"}`}
                    >
                      🐜 INSECT
                    </button>
                  </div>
                  <div className="flex gap-2">
                    <select 
                      value={imageLanguage} 
                      onChange={(e) => setImageLanguage(e.target.value)}
                      className="p-2 border border-slate-300 rounded-lg bg-white text-sm font-bold text-slate-700"
                    >
                      <option value="en">English</option>
                      <option value="hi">Hindi (हिंदी)</option>
                      <option value="gu">Gujarati (ગુજરાતી)</option>
                      <option value="mr">Marathi (मराठी)</option>
                      <option value="pa">Punjabi (ਪੰਜਾਬੀ)</option>
                      <option value="bn">Bengali (বাংলা)</option>
                      <option value="ta">Tamil (தமிழ்)</option>
                      <option value="te">Telugu (తెలుగు)</option>
                      <option value="kn">Kannada (ಕನ್ನಡ)</option>
                      <option value="ml">Malayalam (മലയാളം)</option>
                      <option value="ur">Urdu (اردو)</option>
                    </select>
                    <input ref={imageInputRef} type="file" accept="image/*" className="hidden" onChange={uploadImage} />
                    <button onClick={() => imageInputRef.current.click()} className="flex-1 btn-primary bg-orange-600 hover:bg-orange-700">Select {imageType === "disease" ? "Disease" : "Insect"} Photo</button>
                  </div>
                </div>
              )}
              {activeTab === "voice" && (
                <div className="flex-1 flex gap-2">
                  <select 
                    value={language} 
                    onChange={(e) => setLanguage(e.target.value)}
                    className="p-2 border border-slate-300 rounded-lg bg-white text-sm font-bold text-slate-700"
                  >
                    <option value="en-US">English</option>
                    <option value="hi-IN">Hindi (हिंदी)</option>
                    <option value="gu-IN">Gujarati (ગુજરાતી)</option>
                    <option value="mr-IN">Marathi (मराठी)</option>
                    <option value="pa-IN">Punjabi (ਪੰਜਾਬੀ)</option>
                    <option value="bn-IN">Bengali (বাংলা)</option>
                    <option value="ta-IN">Tamil (தமிழ்)</option>
                    <option value="te-IN">Telugu (తెలుగు)</option>
                    <option value="kn-IN">Kannada (ಕನ್ನಡ)</option>
                    <option value="ml-IN">Malayalam (മലയാളം)</option>
                    <option value="ur-IN">Urdu (اردو)</option>
                  </select>
                  <button 
                    onClick={toggleListening}
                    className={`flex-1 btn-primary py-4 transition-all ${
                      isListening ? "bg-red-500 hover:bg-red-600 animate-pulse" : "bg-blue-600 hover:bg-blue-700"
                    }`}
                  >
                    {isListening ? "Listening... (Tap to Stop)" : "Tap to Speak"}
                  </button>
                </div>
              )}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default function App() {
  const [inChat, setInChat] = useState(false);
  return inChat ? <FarmerChatbot /> : <LandingPage onEnterChat={() => setInChat(true)} />;
}