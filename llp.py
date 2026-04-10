<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Last Leaf - AI Plant Health Monitor</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Outfit:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #FAF6ED;
            --text-dark: #3E3B35;
            --accent: #8E7C68;
            --terracotta: #C47A5D;
            --sage: #758A6C;
        }
        :root[data-theme="dark"] {
            --bg-color: #1a1a1a;
            --text-dark: #f0f0f0;
            --accent: #a09587;
            --terracotta: #d98d70;
            --sage: #8fa685;
        }
        
        :root[data-theme="dark"] .blob-1 { background: #3d3429; }
        :root[data-theme="dark"] .blob-2 { background: #2f382a; }
        :root[data-theme="dark"] .scanner-container { background: #2a2a2a; border-color: var(--accent); }
        :root[data-theme="dark"] .result-section { background: #262626; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        :root[data-theme="dark"] .result-section h3 { border-bottom-color: #444; }
        :root[data-theme="dark"] .modal-overlay { background: rgba(0, 0, 0, 0.9); }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-dark);
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }
        /* Typography */
        h1, h2, h3, .logo {
            font-family: 'Playfair Display', serif;
        }
        /* Navbar */
        header {
            padding: 2rem 6%;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            font-size: 2rem;
            font-weight: 600;
            color: var(--terracotta);
            text-decoration: none;
        }
        .nav-center {
            display: flex;
            gap: 2rem;
        }
        .nav-center a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 400;
            font-size: 1.05rem;
            position: relative;
        }
        .nav-center a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 1px;
            bottom: -4px;
            left: 0;
            background-color: var(--sage);
            transition: width 0.3s ease;
        }
        .nav-center a:hover::after {
            width: 100%;
        }
        .header-action button {
            background: none;
            border: 1px solid var(--accent);
            padding: 0.75rem 1.5rem;
            border-radius: 50px;
            color: var(--text-dark);
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .header-action button:hover {
            background: var(--text-dark);
            color: var(--bg-color);
        }
        /* Hero */
        main {
            flex: 1;
            display: flex;
            align-items: center;
            padding: 2rem 6%;
            position: relative;
        }
        .hero-content {
            flex: 1;
            max-width: 50%;
            z-index: 2;
        }
        .tagline {
            color: var(--terracotta);
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-size: 0.875rem;
            margin-bottom: 1rem;
            display: block;
        }
        h1 {
            font-size: 4.5rem;
            line-height: 1.1;
            margin-bottom: 1.5rem;
            color: var(--text-dark);
        }
        h1 i {
            color: var(--sage);
            font-weight: 400;
        }
        p.desc {
            font-size: 1.15rem;
            line-height: 1.7;
            color: var(--accent);
            margin-bottom: 3rem;
            max-width: 85%;
        }
        .btn-primary {
            display: inline-flex;
            justify-content: center;
            align-items: center;
            background-color: var(--terracotta);
            color: #fff;
            text-decoration: none;
            padding: 1.25rem 2.5rem;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 500;
            font-family: inherit;
            border: none;
            cursor: pointer;
            transition: transform 0.3s ease, background-color 0.3s ease;
            box-shadow: 0 10px 25px rgba(196, 122, 93, 0.2);
        }
        .btn-primary:hover {
            transform: translateY(-3px);
            background-color: #B0694C;
            box-shadow: 0 15px 30px rgba(196, 122, 93, 0.3);
        }
        .hero-image-wrapper {
            flex: 1;
            position: relative;
            display: flex;
            justify-content: flex-end;
            align-items: center;
        }
        .image-frame {
            position: relative;
            width: 80%;
            aspect-ratio: 4/5;
            border-radius: 200px 200px 20px 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
            animation: float 6s ease-in-out infinite;
        }
        .image-frame img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
        }
        /* Decorative Elements */
        .blob-1 {
            position: absolute;
            background: #E8DDCD;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.7;
            z-index: -1;
        }
        
        .blob-2 {
            position: absolute;
            background: #E4E7D3; /* sage tint */
            border-radius: 50%;
            filter: blur(70px);
            opacity: 0.6;
            z-index: -1;
        }
        .b1 { width: 400px; height: 400px; top: -50px; right: 20%; }
        .b2 { width: 300px; height: 300px; bottom: 0; left: 10%; }
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
            100% { transform: translateY(0px); }
        }
        /* Scanner Modal */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(62, 59, 53, 0.85);
            backdrop-filter: blur(5px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .modal-overlay.active {
            display: flex;
            opacity: 1;
        }
        .modal-content {
            background: var(--bg-color);
            padding: 2.5rem;
            border-radius: 20px;
            width: 90%;
            max-width: 550px;
            position: relative;
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
            text-align: center;
            max-height: 90vh;
            overflow-y: auto;
        }
        .close-modal {
            position: absolute;
            top: 15px; right: 20px;
            font-size: 2rem;
            cursor: pointer;
            background: none; border: none;
            color: var(--text-dark);
            line-height: 1;
        }
        .scanner-container {
            position: relative;
            width: 100%;
            height: 250px;
            background: #eadecd;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 2px dashed var(--accent);
        }
        .scanner-container img {
            width: 100%; height: 100%; object-fit: cover; border-radius: 13px;
        }
        .scan-line {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
            background: var(--terracotta);
            box-shadow: 0 0 15px var(--terracotta);
            animation: scan 2s linear infinite;
            display: none;
        }
        @keyframes scan {
            0% { top: -10%; opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { top: 110%; opacity: 0; }
        }
        .scan-status-text {
            font-size: 1.1rem;
            color: var(--accent);
            margin-bottom: 1rem;
            font-style: italic;
        }
        .scan-results {
            display: none;
            text-align: left;
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .scan-results h2 {
            margin-bottom: 0.2rem;
            color: var(--terracotta);
            font-size: 2rem;
        }
        .status-badge {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .status-healthy { background: var(--sage); color: white; }
        .status-diseased { background: #C47A5D; color: white; }
        .result-section {
            margin-bottom: 1.25rem;
            background: white;
            padding: 1.25rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        }
        .result-section h3 {
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            font-family: 'Outfit', sans-serif;
            color: var(--text-dark);
            border-bottom: 1px solid #eee;
            padding-bottom: 0.5rem;
        }
        .result-section ul {
            padding-left: 1.2rem;
            color: var(--accent);
            font-size: 0.95rem;
            line-height: 1.6;
        }
        .result-section p {
            color: var(--accent);
            font-size: 0.95rem;
            line-height: 1.6;
        }
        @media (max-width: 900px) {
            main {
                flex-direction: column-reverse;
                text-align: center;
                padding-top: 4rem;
                gap: 4rem;
            }
            .hero-content {
                max-width: 100%;
            }
            p.desc {
                max-width: 100%;
                margin: 0 auto 2.5rem;
            }
            .hero-image-wrapper {
                justify-content: center;
                width: 100%;
            }
            .image-frame {
                width: 90%;
            }
            .nav-center {
                display: none; /* simple mobile behavior for now */
            }
            h1 {
                font-size: 3.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="blob-1 b1"></div>
    <div class="blob-2 b2"></div>
    
    <header>
        <a href="#" class="logo">Last Leaf.</a>
        <nav class="nav-center">
            <a href="#">Scan Plant</a>
            <a href="#">Disease DB</a>
            <a href="#">My Garden</a>
        </nav>
        <div class="header-action">
            <button id="themeToggle" style="margin-right: 15px; font-size: 1.2rem; cursor: pointer; padding: 0.5rem; border-radius: 50%;">🌙</button>
        </div>
    </header>
    <main>
        <div class="hero-content">
            <span class="tagline">AI-Powered Plant Care</span>
            <h1>Identify plant <i>diseases</i> in seconds.</h1>
            <p class="desc">Snap a photo of a leaf, and our advanced AI will instantly identify the species, diagnose diseases, and recommend precise treatments to save your plant.</p>
            <button id="scanBtn" class="btn-primary">Scan Plant Leaf</button>
            <input type="file" id="imageInput" accept="image/*" style="display: none;" />
        </div>
        <div class="hero-image-wrapper">
            <div class="image-frame">
                <img src="assets/organic_plant_1775827810882.png" alt="A lush cascading pothos plant in a beautifully textured terracotta hanging pot">
            </div>
        </div>
    </main>
    <!-- Scanner Modal -->
    <div class="modal-overlay" id="scannerModal">
        <div class="modal-content">
            <button class="close-modal" id="closeModal">&times;</button>
            <h2 id="modalTitle" style="margin-bottom: 1.5rem; color: var(--text-dark);">AI Plant Scanner</h2>
            
            <div class="scanner-container">
                <video id="cameraFeed" autoplay playsinline style="display: none; width: 100%; height: 100%; object-fit: cover; border-radius: 13px;"></video>
                <canvas id="captureCanvas" style="display: none;"></canvas>
                <img id="scannedImage" src="" alt="Scanned Leaf" style="display: none;">
                <div class="scan-line" id="scanLine"></div>
                <p id="placeholderText" style="color: var(--accent); padding: 2rem;">Connecting to camera...</p>
            </div>
            <button id="captureBtn" class="btn-primary" style="margin-bottom: 1.5rem; display: none;">Capture Photo</button>
            
            <p class="scan-status-text" id="scanStatusText">Awaiting image...</p>
            <div class="scan-results" id="scanResults">
                <h2 id="resPlantName">Plant Name</h2>
                <span class="status-badge" id="resStatusBadge">Status</span>
                
                <div class="result-section" id="resDiseaseSection" style="display:none;">
                    <h3>Diagnosis</h3>
                    <p id="resDiseaseName" style="color: #ab4a4a; font-weight: 600;"></p>
                </div>
                <div class="result-section">
                    <h3>Symptoms Identified</h3>
                    <ul id="resSymptoms">
                    </ul>
                </div>
                <div class="result-section">
                    <h3>Plant Features</h3>
                    <ul id="resFeatures">
                    </ul>
                </div>
                <div class="result-section" id="resTreatmentSection" style="display:none;">
                    <h3>Recommended Treatment</h3>
                    <p id="resTreatment"></p>
                </div>
            </div>
        </div>
    </div>
    <script>
        const scanBtn = document.getElementById('scanBtn');
        const imageInput = document.getElementById('imageInput');
        const scannerModal = document.getElementById('scannerModal');
        const closeModal = document.getElementById('closeModal');
        const scannedImage = document.getElementById('scannedImage');
        const placeholderText = document.getElementById('placeholderText');
        const scanLine = document.getElementById('scanLine');
        const scanStatusText = document.getElementById('scanStatusText');
        const scanResults = document.getElementById('scanResults');
        const video = document.getElementById('cameraFeed');
        const canvas = document.getElementById('captureCanvas');
        const captureBtn = document.getElementById('captureBtn');
        let mediaStream = null;
        // Open Modal & Request Camera
        scanBtn.addEventListener('click', async () => {
            scannerModal.classList.add('active');
            // reset state
            scanResults.style.display = 'none';
            scannedImage.style.display = 'none';
            captureBtn.style.display = 'none';
            scanStatusText.innerText = 'Awaiting image...';
            placeholderText.innerText = 'Requesting camera access...';
            placeholderText.style.display = 'block';
            video.style.display = 'none';
            try {
                mediaStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
                video.srcObject = mediaStream;
                video.style.display = 'block';
                placeholderText.style.display = 'none';
                captureBtn.style.display = 'inline-flex';
            } catch (err) {
                placeholderText.innerText = 'Camera access denied. Please allow camera permissions to scan leaves.';
            }
        });
        // Capture Photo
        captureBtn.addEventListener('click', () => {
            // Draw video frame to canvas
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
            
            // Stop video stream
            if (mediaStream) {
                mediaStream.getTracks().forEach(track => track.stop());
            }
            video.style.display = 'none';
            captureBtn.style.display = 'none';
            
            // Show captured image
            scannedImage.src = canvas.toDataURL('image/png');
            scannedImage.style.display = 'block';
            
            // Run scanning simulation
            simulateScan();
        });
        // Close modal
        closeModal.addEventListener('click', () => {
            scannerModal.classList.remove('active');
            if (mediaStream) {
                mediaStream.getTracks().forEach(track => track.stop());
            }
        });
        function simulateScan() {
            scanLine.style.display = 'block';
            scanStatusText.innerText = 'Analyzing leaf structure and patterns...';
            scanResults.style.display = 'none';
            // Simulate AI processing delay
            setTimeout(() => {
                scanLine.style.display = 'none';
                scanStatusText.innerText = 'Analysis complete.';
                fetchAndDisplayData();
            }, 2500);
        }
        async function fetchAndDisplayData() {
            try {
                // Fetch our mock AI training data
                const response = await fetch('plant_data.json');
                const data = await response.json();
                
                // Randomly pick a result to simulate the AI classification
                const randomIdx = Math.floor(Math.random() * data.length);
                const result = data[randomIdx];
                displayResult(result);
            } catch (error) {
                console.error("Failed to load plant data", error);
                scanStatusText.innerText = 'Error connecting to AI model.';
            }
        }
        function displayResult(result) {
            scanStatusText.style.display = 'none';
            scanResults.style.display = 'block';
            // Update DOM elements
            document.getElementById('resPlantName').innerText = result.plant_name;
            
            const badge = document.getElementById('resStatusBadge');
            badge.innerText = result.status;
            badge.className = 'status-badge ' + (result.status === 'Healthy' ? 'status-healthy' : 'status-diseased');
            // Features
            const featuresList = document.getElementById('resFeatures');
            featuresList.innerHTML = '';
            result.plant_features.forEach(f => {
                const li = document.createElement('li');
                li.innerText = f;
                featuresList.appendChild(li);
            });
            // Symptoms
            const symptomsList = document.getElementById('resSymptoms');
            symptomsList.innerHTML = '';
            if (result.symptoms && result.symptoms.length > 0) {
                result.symptoms.forEach(s => {
                    const li = document.createElement('li');
                    li.innerText = s;
                    symptomsList.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.innerText = 'No symptoms detected. The leaf appears healthy.';
                symptomsList.appendChild(li);
            }
            // Disease specific sections
            const diseaseSection = document.getElementById('resDiseaseSection');
            const treatmentSection = document.getElementById('resTreatmentSection');
            if (result.status === 'Diseased') {
                diseaseSection.style.display = 'block';
                document.getElementById('resDiseaseName').innerText = result.disease_name;
                
                if (result.treatment) {
                    treatmentSection.style.display = 'block';
                    document.getElementById('resTreatment').innerText = result.treatment;
                } else {
                    treatmentSection.style.display = 'none';
                }
            } else {
                diseaseSection.style.display = 'none';
                treatmentSection.style.display = 'none';
            }
        }
        // Theme Toggle Logic
        const themeToggle = document.getElementById('themeToggle');
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'light');
                themeToggle.innerText = '🌙';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                themeToggle.innerText = '☀️';
            }
        });
    </script>
</body>
</html>
