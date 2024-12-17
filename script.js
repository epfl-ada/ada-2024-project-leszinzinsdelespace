class AudioPlayer {
    constructor() {
        this.songs = [
            'assets/songs/it_beggins_to_look_a_lot_like_christmas.mp3',
            'assets/songs/letitsnow.mp3',
            'assets/songs/Mastercarey.mp3',
            'assets/songs/vivelecringe.mp3'
        ];
        
        // Shuffle the songs array at initialization
        this.shuffleArray(this.songs);
        
        this.currentSongIndex = 0;
        this.isPlaying = false;
        this.audio = new Audio();
        this.audio.volume = 0.5;

        this.initializeControls();
        this.updateControlsVisibility(false); // Hide controls initially
        this.setupEventListeners();

        // Add device change listener
        navigator.mediaDevices.addEventListener('devicechange', () => {
            this.handleDeviceChange();
        });
    }

    // Add a shuffle method
    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    initializeControls() {
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.nextBtn = document.getElementById('nextBtn');
    }

    updateControlsVisibility(isPlaying) {
        const controls = document.querySelector('.audio-controls');
        if (isPlaying) {
            controls.classList.add('playing');
            this.nextBtn.style.display = 'flex';
            this.playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
        } else {
            controls.classList.remove('playing');
            this.nextBtn.style.display = 'none';
            this.playPauseBtn.innerHTML = '<i class="fas fa-music"></i> Enhance Experience';
        }
    }

    setupEventListeners() {
        this.playPauseBtn.addEventListener('click', () => this.togglePlayPause());
        this.nextBtn.addEventListener('click', () => this.playNext());
        
        this.audio.addEventListener('ended', () => this.playNext());
        this.audio.addEventListener('error', (e) => {
            console.error('Audio error:', e);
            this.playNext();
        });

        // Add audio state change listeners
        this.audio.addEventListener('pause', () => {
            this.playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
            this.isPlaying = false;
            this.updateControlsVisibility(false);
        });

        this.audio.addEventListener('play', () => {
            this.playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
            this.isPlaying = true;
            this.updateControlsVisibility(true);
        });
    }

    togglePlayPause() {
        if (!this.audio.src) {
            this.loadAndPlaySong(this.currentSongIndex);
            return;
        }

        if (this.isPlaying) {
            this.audio.pause();
            this.playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
            this.updateControlsVisibility(false);
        } else {
            this.audio.play()
                .then(() => {
                    this.playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                    this.updateControlsVisibility(true);
                })
                .catch(error => {
                    console.error('Error playing audio:', error);
                    this.playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
                    this.isPlaying = false;
                    this.updateControlsVisibility(false);
                    return;
                });
        }
        this.isPlaying = !this.isPlaying;
    }

    loadAndPlaySong(index) {
        this.audio.src = this.songs[index];
        this.audio.play()
            .then(() => {
                this.isPlaying = true;
                this.playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                this.updateControlsVisibility(true);
            })
            .catch(error => {
                console.error('Error playing audio:', error);
                this.isPlaying = false;
                this.playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
                this.updateControlsVisibility(false);
                this.playNext();
            });
    }

    playNext() {
        this.currentSongIndex = (this.currentSongIndex + 1) % this.songs.length;
        this.loadAndPlaySong(this.currentSongIndex);
    }

    // Add this new method
    handleDeviceChange() {
        if (this.isPlaying) {
            this.audio.pause();
            this.isPlaying = false;
            this.playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
            this.updateControlsVisibility(false);
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll(".section");
  const navItems = document.querySelectorAll(".side-nav li");
  const navIndicator = document.querySelector(".nav-indicator::after");

  // Only proceed with navigation setup if elements exist
  if (sections.length && navItems.length) {
    // Calculate the total height of the navigation
    const calculateIndicatorPosition = (index) => {
      const navItems = document.querySelectorAll(".side-nav li");
      let position = 0;
      
      for (let i = 0; i < index; i++) {
        position += navItems[i].offsetHeight + 20; // 20px is the gap between items
      }
      
      return `${position}px`;
    };

    // Update active nav item on scroll
    const updateActiveNav = () => {
      const scrollPosition = window.scrollY + window.innerHeight / 2;

      let found = false;
      sections.forEach((section, index) => {
        if (found) return;
        
        const sectionTop = section.getBoundingClientRect().top + window.pageYOffset - 20;
        const sectionBottom = section.getBoundingClientRect().bottom + window.pageYOffset - 20;

        if (scrollPosition >= sectionTop && scrollPosition <= sectionBottom) {
          found = true;
          
          navItems.forEach((item) => item.classList.remove("active"));
          navItems[index].classList.add("active");

          document.documentElement.style.setProperty(
            "--nav-indicator-top",
            calculateIndicatorPosition(index)
          );
        }
      });

      // Handle last section
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 100) {
        navItems.forEach((item) => item.classList.remove("active"));
        navItems[sections.length - 1].classList.add("active");
        document.documentElement.style.setProperty(
          "--nav-indicator-top",
          calculateIndicatorPosition(sections.length - 1)
        );
      }
    };

    // Smooth scroll to section when clicking nav items
    navItems.forEach((item) => {
      item.addEventListener("click", (e) => {
        e.preventDefault();
        const targetId = item.querySelector("a").getAttribute("href");
        const targetSection = document.querySelector(targetId);

        window.scrollTo({
          top: targetSection.getBoundingClientRect().top + window.pageYOffset - 100,
          behavior: "smooth",
        });
      });
    });

    // Listen for scroll events with debouncing
    let ticking = false;
    window.addEventListener("scroll", () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          updateActiveNav();
          ticking = false;
        });
        ticking = true;
      }
    });

    // Initial update
    updateActiveNav();
  }

  // Initialize the similarity calculator interface
  const inputs = document.querySelectorAll('.search-input');
  const goBtn = document.querySelector('.go-button');
  console.log("Found inputs:", inputs.length);
  console.log("Found go button:", goBtn !== null);

  // Global variables
  let embeddings = {};
  let wikiLinks = new Set(); // Store existing links

  // Load both embeddings and links data
  Promise.all([
    fetch('data/embeddings.csv').then(response => response.text()),
    fetch('data/links.csv').then(response => response.text())
  ])
  .then(([embeddingsData, linksData]) => {
    // Process embeddings
    const lines = embeddingsData.split('\n');
    const startIndex = lines[0].includes('article,embedding') ? 1 : 0;
    
    for (let i = startIndex; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line) {
            try {
                // More robust parsing of the CSV line
                const firstCommaIndex = line.indexOf(',');
                if (firstCommaIndex === -1) continue;

                // Extract and clean article name
                const article = decodeURIComponent(line.substring(0, firstCommaIndex))
                    .replace(/_/g, ' ')
                    .trim();

                // Extract and parse embedding array
                const embeddingStr = line.substring(firstCommaIndex + 1).trim();
                if (!embeddingStr.startsWith('[') || !embeddingStr.endsWith(']')) continue;

                const embedding = embeddingStr
                    .slice(1, -1)  // Remove brackets
                    .split(',')
                    .map(num => parseFloat(num.trim()))
                    .filter(num => !isNaN(num));

                if (embedding.length > 0) {
                    embeddings[article] = embedding;
                    console.log(`Loaded embedding for: ${article}`);  // Debug log
                }
            } catch (error) {
                console.error('Error processing line:', line, error);
            }
        }
    }
    
    // Process links
    const linkLines = linksData.split('\n');
    const linkStartIndex = linkLines[0].includes('source,target') ? 1 : 0;
    
    for (let i = linkStartIndex; i < linkLines.length; i++) {
        const line = linkLines[i].trim();
        if (line) {
            const [source, target] = line.split(',').map(x => decodeURI(x).replace('_', ' '));
            wikiLinks.add(`${source}|${target}`);
        }
    }
    
    console.log("Loaded embeddings:", Object.keys(embeddings).length);
    console.log("Loaded links:", wikiLinks.size);

    // Populate datalist after loading data
    const datalist = document.getElementById('articles');
    Object.keys(embeddings).forEach(article => {
        const option = document.createElement('option');
        option.value = article;
        datalist.appendChild(option);
    });
  })
  .catch(error => {
    console.error('Error loading data:', error);
  });

  // Check if link exists in the network
  function linkExists(start, target) {
    return wikiLinks.has(`${start}|${target}`);
  }

  // Calculate cosine similarity between two vectors
  function cosineSimilarity(vec1, vec2) {
    const dotProduct = vec1.reduce((sum, val, i) => sum + val * vec2[i], 0);
    const mag1 = Math.sqrt(vec1.reduce((sum, val) => sum + val * val, 0));
    const mag2 = Math.sqrt(vec2.reduce((sum, val) => sum + val * val, 0));
    return dotProduct / (mag1 * mag2);
  }

  // Function to calculate similarity and check link existence
  async function calculateSimilarity(startArticle, targetArticle) {
    console.log("Starting similarity calculation...");
    console.log("Start article:", startArticle);
    console.log("Target article:", targetArticle);
    console.log("Total embeddings loaded:", Object.keys(embeddings).length);
    console.log("Available articles:", Object.keys(embeddings).slice(0, 5)); // Show first 5 articles
    
    const start = startArticle.trim();
    const target = targetArticle.trim();

    // Get embeddings for both articles
    const startEmbedding = embeddings[start];
    const targetEmbedding = embeddings[target];

    if (!startEmbedding) {
        console.error(`Could not find embedding for start article: ${start}`);
        return null;
    }

    if (!targetEmbedding) {
        console.error(`Could not find embedding for target article: ${target}`);
        return null;
    }

    // Calculate cosine similarity
    const similarity = cosineSimilarity(startEmbedding, targetEmbedding);
    const exists = linkExists(start, target);
    
    console.log("Calculated similarity:", similarity);
    console.log("Link exists:", exists);
    
    return { similarity, exists };
  }

  // Update the GO button event listener
  const goButton = document.querySelector(".go-button");
  if (goButton) {
    goButton.addEventListener("click", async () => {
        console.log("GO button clicked");
        const startInput = document.querySelector('input[placeholder="start article"]');
        const targetInput = document.querySelector('input[placeholder="target article"]');

        console.log("Start input:", startInput?.value);
        console.log("Target input:", targetInput?.value);

        if (startInput && targetInput) {
            const startArticle = startInput.value.trim();
            const targetArticle = targetInput.value.trim();

            if (startArticle && targetArticle) {
                try {
                    const result = await calculateSimilarity(startArticle, targetArticle);
                    console.log("Calculation result:", result);
                    if (result !== null) {
                        updateResults(result.similarity, result.exists);
                    }
                } catch (error) {
                    console.error("Error during calculation:", error);
                }
            }
        }
    });
  } else {
    console.error("Could not find GO button");
  }

  // Update display with results
  function updateResults(similarity, exists) {
    console.log("Updating results with similarity:", similarity);
    
    // Update similarity score
    updateSimilarityScore(similarity);
    
    // Update existence message
    const notExist = document.querySelector(".not-exist");
    const shouldExist = document.querySelector(".should-exist");
    
    if (exists) {
        notExist.textContent = "THE LINK EXISTS";
        shouldExist.style.display = "none";
    } else {
        notExist.textContent = "THE LINK DOES NOT EXIST";
        shouldExist.style.display = "block";
    }
  }

  // Update similarity score display
  function updateSimilarityScore(score) {
    console.log("Updating similarity score:", score);
    const similarityValue = document.querySelector(".similarity-value");
    if (similarityValue) {
        console.log("Found similarity-value element");
        const currentScore = parseFloat(similarityValue.dataset.score || 0);
        const newScore = parseFloat(score);

        console.log("Current score:", currentScore);
        console.log("New score:", newScore);

        const duration = 1000;
        const start = performance.now();

        function updateScore(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = currentScore + (newScore - currentScore) * progress;
            
            console.log("Updating to value:", currentValue.toFixed(2));
            similarityValue.textContent = currentValue.toFixed(2);

            // Update gradient based on score
            const r = Math.round(31 + (currentValue * 224));
            const g = Math.round(31 + (currentValue * 82));
            const b = Math.round(255 - (currentValue * 112));
            
            const color = `rgb(${r}, ${g}, ${b})`; 
            
            similarityValue.style.background = color;
            similarityValue.style.boxShadow = `0 0 30px ${color.replace('rgb', 'rgba').replace(')', ', 0.3)')}`;

            if (progress < 1) {
                requestAnimationFrame(updateScore);
            } else {
                similarityValue.dataset.score = newScore;
                console.log("Final score set:", newScore);
            }
        }

        requestAnimationFrame(updateScore);
    } else {
        console.error("Could not find similarity-value element");
    }
  }

  // Add input validation
  document.querySelectorAll('.search-input').forEach(input => {
    input.setAttribute('list', 'articles'); // Make sure inputs are linked to datalist
    
    input.addEventListener('input', function() {
        const value = this.value;
        const datalistOptions = document.getElementById('articles').options;
        let isValid = false;
        
        // Check if the input matches any option in the datalist
        for (let option of datalistOptions) {
            if (option.value === value) {
                isValid = true;
                break;
            }
        }
        
        // Visual feedback for valid/invalid input
        if (isValid) {
            this.style.borderColor = 'rgba(255, 255, 255, 0.2)';
            this.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
        } else {
            this.style.borderColor = 'rgba(255, 31, 113, 0.5)';
            this.style.backgroundColor = 'rgba(255, 31, 113, 0.1)';
        }
    });
  });

  const audioPlayer = new AudioPlayer();
});

document.addEventListener('touchstart', function() {}, {passive: true});

function createSnowflakes() {
    const container = document.createElement('div');
    container.className = 'snow-container';
    document.body.prepend(container);

    const createSnowflake = () => {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        
        // Random starting position
        snowflake.style.left = `${Math.random() * 100}%`;
        
        // Random size
        const size = Math.random() * 4 + 2;
        snowflake.style.width = `${size}px`;
        snowflake.style.height = `${size}px`;
        
        // Much slower animation duration (increased to 8+5)
        snowflake.style.animationDuration = `${Math.random() * 8 + 5}s`;
        
        container.appendChild(snowflake);
        
        // Increased timeout for longer animation
        setTimeout(() => {
            snowflake.remove();
        }, 13000);
    };

    // Create initial snowflakes
    for (let i = 0; i < 30; i++) {
        setTimeout(createSnowflake, Math.random() * 2000);
    }

    // Much slower interval for creating snowflakes (increased to 500)
    setInterval(createSnowflake, 500);
}

// Start snow effect when page loads
document.addEventListener('DOMContentLoaded', createSnowflakes);

// Create modal container
const modal = document.createElement('div');
modal.className = 'graph-modal';
modal.innerHTML = `
    <button class="graph-modal-close">×</button>
    <img src="" alt="Full screen graph">
`;
document.body.appendChild(modal);

// Add click handlers to all regular graphs
document.querySelectorAll('.graph-container .graph, .graph-wrapper .graph').forEach(graph => {
    if (!graph.closest('.interactive-graph-container')) { // Exclude interactive graphs
        graph.addEventListener('click', function() {
            const modalImg = modal.querySelector('img');
            modalImg.src = this.src;
            modal.classList.add('active');
            document.body.classList.add('modal-open');
        });
    }
});

// Close modal when clicking outside the image or on close button
modal.addEventListener('click', function(e) {
    if (e.target === modal || e.target.classList.contains('graph-modal-close')) {
        modal.classList.remove('active');
        document.body.classList.remove('modal-open');
    }
});

// Close modal with escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        modal.classList.remove('active');
        document.body.classList.remove('modal-open');
    }
});

class PathVisualizer {
    constructor() {
        this.finishedPaths = Array.from({length: 20}, (_, i) => `assets/path_visualisation/finished_path_${i}.html`);
        this.unfinishedPaths = Array.from({length: 20}, (_, i) => `assets/path_visualisation/unfinished_path_${i}.html`);
        this.currentPath = this.finishedPaths[0];
        
        this.init();
    }

    init() {
        // Create container and controls
        const container = document.createElement('div');
        container.className = 'path-container';
        
        const controls = document.createElement('div');
        controls.className = 'path-controls';
        
        const finishedButton = document.createElement('button');
        finishedButton.className = 'path-button';
        finishedButton.textContent = 'Show Random Finished Path';
        
        const unfinishedButton = document.createElement('button');
        unfinishedButton.className = 'path-button';
        unfinishedButton.textContent = 'Show Random Unfinished Path';
        
        controls.appendChild(finishedButton);
        controls.appendChild(unfinishedButton);
        
        // Create iframe
        const iframe = document.createElement('iframe');
        iframe.src = this.currentPath;
        container.appendChild(iframe);
        
        // Add to DOM
        const beyondSection = document.querySelector('#beyond');
        if (beyondSection) {
            beyondSection.appendChild(controls);
            beyondSection.appendChild(container);
        }
        
        // Add event listeners
        finishedButton.addEventListener('click', () => {
            const randomPath = this.finishedPaths[Math.floor(Math.random() * this.finishedPaths.length)];
            if (randomPath !== this.currentPath) {
                this.currentPath = randomPath;
                iframe.src = this.currentPath;
            } else {
                // If same path is selected, try again
                finishedButton.click();
            }
        });
        
        unfinishedButton.addEventListener('click', () => {
            const randomPath = this.unfinishedPaths[Math.floor(Math.random() * this.unfinishedPaths.length)];
            if (randomPath !== this.currentPath) {
                this.currentPath = randomPath;
                iframe.src = this.currentPath;
            } else {
                // If same path is selected, try again
                unfinishedButton.click();
            }
        });
    }
}

// Initialize the path visualizer when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PathVisualizer();
});
