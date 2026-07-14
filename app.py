import os
import shutil
from pathlib import Path
from PIL import Image
import io
import uuid

project_name = "myapk"
package_name = "com.example.apk"
main_activity_name = "MainActivity"
splash_activity_name = "SplashActivity"
html_file_name = "index.html"
manifest_file_name = "manifest.json"
icon_path = r"C:\Users\nadhi\Downloads\kiko.png"


# Create directories
os.makedirs(f"{project_name}/app/src/main/java/{package_name.replace('.', '/')}", exist_ok=True)
os.makedirs(f"{project_name}/app/src/main/res/layout", exist_ok=True)
os.makedirs(f"{project_name}/app/src/main/assets", exist_ok=True)
os.makedirs(f"{project_name}/app/src/main/res/values", exist_ok=True)
# Removed raw directory since we're not using video anymore
os.makedirs(f"{project_name}/app/proguard", exist_ok=True)
for density in ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]:
    os.makedirs(f"{project_name}/app/src/main/res/mipmap-{density}", exist_ok=True)

# Handle app icon for launcher
def create_fallback_icon(size):
    """Create a fallback ic_launcher.png (blue square)"""
    img = Image.new('RGBA', (size, size), (0, 0, 255, 255))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

icon_sizes = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192
}

if os.path.exists(icon_path):
    try:
        with Image.open(icon_path) as img:
            if img.format == 'PNG' and img.size[0] >= 192 and img.size[1] >= 192:
                print(f"Using {icon_path} for ic_launcher.png")
                for density, size in icon_sizes.items():
                    resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
                    output_path = f"{project_name}/app/src/main/res/mipmap-{density}/ic_launcher.png"
                    resized_img.save(output_path, format='PNG')
                    print(f"Created {output_path}")
            else:
                print(f"Warning: {icon_path} is not a valid PNG or too small. Using fallback icon.")
                for density, size in icon_sizes.items():
                    output_path = f"{project_name}/app/src/main/res/mipmap-{density}/ic_launcher.png"
                    with open(output_path, 'wb') as f:
                        f.write(create_fallback_icon(size))
                    print(f"Created fallback {output_path}")
    except Exception as e:
        print(f"Error processing {icon_path}: {e}. Using fallback icon.")
        for density, size in icon_sizes.items():
            output_path = f"{project_name}/app/src/main/res/mipmap-{density}/ic_launcher.png"
            with open(output_path, 'wb') as f:
                f.write(create_fallback_icon(size))
            print(f"Created fallback {output_path}")
else:
    print(f"Icon not found at {icon_path}. Using fallback icon.")
    for density, size in icon_sizes.items():
        output_path = f"{project_name}/app/src/main/res/mipmap-{density}/ic_launcher.png"
        with open(output_path, 'wb') as f:
            f.write(create_fallback_icon(size))
        print(f"Created fallback {output_path}")

# Handle app icons for manifest
icon_192_path = f"{project_name}/app/src/main/assets/icon-192.png"
icon_512_path = f"{project_name}/app/src/main/assets/icon-512.png"
if os.path.exists(icon_path):
    try:
        with Image.open(icon_path) as img:
            if img.format == 'PNG' and img.size[0] >= 192 and img.size[1] >= 192:
                print(f"Using {icon_path} for manifest icons")
                for size, path in [(192, icon_192_path), (512, icon_512_path)]:
                    resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
                    resized_img.save(path, format='PNG')
                    print(f"Created {path}")
            else:
                print(f"Warning: {icon_path} is not a valid PNG or too small. Using fallback icons for manifest.")
                for size, path in [(192, icon_192_path), (512, icon_512_path)]:
                    with open(path, 'wb') as f:
                        f.write(create_fallback_icon(size))
                    print(f"Created fallback {path}")
    except Exception as e:
        print(f"Error processing {icon_path} for manifest icons: {e}. Using fallback icons.")
        for size, path in [(192, icon_192_path), (512, icon_512_path)]:
            with open(path, 'wb') as f:
                f.write(create_fallback_icon(size))
            print(f"Created fallback {path}")
else:
    print(f"Icon not found at {icon_path}. Using fallback icons for manifest.")
    for size, path in [(192, icon_192_path), (512, icon_512_path)]:
        with open(path, 'wb') as f:
            f.write(create_fallback_icon(size))
        print(f"Created fallback {path}")

# Removed video handling section since we're not using video anymore

# HTML content (updated to match provided HTML)
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delivo Food Delivery App</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #fdfdfd;
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden; 
        }

        /* App Container fixed to viewport */
        .app-container {
            width: 100%;
            height: 100vh;
            background-color: #fdfdfd;
            position: relative;
            overflow: hidden; /* Prevent container scrolling, let inner screens scroll */
        }

        /* Hide scrollbars universally for cleaner look */
        ::-webkit-scrollbar {
            display: none;
        }
        * {
            -ms-overflow-style: none;
            scrollbar-width: none;
            -webkit-tap-highlight-color: transparent;
        }

        .text-brand { color: #ff5a1f; }
        .bg-brand { background-color: #ff5a1f; }
        .bg-brand-light { background-color: #fff0eb; }
        .border-brand { border-color: #ff5a1f; }

        /* Custom Radio Button Styles */
        .custom-radio input[type="radio"] { display: none; }
        .custom-radio .checkmark {
            width: 20px; height: 20px; border-radius: 50%;
            border: 2px solid #d1d5db; display: flex;
            align-items: center; justify-content: center;
            margin-right: 12px; transition: all 0.2s;
        }
        .custom-radio input[type="radio"]:checked + .checkmark { background-color: #ff5a1f; border-color: #ff5a1f; }
        .custom-radio input[type="radio"]:checked + .checkmark::after {
            content: ''; width: 10px; height: 10px;
            background-color: white; border-radius: 50%; display: block;
        }
        .custom-radio input[type="radio"]:checked ~ .label-text { color: #111827; font-weight: 500; }
        
        /* Floating bottom nav shadow */
        .bottom-nav-shadow { box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); }

        /* App Animations */
        .toast-enter { animation: toast-in 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        .toast-exit { animation: toast-out 0.3s ease-in forwards; }
        
        @keyframes toast-in { 
            from { transform: translateY(-150%); opacity: 0; } 
            to { transform: translateY(0); opacity: 1; } 
        }
        @keyframes toast-out { 
            from { transform: translateY(0); opacity: 1; } 
            to { transform: translateY(-150%); opacity: 0; } 
        }
        
        /* Utility for screens to take full height and scroll internally */
        .screen {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            overflow-y: auto;
            padding-bottom: 7rem; /* Make space for fixed bottom nav */
            background-color: #fdfdfd;
        }
    </style>
</head>
<body>

    <div class="app-container" id="app-root">
        
        <!-- Toast Notification Container -->
        <div id="toast-container" class="absolute top-6 left-0 right-0 z-[100] flex flex-col items-center space-y-2 pointer-events-none px-4"></div>

        <!-- ================= SCREEN 0: HOME ================= -->
        <div id="screen-home" class="screen block transition-all duration-300 ease-out origin-top">
            <div class="px-5 pt-8">
                <!-- Header -->
                <div class="flex justify-between items-center">
                    <div class="flex items-center space-x-1 cursor-pointer" onclick="showToast('Location selection coming soon')">
                        <svg class="w-5 h-5 text-brand" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                        <span class="font-bold text-gray-800 text-lg">Albuquerque, NM</span>
                        <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </div>
                    <div class="relative cursor-pointer hover:scale-105 transition-transform" onclick="showToast('You have no new notifications')">
                        <svg class="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                        <span class="absolute top-0 right-0 block h-2.5 w-2.5 rounded-full bg-red-500 border-2 border-white"></span>
                    </div>
                </div>

                <!-- Search Bar Placeholder (Navigates to Search Tab) -->
                <div class="mt-6 relative" onclick="document.querySelectorAll('.nav-btn')[1].click()">
                    <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" /></svg>
                    </div>
                    <div class="block w-full pl-11 pr-12 py-3.5 bg-white border border-gray-100 rounded-full text-sm shadow-[0_4px_20px_rgba(0,0,0,0.03)] text-gray-400 font-medium cursor-text">Search delivo™</div>
                </div>

                <!-- Promo Banner -->
                <div class="mt-6 bg-gradient-to-r from-[#ff6b2b] to-[#ff4a00] rounded-[28px] p-5 relative overflow-hidden text-white shadow-lg">
                    <div class="relative z-10 w-2/3">
                        <div class="flex items-center space-x-2 text-xs mb-1">
                            <span class="opacity-90">Use code</span>
                            <span class="bg-white text-brand font-bold px-2 py-0.5 rounded text-[10px]">FIRST50</span>
                            <span class="opacity-90">at checkout.</span>
                        </div>
                        <p class="text-[11px] opacity-90 mb-3">Hurry, offer ends soon!</p>
                        <h2 class="text-[22px] font-bold leading-tight mb-4 text-white">Get 50% Off<br>Your First Order!</h2>
                        <button onclick="handlePromoClick(this)" class="bg-black text-white text-xs font-semibold px-5 py-2.5 rounded-full hover:bg-gray-800 transition active:scale-95 min-w-[105px] text-center flex justify-center items-center">Order Now</button>
                    </div>
                    <img src="https://images.unsplash.com/photo-1573080496219-bb080dd4f877?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80" alt="Fries" class="absolute -right-6 top-6 w-32 h-32 object-cover rounded-full rotate-12 opacity-90 mix-blend-luminosity">
                    <div class="absolute right-4 bottom-4 w-16 h-16 bg-white/20 rounded-full blur-xl"></div>
                </div>
                
                <!-- Pagination Dots -->
                <div class="flex justify-center space-x-1.5 mt-4">
                    <div class="w-6 h-1 bg-gray-800 rounded-full transition-all"></div>
                    <div class="w-1 h-1 bg-gray-300 rounded-full transition-all"></div>
                    <div class="w-1 h-1 bg-gray-300 rounded-full transition-all"></div>
                    <div class="w-1 h-1 bg-gray-300 rounded-full transition-all"></div>
                </div>

                <!-- Categories -->
                <div class="flex space-x-4 mt-6 overflow-x-auto pb-2 -mx-5 px-5 scrollbar-hide">
                    <div onclick="selectCategory(this)" class="category-item flex flex-col items-center space-y-2 cursor-pointer flex-shrink-0">
                        <div class="icon-bg w-[68px] h-[68px] bg-brand rounded-[20px] flex items-center justify-center p-2.5 shadow-md shadow-orange-500/20 transition-all duration-300 scale-105">
                            <img src="https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80" alt="Burger" class="w-full h-full object-cover rounded-xl mix-blend-multiply brightness-110">
                        </div>
                        <span class="icon-text text-[13px] font-bold text-brand transition-colors duration-300">Burger</span>
                    </div>
                    <div onclick="selectCategory(this)" class="category-item flex flex-col items-center space-y-2 cursor-pointer flex-shrink-0 group">
                        <div class="icon-bg w-[68px] h-[68px] bg-[#1a1a1a] rounded-[20px] flex items-center justify-center p-2.5 group-hover:bg-gray-800 transition-all duration-300 active:scale-95">
                            <img src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80" alt="Pizza" class="w-full h-full object-cover rounded-xl opacity-90">
                        </div>
                        <span class="icon-text text-[13px] font-semibold text-gray-700 transition-colors duration-300 group-hover:text-gray-900">Pizza</span>
                    </div>
                    <div onclick="selectCategory(this)" class="category-item flex flex-col items-center space-y-2 cursor-pointer flex-shrink-0 group">
                        <div class="icon-bg w-[68px] h-[68px] bg-[#1a1a1a] rounded-[20px] flex items-center justify-center p-2.5 group-hover:bg-gray-800 transition-all duration-300 active:scale-95">
                            <img src="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80" alt="Salad" class="w-full h-full object-cover rounded-xl opacity-90">
                        </div>
                        <span class="icon-text text-[13px] font-semibold text-gray-700 transition-colors duration-300 group-hover:text-gray-900">Salad</span>
                    </div>
                    <div onclick="selectCategory(this)" class="category-item flex flex-col items-center space-y-2 cursor-pointer flex-shrink-0 group">
                        <div class="icon-bg w-[68px] h-[68px] bg-[#1a1a1a] rounded-[20px] flex items-center justify-center p-2.5 group-hover:bg-gray-800 transition-all duration-300 active:scale-95">
                            <img src="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80" alt="Sushi" class="w-full h-full object-cover rounded-xl opacity-90">
                        </div>
                        <span class="icon-text text-[13px] font-semibold text-gray-700 transition-colors duration-300 group-hover:text-gray-900">Sushi</span>
                    </div>
                </div>

                <!-- Top Picks Section -->
                <div class="mt-8">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-lg font-bold text-gray-900">Top picks on delivo™</h3>
                        <button onclick="showToast('Loading all top picks...')" class="bg-[#ffdd00] text-gray-900 text-[11px] font-bold px-3 py-1.5 rounded-full hover:bg-yellow-400 transition active:scale-95">See all</button>
                    </div>

                    <div class="flex space-x-4 overflow-x-auto pb-4 -mx-5 px-5 scrollbar-hide">
                        <!-- Product Card 1 -->
                        <div onclick="navigateToDetail(this)" class="min-w-[240px] bg-white rounded-[24px] p-3 shadow-[0_8px_24px_rgba(149,157,165,0.08)] cursor-pointer border border-gray-100 flex-shrink-0 group hover:shadow-[0_8px_24px_rgba(149,157,165,0.15)] transition-shadow">
                            <div class="relative h-40 rounded-[20px] overflow-hidden mb-3 bg-[#111]">
                                <img src="https://images.unsplash.com/photo-1550547660-d9450f859349?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Cheeseburger" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                                <button onclick="event.stopPropagation(); showToast('Added to wishlist')" class="absolute top-2 right-2 bg-white/90 p-1.5 rounded-full shadow-sm hover:bg-white transition active:scale-90">
                                    <svg class="w-4 h-4 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                                </button>
                                <div class="absolute bottom-2 left-2 bg-white/95 px-2.5 py-1 rounded-lg text-[11px] font-bold flex items-center space-x-1 shadow-sm">
                                    <svg class="w-3 h-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    <span>31 min</span>
                                </div>
                            </div>
                            <h4 class="font-bold text-gray-900 text-[15px] mb-1">Cheese Burger</h4>
                            <div class="flex justify-between items-center text-[12px] mb-3">
                                <div class="flex items-center text-gray-600 space-x-1">
                                    <svg class="w-3.5 h-3.5 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                                    <span class="font-medium">Burger Haven</span>
                                </div>
                                <div class="flex items-center font-bold text-gray-900">
                                    <span>4.8</span>
                                    <svg class="w-3.5 h-3.5 text-yellow-400 mx-0.5 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                                    <span class="text-gray-400 font-normal text-[10px]">(335+)</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-end mt-1">
                                <span class="text-brand text-[11px] font-semibold">$0 Delivery fee over $26</span>
                                <span class="bg-gray-900 text-white px-3 py-1.5 rounded-[12px] font-bold text-[13px]">$8.99</span>
                            </div>
                        </div>

                        <!-- Product Card 2 -->
                        <div onclick="navigateToDetail(this)" class="min-w-[240px] bg-white rounded-[24px] p-3 shadow-[0_8px_24px_rgba(149,157,165,0.08)] border border-gray-100 flex-shrink-0 group cursor-pointer hover:shadow-[0_8px_24px_rgba(149,157,165,0.15)] transition-shadow">
                            <div class="relative h-40 rounded-[20px] overflow-hidden mb-3 bg-[#111]">
                                <img src="https://images.unsplash.com/photo-1553979459-d2229ba7433b?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="BBQ Bacon Burger" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                                <button onclick="event.stopPropagation(); showToast('Added to wishlist')" class="absolute top-2 right-2 bg-white/90 p-1.5 rounded-full shadow-sm hover:bg-white transition active:scale-90">
                                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                                </button>
                                <div class="absolute bottom-2 left-2 bg-white/95 px-2.5 py-1 rounded-lg text-[11px] font-bold flex items-center space-x-1 shadow-sm">
                                    <svg class="w-3 h-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    <span>27 min</span>
                                </div>
                            </div>
                            <h4 class="font-bold text-gray-900 text-[15px] mb-1 truncate">Burger Haven Special</h4>
                            <div class="flex justify-between items-center text-[12px] mb-3">
                                <div class="flex items-center text-gray-600 space-x-1">
                                    <svg class="w-3.5 h-3.5 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                                    <span class="font-medium truncate">BBQ Bacon...</span>
                                </div>
                                <div class="flex items-center font-bold text-gray-900">
                                    <span>4.6</span>
                                    <svg class="w-3.5 h-3.5 text-yellow-400 mx-0.5 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                                    <span class="text-gray-400 font-normal text-[10px]">(120+)</span>
                                </div>
                            </div>
                            <div class="flex justify-between items-end mt-1">
                                <span class="text-brand text-[11px] font-semibold">$0 Delivery fee over $26</span>
                                <span class="bg-gray-900 text-white px-3 py-1.5 rounded-[12px] font-bold text-[13px]">$9.99</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= SCREEN 1: SEARCH ================= -->
        <div id="screen-search" class="screen hidden">
            <div class="px-5 pt-8">
                <h2 class="text-2xl font-bold text-gray-900 mb-4">Search</h2>
                <!-- Search Bar -->
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" /></svg>
                    </div>
                    <input id="main-search-input" type="text" onkeyup="handleSearch(event)" class="block w-full pl-11 pr-12 py-3.5 bg-white border border-gray-100 rounded-full text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-brand/20 transition-all placeholder-gray-400 font-medium" placeholder="Burgers, pizza, sushi..." autofocus>
                </div>
                
                <h3 class="font-bold text-gray-900 mt-8 mb-3">Popular Searches</h3>
                <div class="flex flex-wrap gap-2">
                    <span class="px-4 py-2 bg-gray-100 rounded-full text-sm font-medium text-gray-700 cursor-pointer hover:bg-gray-200 transition">Healthy Salads</span>
                    <span class="px-4 py-2 bg-gray-100 rounded-full text-sm font-medium text-gray-700 cursor-pointer hover:bg-gray-200 transition">Spicy Tacos</span>
                    <span class="px-4 py-2 bg-gray-100 rounded-full text-sm font-medium text-gray-700 cursor-pointer hover:bg-gray-200 transition">Vegan</span>
                    <span class="px-4 py-2 bg-gray-100 rounded-full text-sm font-medium text-gray-700 cursor-pointer hover:bg-gray-200 transition">Desserts</span>
                </div>
            </div>
        </div>

        <!-- ================= SCREEN 2: CART ================= -->
        <div id="screen-cart" class="screen hidden">
            <div class="px-5 pt-8">
                <h2 class="text-2xl font-bold text-gray-900 mb-6">Your Cart</h2>
                
                <!-- Dynamic Cart Items Container -->
                <div id="cart-items-container" class="space-y-4">
                    <!-- Items rendered here via JS -->
                </div>

                <div class="mt-8 border-t border-gray-100 pt-6">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-gray-500 font-medium">Subtotal</span>
                        <span id="cart-subtotal" class="font-bold text-gray-900">$0.00</span>
                    </div>
                    <div class="flex justify-between items-center mb-4">
                        <span class="text-gray-500 font-medium">Delivery</span>
                        <span class="font-bold text-brand">Free</span>
                    </div>
                    <div class="flex justify-between items-center text-lg">
                        <span class="font-bold text-gray-900">Total</span>
                        <span id="cart-total" class="font-extrabold text-gray-900">$0.00</span>
                    </div>
                    
                    <button onclick="handleCheckout(this)" id="checkout-btn" class="w-full mt-6 bg-brand text-white font-bold py-4 rounded-full shadow-lg hover:bg-[#e04e18] transition-colors active:scale-95 disabled:opacity-50 disabled:active:scale-100" disabled>
                        Proceed to Checkout
                    </button>
                </div>
            </div>
        </div>

        <!-- ================= SCREEN 3: PROFILE ================= -->
        <div id="screen-profile" class="screen hidden">
            <div class="px-5 pt-8">
                <h2 class="text-2xl font-bold text-gray-900 mb-6">Profile</h2>
                
                <div class="flex items-center space-x-4 mb-8">
                    <div class="w-20 h-20 rounded-full bg-brand-light flex items-center justify-center border-4 border-white shadow-sm overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80" alt="Avatar" class="w-full h-full object-cover">
                    </div>
                    <div>
                        <h3 class="text-xl font-bold text-gray-900">John Doe</h3>
                        <p class="text-gray-500 text-sm">john.doe@example.com</p>
                    </div>
                </div>

                <div class="space-y-3">
                    <div class="flex justify-between items-center bg-white p-4 rounded-2xl border border-gray-50 shadow-sm cursor-pointer hover:shadow-md transition" onclick="showToast('Loading Orders...')">
                        <div class="flex items-center space-x-3">
                            <div class="p-2 bg-gray-50 rounded-xl text-gray-600">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
                            </div>
                            <span class="font-semibold text-gray-800">My Orders</span>
                        </div>
                        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    </div>
                    <div class="flex justify-between items-center bg-white p-4 rounded-2xl border border-gray-50 shadow-sm cursor-pointer hover:shadow-md transition" onclick="showToast('Loading Addresses...')">
                        <div class="flex items-center space-x-3">
                            <div class="p-2 bg-gray-50 rounded-xl text-gray-600">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                            </div>
                            <span class="font-semibold text-gray-800">Saved Addresses</span>
                        </div>
                        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    </div>
                    <div class="flex justify-between items-center bg-white p-4 rounded-2xl border border-gray-50 shadow-sm cursor-pointer hover:shadow-md transition" onclick="showToast('Loading Payment Methods...')">
                        <div class="flex items-center space-x-3">
                            <div class="p-2 bg-gray-50 rounded-xl text-gray-600">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
                            </div>
                            <span class="font-semibold text-gray-800">Payment Methods</span>
                        </div>
                        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= PRODUCT DETAIL (OVERLAY) ================= -->
        <!-- Fixed position overlay that slides in -->
        <div id="screen-detail" class="fixed inset-0 bg-white z-[60] flex flex-col transform translate-x-full transition-transform duration-300 ease-out shadow-[-20px_0_40px_rgba(0,0,0,0.1)]">
            <!-- Header Nav -->
            <div class="flex justify-between items-center px-5 py-4 pt-8 bg-white z-10 sticky top-0">
                <button onclick="navigateToHome()" class="p-2 rounded-full bg-gray-50 hover:bg-gray-100 transition active:scale-95">
                    <svg class="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
                <div class="flex space-x-3">
                    <button onclick="showToast('Link copied to clipboard!')" class="p-2 rounded-full bg-gray-50 hover:bg-gray-100 transition active:scale-95">
                        <svg class="w-5 h-5 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                    </button>
                    <button onclick="toggleFavorite(this)" class="p-2 rounded-full bg-gray-50 hover:bg-gray-100 transition active:scale-95 group">
                        <svg id="heart-icon" class="w-5 h-5 text-gray-800 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                    </button>
                </div>
            </div>

            <!-- Scrollable Content -->
            <div class="flex-1 overflow-y-auto px-5 pb-32">
                <!-- Main Image -->
                <div class="relative w-full h-[300px] mt-2 rounded-[32px] overflow-hidden bg-[#111]">
                    <img id="detail-image" src="https://images.unsplash.com/photo-1550547660-d9450f859349?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Item Image" class="w-full h-full object-cover">
                    <div class="absolute bottom-4 left-4 bg-brand text-white px-4 py-1.5 rounded-full font-bold text-[17px] shadow-lg">
                        $ 8.99
                    </div>
                </div>

                <!-- Title & Info -->
                <div class="mt-5 flex justify-between items-start">
                    <div>
                        <h1 id="detail-title" class="text-[26px] font-extrabold text-gray-900 tracking-tight leading-tight">Cheese Burger</h1>
                        <p class="text-brand font-semibold mt-1 text-[13px]">$0 Delivery fee over $26</p>
                    </div>
                    <div class="flex items-center space-x-1 bg-gray-50 px-3 py-1.5 rounded-full mt-1 border border-gray-100">
                        <span class="text-brand text-sm">🔥</span>
                        <span class="text-[13px] font-bold text-gray-700">271 Cal.</span>
                    </div>
                </div>

                <!-- Ingredients -->
                <div class="mt-6">
                    <h3 class="text-[17px] font-bold text-gray-900 mb-2.5">Ingredients</h3>
                    <p class="text-gray-600 text-[13px] leading-relaxed font-medium">
                        • 1 Juicy beef &nbsp; • 1 Slice of cheddar cheese<br>
                        • 1 burger bun &nbsp; • Fresh lettuce<br>
                        • Ripe tomato slices &nbsp; • Pickles for crunch<br>
                        • Ketchup &nbsp; • Mustard &nbsp; • Onions and bacon
                    </p>
                </div>

                <!-- Variations Form -->
                <div class="mt-6 bg-[#f7f7f7] rounded-[24px] p-5">
                    <h3 class="text-[17px] font-bold text-gray-900 mb-4">Variation</h3>
                    
                    <div class="space-y-4">
                        <label class="custom-radio flex items-center justify-between cursor-pointer group">
                            <div class="flex items-center">
                                <input type="radio" name="variation" value="Small" checked>
                                <div class="checkmark"></div>
                                <span class="label-text text-gray-600 text-sm group-hover:text-gray-900 transition">Small</span>
                            </div>
                            <span class="font-bold text-gray-900 text-sm">$ 8.99</span>
                        </label>
                        <label class="custom-radio flex items-center justify-between cursor-pointer group">
                            <div class="flex items-center">
                                <input type="radio" name="variation" value="Medium">
                                <div class="checkmark"></div>
                                <span class="label-text text-gray-600 text-sm group-hover:text-gray-900 transition">Medium</span>
                            </div>
                            <span class="font-bold text-gray-900 text-sm">$ 9.99</span>
                        </label>
                        <label class="custom-radio flex items-center justify-between cursor-pointer group">
                            <div class="flex items-center">
                                <input type="radio" name="variation" value="Large">
                                <div class="checkmark"></div>
                                <span class="label-text text-gray-600 text-sm group-hover:text-gray-900 transition">Large</span>
                            </div>
                            <span class="font-bold text-gray-900 text-sm">$ 10.99</span>
                        </label>
                    </div>
                </div>
            </div>

            <!-- Bottom Action Bar -->
            <div class="absolute bottom-0 left-0 right-0 p-5 bg-white bg-opacity-95 backdrop-blur-sm pt-4 pb-8 border-t border-gray-50 z-20">
                <div class="bg-brand rounded-full p-2 pl-6 flex justify-between items-center shadow-lg shadow-orange-500/30">
                    <button id="add-to-cart-btn" onclick="addToCart(this)" class="text-white font-bold text-lg flex-1 text-left flex items-center min-w-[120px] focus:outline-none transition-opacity active:opacity-75">
                        Add to cart
                    </button>
                    
                    <div class="flex items-center bg-[#d94a1a] rounded-full p-1 px-2 text-white shadow-inner">
                        <button onclick="updateQty(-1)" class="w-8 h-8 flex items-center justify-center font-bold text-lg hover:bg-black/10 rounded-full transition active:scale-90">-</button>
                        <span id="qty-display" class="w-6 text-center font-bold text-lg">1</span>
                        <button onclick="updateQty(1)" class="w-8 h-8 flex items-center justify-center font-bold text-lg hover:bg-black/10 rounded-full transition active:scale-90">+</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= GLOBAL BOTTOM NAVIGATION ================= -->
        <!-- Properly fixed at the bottom of the app container -->
        <div class="absolute bottom-6 left-6 right-6 bg-white rounded-full py-3 px-4 flex justify-between items-center bottom-nav-shadow z-[70]">
            <button onclick="selectTab(0, this)" class="nav-btn bg-brand text-white flex items-center space-x-2 px-5 py-2.5 rounded-full transition-all active:scale-95">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                <span class="font-bold text-sm nav-text">Explore</span>
            </button>
            <button onclick="selectTab(1, this)" class="nav-btn p-2 text-gray-400 hover:text-gray-800 transition-all flex items-center space-x-2 rounded-full active:scale-95">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                <span class="font-bold text-sm nav-text hidden">Search</span>
            </button>
            <button onclick="selectTab(2, this)" class="nav-btn p-2 text-gray-400 hover:text-gray-800 transition-all flex items-center space-x-2 rounded-full active:scale-95 relative">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
                <span id="cart-badge" class="absolute top-1 right-2 hidden h-2.5 w-2.5 rounded-full bg-red-500 border-2 border-white"></span>
                <span class="font-bold text-sm nav-text hidden">Cart</span>
            </button>
            <button onclick="selectTab(3, this)" class="nav-btn p-2 text-gray-400 hover:text-gray-800 transition-all flex items-center space-x-2 rounded-full active:scale-95">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                <span class="font-bold text-sm nav-text hidden">Profile</span>
            </button>
        </div>
        
    </div>

    <script>
        // Global App State
        const state = {
            qty: 1,
            isFavorite: false,
            selectedVariation: 'Small',
            basePrices: { 'small': 8.99, 'medium': 9.99, 'large': 10.99 },
            cart: [], // Stores items added to cart
            currentProductImage: "https://images.unsplash.com/photo-1550547660-d9450f859349?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
        };

        // Screen Elements array matching tab indices
        const screens = [
            document.getElementById('screen-home'),
            document.getElementById('screen-search'),
            document.getElementById('screen-cart'),
            document.getElementById('screen-profile')
        ];
        
        const detailScreen = document.getElementById('screen-detail');
        const qtyDisplay = document.getElementById('qty-display');
        const toastContainer = document.getElementById('toast-container');

        // Navigation for Product Details
        function navigateToDetail(cardElement) {
            // Grab info from clicked card to populate detail screen
            const title = cardElement.querySelector('h4').innerText;
            const img = cardElement.querySelector('img').src;
            
            document.getElementById('detail-title').innerText = title;
            document.getElementById('detail-image').src = img;
            state.currentProductImage = img; // save for cart

            // Reset variation to Small
            document.querySelector('input[name="variation"][value="Small"]').checked = true;
            state.selectedVariation = 'Small';
            state.qty = 1;
            qtyDisplay.innerText = state.qty;

            // Slide in
            detailScreen.classList.remove('translate-x-full');
            detailScreen.querySelector('.overflow-y-auto').scrollTop = 0;
            
            // Dim background (only the active screen)
            screens.forEach(s => {
                if(!s.classList.contains('hidden')) {
                    s.style.transform = 'scale(0.97)';
                    s.style.opacity = '0.5';
                    s.style.pointerEvents = 'none';
                }
            });
        }

        function navigateToHome() {
            detailScreen.classList.add('translate-x-full');
            // Restore background
            screens.forEach(s => {
                if(!s.classList.contains('hidden')) {
                    s.style.transform = 'scale(1)';
                    s.style.opacity = '1';
                    s.style.pointerEvents = 'auto';
                }
            });
        }

        // --- Core Application Logic ---

        function updateQty(change) {
            state.qty += change;
            if (state.qty < 1) state.qty = 1;
            if (state.qty > 99) state.qty = 99;
            qtyDisplay.innerText = state.qty;
        }

        function addToCart(btn) {
            simulateLoading(btn, "Add to cart", () => {
                const title = document.getElementById('detail-title').innerText;
                const price = state.basePrices[state.selectedVariation.toLowerCase()];
                const total = (price * state.qty).toFixed(2);
                
                // Save to cart array
                state.cart.push({
                    name: title,
                    variation: state.selectedVariation,
                    price: price,
                    qty: state.qty,
                    image: state.currentProductImage
                });

                updateCartUI();
                showToast(`Added ${state.qty}x ${state.selectedVariation} ${title} ($${total})`);
                setTimeout(navigateToHome, 600);
            });
        }

        function updateCartUI() {
            const badge = document.getElementById('cart-badge');
            if(state.cart.length > 0) {
                badge.classList.remove('hidden');
                document.getElementById('checkout-btn').disabled = false;
            } else {
                badge.classList.add('hidden');
                document.getElementById('checkout-btn').disabled = true;
            }
        }

        function renderCartPage() {
            const container = document.getElementById('cart-items-container');
            const subtotalEl = document.getElementById('cart-subtotal');
            const totalEl = document.getElementById('cart-total');

            if (state.cart.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-12">
                        <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
                        </div>
                        <h3 class="text-lg font-bold text-gray-900">Your cart is empty</h3>
                        <p class="text-gray-500 text-sm mt-1">Looks like you haven't added anything yet.</p>
                        <button onclick="selectTab(0, document.querySelectorAll('.nav-btn')[0])" class="mt-6 text-brand font-bold">Browse Menu</button>
                    </div>`;
                subtotalEl.innerText = '$0.00';
                totalEl.innerText = '$0.00';
                return;
            }

            let html = '';
            let total = 0;
            state.cart.forEach((item, index) => {
                const itemTotal = item.price * item.qty;
                total += itemTotal;
                html += `
                    <div class="flex items-center space-x-4 bg-white p-3.5 rounded-2xl shadow-[0_2px_10px_rgba(0,0,0,0.03)] border border-gray-100 relative">
                        <div class="w-16 h-16 bg-gray-100 rounded-[14px] overflow-hidden flex-shrink-0">
                            <img src="${item.image}" class="w-full h-full object-cover">
                        </div>
                        <div class="flex-1">
                            <h4 class="font-bold text-gray-900 text-sm">${item.name}</h4>
                            <p class="text-xs text-gray-500 mt-0.5">${item.variation}</p>
                            <div class="font-bold text-brand mt-1.5 text-sm">$${item.price.toFixed(2)}</div>
                        </div>
                        <div class="font-bold text-gray-900 bg-gray-50 px-3 py-1 rounded-lg border border-gray-200">
                            x${item.qty}
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
            subtotalEl.innerText = `$${total.toFixed(2)}`;
            totalEl.innerText = `$${total.toFixed(2)}`;
        }

        function handleCheckout(btn) {
            simulateLoading(btn, "Proceed to Checkout", () => {
                showToast("Order Placed Successfully! 🎉", "success");
                state.cart = []; // Empty cart
                updateCartUI();
                renderCartPage();
                setTimeout(() => selectTab(0, document.querySelectorAll('.nav-btn')[0]), 2000); // go home
            });
        }

        // Bottom Navigation Tab Switching
        function selectTab(index, clickedBtn) {
            const tabs = document.querySelectorAll('.nav-btn');
            
            // UI Update for Tabs
            tabs.forEach((tab, i) => {
                const icon = tab.querySelector('svg');
                const text = tab.querySelector('.nav-text');
                
                if (i === index) {
                    tab.className = 'nav-btn bg-brand text-white flex items-center space-x-2 px-5 py-2.5 rounded-full transition-all active:scale-95';
                    icon.classList.remove('text-gray-400');
                    text.classList.remove('hidden');
                } else {
                    tab.className = 'nav-btn p-2 text-gray-400 hover:text-gray-800 transition-all flex items-center space-x-2 rounded-full active:scale-95 relative';
                    text.classList.add('hidden');
                }
            });
            
            // Switch Main Screens
            screens.forEach((screen, i) => {
                if(i === index) {
                    screen.classList.remove('hidden');
                    screen.classList.add('block');
                    // Reset transform scale if coming from detail view
                    screen.style.transform = 'scale(1)';
                    screen.style.opacity = '1';
                    screen.style.pointerEvents = 'auto';
                } else {
                    screen.classList.add('hidden');
                    screen.classList.remove('block');
                }
            });

            // Ensure detail screen closes if we switch main tabs
            if(!detailScreen.classList.contains('translate-x-full')) {
                detailScreen.classList.add('translate-x-full');
            }

            // Screen Specific Logic
            if(index === 1) {
                // Focus search bar slightly delayed
                setTimeout(() => document.getElementById('main-search-input').focus(), 100);
            }
            if(index === 2) {
                renderCartPage();
            }
        }

        // Form Events
        document.querySelectorAll('input[name="variation"]').forEach(radio => {
            radio.addEventListener('change', (e) => state.selectedVariation = e.target.value);
        });

        function handleSearch(e) {
            if (e.key === 'Enter' && e.target.value.trim() !== '') {
                showToast(`Searching menus for "${e.target.value}"...`);
                e.target.blur();
            }
        }

        function handlePromoClick(btn) {
            simulateLoading(btn, "Order Now", () => {
                showToast("Promo FIRST50 applied! Proceeding...", "success");
            });
        }

        function toggleFavorite(btn) {
            state.isFavorite = !state.isFavorite;
            const icon = document.getElementById('heart-icon');
            if (state.isFavorite) {
                icon.setAttribute('fill', '#ef4444');
                icon.classList.add('text-red-500');
                icon.style.transform = 'scale(1.25)';
                setTimeout(() => icon.style.transform = 'scale(1)', 200);
                showToast("Added to your wishlist ❤️");
            } else {
                icon.setAttribute('fill', 'none');
                icon.classList.remove('text-red-500');
                icon.style.transform = 'scale(1)';
            }
        }

        function selectCategory(clickedEl) {
            document.querySelectorAll('.category-item').forEach(item => {
                const bg = item.querySelector('.icon-bg');
                const text = item.querySelector('.icon-text');
                bg.className = 'icon-bg w-[68px] h-[68px] bg-[#1a1a1a] rounded-[20px] flex items-center justify-center p-2.5 transition-all duration-300 group-hover:bg-gray-800 active:scale-95';
                item.classList.add('group');
                text.className = 'icon-text text-[13px] font-semibold text-gray-700 transition-colors duration-300 group-hover:text-gray-900';
            });
            const activeBg = clickedEl.querySelector('.icon-bg');
            const activeText = clickedEl.querySelector('.icon-text');
            clickedEl.classList.remove('group');
            activeBg.className = 'icon-bg w-[68px] h-[68px] bg-brand rounded-[20px] flex items-center justify-center p-2.5 shadow-md shadow-orange-500/20 transition-all duration-300 scale-105';
            activeText.className = 'icon-text text-[13px] font-bold text-brand transition-colors duration-300';
        }

        // Utilities
        function simulateLoading(btnElement, originalText, callback) {
            const originalWidth = btnElement.offsetWidth;
            btnElement.style.width = `${originalWidth}px`;
            btnElement.disabled = true;
            btnElement.innerHTML = `<svg class="animate-spin h-5 w-5 mx-auto text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>`;
            setTimeout(() => {
                btnElement.disabled = false;
                btnElement.innerHTML = originalText;
                btnElement.style.width = 'auto'; 
                if(callback) callback();
            }, 800);
        }

        function showToast(message, type = 'success') {
            const toast = document.createElement('div');
            const bgClass = type === 'success' ? 'bg-gray-900' : 'bg-brand';
            toast.className = `px-5 py-3.5 rounded-[16px] shadow-xl text-sm font-bold text-white flex items-center space-x-2 toast-enter pointer-events-auto ${bgClass}`;
            toast.innerHTML = `
                ${type === 'success' ? '<svg class="w-5 h-5 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>' : ''}
                <span>${message}</span>
            `;
            toastContainer.appendChild(toast);
            setTimeout(() => {
                toast.classList.replace('toast-enter', 'toast-exit');
                setTimeout(() => toast.remove(), 300);
            }, 2500);
        }
    </script>
</body>
</html>
"""

# Write HTML file
with open(f"{project_name}/app/src/main/assets/{html_file_name}", "w", encoding="utf-8") as file:
    file.write(html_content)

# Manifest.json content
manifest_content = """{
    "name": "robo_dev",
    "short_name": "robo_dev",
    "description": "opensourced by robo_dev",
    "start_url": "index.html",
    "display": "standalone",
    "background_color": "#1e3a8a",
    "theme_color": "#1e3a8a",
    "orientation": "portrait",
    "icons": [
        {
            "src": "icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}
"""

# Write manifest.json file
with open(f"{project_name}/app/src/main/assets/{manifest_file_name}", "w", encoding="utf-8") as file:
    file.write(manifest_content)

# Root level build.gradle
root_build_gradle = """buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.7.0'
    }
}

tasks.register('clean', Delete) {
    delete rootProject.buildDir
}
"""

with open(f"{project_name}/build.gradle", "w", encoding="utf-8") as file:
    file.write(root_build_gradle)

# settings.gradle
settings_gradle = f"""pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
    plugins {{
        id 'com.android.application' version '8.7.0'
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{project_name}"
include ':app'
"""

with open(f"{project_name}/settings.gradle", "w", encoding="utf-8") as file:
    file.write(settings_gradle)

# gradle.properties
gradle_properties_content = """android.useAndroidX=true
org.gradle.jvmargs=-Xmx8g
org.gradle.parallel=true
# Set JDK 17 in Android Studio: File > Settings > Build, Gradle > Gradle JDK
# If needed, uncomment and set correct JDK path, e.g.:
#org.gradle.java.home=C:\\Program Files\\Java\\jdk-17
"""

with open(f"{project_name}/gradle.properties", "w", encoding="utf-8") as file:
    file.write(gradle_properties_content)

# Gradle wrapper properties
gradle_wrapper_properties = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.10-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""

os.makedirs(f"{project_name}/gradle/wrapper", exist_ok=True)
with open(f"{project_name}/gradle/wrapper/gradle-wrapper.properties", "w", encoding="utf-8") as file:
    file.write(gradle_wrapper_properties)

# local.properties
sdk_dir = r"C:\\Users\\nadhi\\AppData\Local\\Android\Sdk"
local_properties_content = f"""sdk.dir={sdk_dir}
"""

with open(f"{project_name}/local.properties", "w", encoding="utf-8") as file:
    file.write(local_properties_content)

# App-level build.gradle
app_build_gradle = f"""plugins {{
    id 'com.android.application'
}}

android {{
    namespace '{package_name}'
    compileSdk 34

    defaultConfig {{
        applicationId '{package_name}'
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
        multiDexEnabled true
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
        debug {{
            minifyEnabled false
        }}
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }}

    buildToolsVersion '34.0.0'

    configurations.all {{
        resolutionStrategy {{
            force 'androidx.core:core:1.13.1'
            force 'androidx.appcompat:appcompat:1.7.0'
            force 'org.jetbrains.kotlin:kotlin-stdlib:2.0.21'
        }}
    }}
}}

dependencies {{
    implementation('androidx.appcompat:appcompat:1.7.0') {{
        exclude group: 'androidx.core'
        exclude group: 'org.jetbrains.kotlin'
    }}
    implementation 'androidx.core:core:1.13.1'
    implementation 'androidx.multidex:multidex:2.0.1'
}}
"""

with open(f"{project_name}/app/build.gradle", "w", encoding="utf-8") as file:
    file.write(app_build_gradle)

# ProGuard rules
proguard_rules = """# Add project-specific ProGuard rules here.
-dontwarn androidx.**
-keep class androidx.** { *; }
-keep interface androidx.** { *; }
-dontwarn kotlin.**
-keep class kotlin.** { *; }
"""

with open(f"{project_name}/app/proguard-rules.pro", "w", encoding="utf-8") as file:
    file.write(proguard_rules)

# AndroidManifest.xml - Updated to make MainActivity the launcher activity
android_manifest = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:name="androidx.multidex.MultiDexApplication"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:theme="@style/Theme.AppCompat.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

with open(f"{project_name}/app/src/main/AndroidManifest.xml", "w", encoding="utf-8") as file:
    file.write(android_manifest)

# strings.xml
strings_xml = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">my apk</string>
</resources>
"""

with open(f"{project_name}/app/src/main/res/values/strings.xml", "w", encoding="utf-8") as file:
    file.write(strings_xml)

# MainActivity.java
main_activity = f"""package {package_name};

import android.annotation.SuppressLint;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class {main_activity_name} extends AppCompatActivity {{

    private static final int PERMISSION_REQUEST_CODE = 1;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Enable WebView debugging
        WebView.setWebContentsDebuggingEnabled(true);

        // Request permissions
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.INTERNET) != PackageManager.PERMISSION_GRANTED ||
            ContextCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_NETWORK_STATE) != PackageManager.PERMISSION_GRANTED) {{
            ActivityCompat.requestPermissions(
                this,
                new String[] {{
                    android.Manifest.permission.INTERNET,
                    android.Manifest.permission.ACCESS_NETWORK_STATE
                }},
                PERMISSION_REQUEST_CODE
            );
        }}

        WebView webView = findViewById(R.id.web_view);
        if (webView != null) {{
            WebSettings settings = webView.getSettings();
            settings.setJavaScriptEnabled(true);
            settings.setDomStorageEnabled(true);
            settings.setAllowFileAccess(true);
            settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
            webView.setWebViewClient(new WebViewClient() {{
                @Override
                public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {{
                    Log.e("WebView", "Error: " + (description != null ? description : "Unknown") + ", URL: " + (failingUrl != null ? failingUrl : "null"));
                    Toast.makeText({main_activity_name}.this, "WebView Error: " + description, Toast.LENGTH_LONG).show();
                }}

                @Override
                public boolean shouldOverrideUrlLoading(WebView view, String url) {{
                    if (url != null) {{
                        view.loadUrl(url);
                    }}
                    return true;
                }}
            }});
            String assetUrl = "file:///android_asset/{html_file_name}";
            Log.d("WebView", "Loading URL: " + assetUrl);
            webView.loadUrl(assetUrl);
        }} else {{
            Log.e("MainActivity", "Error: WebView not found");
            Toast.makeText(this, "Error: WebView not found", Toast.LENGTH_LONG).show();
        }}
    }}

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {{
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_CODE) {{
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {{
                Toast.makeText(this, "Permissions granted", Toast.LENGTH_SHORT).show();
            }} else {{
                Toast.makeText(this, "Permissions denied.", Toast.LENGTH_LONG).show();
            }}
        }}
    }}
}}
"""

with open(f"{project_name}/app/src/main/java/{package_name.replace('.', '/')}/{main_activity_name}.java", "w", encoding="utf-8") as file:
    file.write(main_activity)

# activity_main.xml
activity_main_xml = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <WebView
        android:id="@+id/web_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />
</LinearLayout>
"""

with open(f"{project_name}/app/src/main/res/layout/activity_main.xml", "w", encoding="utf-8") as file:
    file.write(activity_main_xml)

print(f"Android project '{project_name}' created successfully.")
print(f"App icon: {os.path.basename(icon_path) if os.path.exists(icon_path) else 'Fallback blue square'}")
print("Video splash screen has been removed.")
print(f"Manifest icons: {os.path.basename(icon_path) if os.path.exists(icon_path) else 'Fallback blue square'}")
print("Ensure your device is connected to the ESP32 Wi-Fi (IP: 192.168.4.1).")
print(f"Using SDK path: {sdk_dir}. Verify this path exists.")
print("Set JDK 17 in Android Studio: File > Settings > Build, Execution, Deployment > Gradle > Gradle JDK.")
print("Run './gradlew clean build' to build the APK.")
print("To debug, connect your device and use chrome://inspect in Chrome.")
print("If build fails, run './gradlew build --stacktrace --info > build_log.txt' for logs.")