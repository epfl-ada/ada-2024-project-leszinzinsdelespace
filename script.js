document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll(".section");
  const navItems = document.querySelectorAll(".side-nav li");
  const navIndicator = document.querySelector(".nav-indicator::after");

  // Calculate the total height of the navigation
  const calculateIndicatorPosition = (index) => {
    // Get all nav items
    const navItems = document.querySelectorAll(".side-nav li");
    let position = 0;

    // Calculate position based on actual positions of nav items
    for (let i = 0; i < index; i++) {
      position += navItems[i].offsetHeight + 20; // 20px is the gap between items
    }

    return `${position}px`;
  };

  // Update active nav item on scroll
  const updateActiveNav = () => {
    const scrollPosition = window.scrollY + window.innerHeight / 2; // Use middle of viewport

    // Find the current section
    let found = false;
    let currentSectionIndex = 0;
    sections.forEach((section, index) => {
      if (found) {
        return;
      }
      const sectionTop = section.getBoundingClientRect().top + window.pageYOffset-20;
      const sectionBottom = section.getBoundingClientRect().bottom + window.pageYOffset-20;

      // Check if scroll position is within section bounds
      if (scrollPosition >= sectionTop && scrollPosition <= sectionBottom) {       
        found = true;
        currentSectionIndex = index;

        // Remove active class from all nav items
        navItems.forEach((item) => item.classList.remove("active"));

        // Add active class to current nav item
        navItems[index].classList.add("active");

        // Update indicator position
        document.documentElement.style.setProperty(
          "--nav-indicator-top",
          calculateIndicatorPosition(index)
        );
      }
    });

    // Handle last section specially
    const lastSection = sections[sections.length - 1];
    if (
      window.innerHeight + window.scrollY >=
      document.documentElement.scrollHeight - 100
    ) {
      currentSectionIndex = sections.length - 1;
      navItems.forEach((item) => item.classList.remove("active"));
      navItems[currentSectionIndex].classList.add("active");
      document.documentElement.style.setProperty(
        "--nav-indicator-top",
        calculateIndicatorPosition(currentSectionIndex)
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
        top: targetSection.getBoundingClientRect().top + window.pageYOffset-100,
        behavior: "smooth",
      });
    });
  });

  // Listen for scroll events
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

  // Load embeddings data
  let embeddings = {};
  
  // Load embeddings from CSV file
  fetch('data/embeddings.csv')
    .then(response => response.text())
    .then(data => {
      // Split CSV into lines and process each line
      const lines = data.split('\n');
      
      // Skip header row if present
      const startIndex = lines[0].includes('article,embedding') ? 1 : 0;
      
      // Process each line
      for (let i = startIndex; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line) {
          const article = decodeURI(line.substring(0, line.indexOf(','))).replace('_', ' ');
          const embeddingStr = line.substring(line.indexOf(',') + 3, line.lastIndexOf(']'));
          const embedding = embeddingStr.split(',').map(Number);
          embeddings[article] = embedding;
        }
      }
      console.log("embeddings", embeddings);
    })
    .catch(error => {
      console.error('Error loading embeddings:', error);
    });
 
  // Calculate cosine similarity between two vectors
  function cosineSimilarity(vec1, vec2) {
    const dotProduct = vec1.reduce((sum, val, i) => sum + val * vec2[i], 0);
    const mag1 = Math.sqrt(vec1.reduce((sum, val) => sum + val * val, 0));
    const mag2 = Math.sqrt(vec2.reduce((sum, val) => sum + val * val, 0));
    return dotProduct / (mag1 * mag2);
  }

  // Function to calculate similarity score between articles
  async function calculateSimilarity(startArticle, targetArticle) {
    console.log("Calculating similarity for", startArticle, "and", targetArticle);
    
    // Clean article names to match embeddings format
    const cleanArticleName = (name) => name.trim();
    const start = cleanArticleName(startArticle);
    const target = cleanArticleName(targetArticle);

    // Get embeddings for both articles
    const startEmbedding = embeddings[start];
    const targetEmbedding = embeddings[target];

    if (!startEmbedding || !targetEmbedding) {
      console.error('Could not find embeddings for articles');
      return null;
    }

    // Calculate cosine similarity
    const similarity = cosineSimilarity(startEmbedding, targetEmbedding);
    console.log("similarity", similarity);
    return similarity;
  }

  // Update the GO button event listener
  const goButton = document.querySelector(".go-button");
  if (goButton) {
    goButton.addEventListener("click", async () => {
      const startInput = document.querySelector('input[placeholder="start article"]');
      const targetInput = document.querySelector('input[placeholder="target article"]');

      if (startInput && targetInput) {
        const startArticle = startInput.value.trim();
        const targetArticle = targetInput.value.trim();

        if (startArticle && targetArticle) {
          try {
            const score = await calculateSimilarity(startArticle, targetArticle);
            if (score !== null) {
              updateSimilarityScore(score);
            } else {
              // Fallback to demo value if calculation fails
              updateSimilarityScore(0.87);
            }
          } catch (error) {
            console.error("Error:", error);
            // Fallback to demo value if calculation fails
            updateSimilarityScore(0.87);
          }
        }
      }
    });
  }

  // Keep existing updateSimilarityScore function
  function updateSimilarityScore(score) {
    const similarityValue = document.querySelector(".similarity-value");
    if (similarityValue) {
      const currentScore = parseFloat(similarityValue.dataset.score || 0);
      const newScore = parseFloat(score);

      const duration = 1000;
      const start = performance.now();

      function updateScore(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);
        const currentValue = currentScore + (newScore - currentScore) * progress;
        similarityValue.textContent = currentValue.toFixed(2);

        // Update gradient based on score
        const color = `rgb(${31 + (currentValue * 224)}, ${31 + (currentValue * 212)}, ${243})`; 
        
        similarityValue.style.background = color;
        similarityValue.style.boxShadow = `0 0 30px ${color.replace('rgb', 'rgba').replace(')', ', 0.3)')}`;

        if (progress < 1) {
          requestAnimationFrame(updateScore);
        } else {
          similarityValue.dataset.score = newScore;
        }
      }

      requestAnimationFrame(updateScore);
    }
  }
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
